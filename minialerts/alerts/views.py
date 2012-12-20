# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from alerts.models import Alert

def index(request):
    alerts = Alert.objects.filter(checked=False).order_by('atype', '-date_last_tick')
    try:
        last_alert = Alert.objects.all().order_by("-date_last_tick")[0]
    except IndexError:
        last_alert = None
    if last_alert:
        last_update = last_alert.date_last_tick
        last_update_delta = u"il y a %s" % (last_alert.timedelta(), )
    else:
        last_update = None
        last_update_delta = ''
    return render_to_response('alerts/list.html',
        {'alerts': alerts,
         'last_update': last_update,
         'last_update_delta': last_update_delta})

@csrf_exempt
def push(request):
    """
    data pushed by standalone python script (run by munin-limits)
    """
    json_alerts = request.POST.get("alerts")
    if not json_alerts:
        return
    alerts = json.loads(json_alerts)

    opened_alerts = Alert.objects.filter(checked=False)

    for a in alerts:
        alert = Alert(host=a["host"], group=a["group"],
            category=a["category"], title=a["title"],
            value=a["value"], label=a["label"],
            atype=a["type"], arange=a["range"],
            ipaddr=a.get("ip", ""),
            extinfo=a["extinfo"])
        for oa in opened_alerts:
            if oa == alert:
                oa.tick(alert)
                alert = None
                break
        if alert:
            alert.save()
    return HttpResponse(200, 'Good!')

def toggle(request, alertid):
    alert = get_object_or_404(Alert, pk=alertid)
    alert.checked = not alert.checked
    alert.save()
    return HttpResponse(json.dumps(alert.checked), mimetype="application/json")
