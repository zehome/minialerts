# -*- coding: utf-8 -*-

import datetime
import re

from django.db import models
from django.utils.timezone import utc
from django.utils.timesince import timesince
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail.message import make_msgid
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context, Template
from django.conf import settings

ATYPES = (
    ('WARN', 'warning'),
    ('CRIT', 'critical'),
    ('UNKN', 'unknown'),
)

class AlertMatch(models.Model):
    field = models.CharField(max_length=128, blank=False)
    regex = models.CharField(max_length=1024, blank=False)
    level = models.CharField(max_length=4, choices=ATYPES, blank=False)
    # Comma separated email list
    emails = models.CharField(max_length=1024, blank=False)

    def __unicode__(self):
        return u"%s on %s -> %s" % (self.regex, self.field, self.emails)

    def getemaillist(self):
        # Yeah A Big uggly cleaning I agree.
        return list(set(self.emails.lower().replace(";", ",").\
                                replace(' ','').split(',')))

class Alert(models.Model):
    host = models.CharField(max_length=128, blank=False)
    group = models.CharField(max_length=128, blank=False)
    category = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    label = models.CharField(max_length=128)
    atype = models.CharField(max_length=4, choices=ATYPES, blank=False)
    arange = models.CharField(max_length=128)
    ipaddr = models.CharField(max_length=128)
    extinfo = models.TextField(u'Extended inforamtions')
    date = models.DateTimeField(auto_now_add=True, blank=False)
    date_last_tick = models.DateTimeField(auto_now_add=True, auto_now=True,
                                          blank=False)
    date_last_alerted = models.DateTimeField(blank=True, null=True)
    checked = models.BooleanField(default=False, blank=False)
    ignored = models.BooleanField(default=False, blank=False, null=False)
    email_sent = models.BooleanField(default=False, blank=False)

    class Meta:
        verbose_name = "Alert"

    def __unicode__(self):
        return u"%s@%s %s" % (self.host, self.group, self.title)

    def displayclass(self):
        if self.ignored:
            return "info"
        if self.atype == "critical":
            return "error"
        return self.atype

    def timedelta(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        return u"%s" % timesince(self.date_last_tick, now)

    def tick(self, other):
        self.date_last_tick = datetime.datetime.now()
        self.value = other.value
        self.extinfo = other.extinfo
        self.save()

    def __eq__(self, b):
        return (self.host == b.host and self.group == b.group and
                self.title == b.title)

    def sendemail(self, destList, alertmatch):
        """Send this alert by main to destList emails."""
        # Email Body
        template_context = Context({'alert': self, 'alertmatch': alertmatch})
        template = get_template("alerts/email.txt")
        data = template.render(template_context)
        # Email Subject
        template = get_template("alerts/email_subject.txt")
        subject = template.render(template_context)
        mail = EmailMessage(subject, data, settings.DEFAULT_FROM_EMAIL, destList)
        mail.extra_headers['Message-ID'] = make_msgid()
        mail.extra_headers["X-MINIALERTS-ID"] = self.pk
        mail.send()
        self.email_sent = True
        self.save()

@receiver(post_save, sender=Alert)
def alert_created(sender, **kw):
    instance = kw.get('instance')
    created = kw.get('created')
    if created and not instance.email_sent:
        matchs = AlertMatch.objects.all()
        for m in matchs:
            f = getattr(instance, m.field, None)
            if re.match(m.regex, str(f)):
                print "Should send email for alertMatch %s" % (unicode(m))
                instance.sendemail(m.getemaillist(), m)
