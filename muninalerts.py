#!/usr/bin/env python

import ConfigParser
import logging
import urllib2
import urllib
import json
import sys
import os
import re

logger = logging.getLogger("muninalerts")

class Alert(object):
    def __init__(self, atype, data):
        super(Alert, self).__init__()
        assert(atype in ("warning", "critical"))
        self.data = data
        self.type = atype
        self.label = data["label"]
        self.value = data["value"]
        self.extinfo = data["extinfo"]
        if atype == "warning":
            self.range = data.get("wrange", "")
        elif atype == "critical":
            self.range = data.get("crange", "")

class HostAlert(object):
    def __init__(self, json_data, mapping):
        super(HostAlert, self).__init__()
        self.json_data = json_data
        self.host = self.json_data["host"]
        self.group = self.json_data["group"]
        self.ip = mapping.get("%s;%s" % (self.group, self.host), '')
        if not self.ip:
            self.ip = mapping.get(self.host, '')
        self.category = self.json_data["category"]
        self.title = self.json_data["title"]
        self.alerts = []
        for warn in self.json_data.get("warnings", []):
            self.alerts.append(Alert("warning", warn))
        for crit in self.json_data.get("criticals", []):
            self.alerts.append(Alert("critical", crit))

    def alertsdict(self):
        ret = []
        for alert in self.alerts:
            ret.append({
                "host": self.host, "group": self.group,
                "ip": self.ip,
                "category": self.category, "title": self.title,
                "type": alert.type, "label": alert.label,
                "value": alert.value, "range": alert.range,
                "extinfo": alert.extinfo})
        return ret

    def __str__(self):
        return "%s@%s %d warnings %d criticals" % (self.json_data["host"],
                                      self.json_data["group"],
                                      len(self.json_data.get("warnings", [])),
                                      len(self.json_data.get("criticals", [])))
    def __repr__(self):
        return self.__str__()

class MuninResolver(object):
    def __init__(self, munin_config_dir):
        self._section_re = re.compile("^\s*\[([a-zA-Z0-9;\.-_]+)\]")
        self._address_re = re.compile("^\s*address\s*([a-zA-Z0-9\.]+)")
        self.munin_config_dir = munin_config_dir
        self.mapping = {}

    def readconfig(self):
        for fname in os.listdir(self.munin_config_dir):
            fpath = os.path.join(self.munin_config_dir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                logger.debug("Parsing %s", fpath)
                file = open(fpath, "r")
                section = None
                for l in file.readlines():
                    m = self._section_re.match(l)
                    if m:
                        section = m.group(1)
                    m = self._address_re.match(l)
                    if m:
                        address = m.group(1)
                        if section:
                            self.mapping[section] = address
            except:
                logger.exception("Munin config parse error.")
        return self.mapping

    def resolve(self, hostalert):
        if hostalert.group:
            mapping_key = "%s;%s" % (hostalert.group, hostalert.host)
        else:
            mapping_key = hostalert.host
        return self.mapping_hostip.get(mapping_key, None)

class Decoder(object):
    """Read inputfile and decode using json.loads each line."""
    def __init__(self, inputfile):
        self.inputfile = inputfile
        self.output = []

    def read(self):
        self.output = []

        lineidx = 0
        while True:
            line = self.inputfile.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            lineidx += 1
            try:
                self.output.append(self.decode(line))
            except ValueError:
                logger.exception("Unable to decode line %d." % (lineidx,))
        return self.output

    def decode(self, line):
        return json.loads(line)

class AlertFactory(object):
    def __init__(self, hostalertklass=HostAlert):
        self.klass = hostalertklass
        super(AlertFactory, self).__init__()

    def build(self, json_data, mapping):
        return self.klass(json_data, mapping)

class HttpSync(object):
    def __init__(self, url):
        self.url = url

    def sync(self, hostalerts):
        alerts = []
        for host in hostalerts:
            alerts.extend(host.alertsdict())
        postdata = {'alerts': json.dumps(alerts) }
        request = urllib2.Request(url=self.url, data=urllib.urlencode(postdata))
        request.add_header('User-agent', 'MuninAlerts/1.0')
        try:
            urlf = urllib2.urlopen(request, timeout=20)
            rawdata = urlf.read()
            logger.debug("Received: %s", rawdata)
            urlf.close()
        except urllib2.URLError, e:
            if hasattr(e, "read"):
                print e.read()
            else:
                logger.exception(u"URLError. No internet access?")
            raise
        except urllib2.HTTPError, e:
            if e.code == 403:
                logger.error(u"Access denied.")
            raise
        except Exception, e:
            logger.exception("URLLIB2 exception.")
            raise

if __name__ == "__main__":
    from cStringIO import StringIO
    logging.basicConfig(level=logging.DEBUG)

    factory = AlertFactory()
    
    sio = StringIO()
    sio.write(sys.stdin.read())
    sio.seek(0)

    # IP address host resolver
    resolver = MuninResolver("/etc/munin/munin-conf.d")
    mapping = resolver.readconfig()

    decoder = Decoder(sio)
    hostalerts = []
    for json_alert in decoder.read():
        hostalerts.append(factory.build(json_alert, mapping))

    # HTTP Sync
    syncer = HttpSync("http://127.0.0.1/minialerts/alerts/push/")
    syncer.sync(hostalerts)

    sys.exit(0)

