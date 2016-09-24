# -*- coding: utf-8 -*-

import datetime
import requests
import web


# GLOBAL var keeping track of the Ducks
ducks = {}


urls = (
    '/', 'Index',
    '/report/(\d*)', 'Report',
)

render = web.template.render('templates/')


def set_reporting(id, ip):
    ducks[id] = {'last_seen': datetime.datetime.now(),
                 'ip_address': ip}


def is_awake(timestamp):
    # if we haven't seen a duck in aminute we consider it asleep
    if datetime.datetime.now() - timestamp > datetime.timedelta(0, 60):
        return 'Sleeping'
    return 'Awake'


def get_location_region(ip):
    try:
        r = requests.get('http://ipinfo.io/{}'.format(ip))
        return r.json()['region']
    except:
        return 'Unknown'


def duck_status():
    return [
        {'id': k, 'awake': is_awake(v['last_seen']), 'where': get_location_region(v['ip_address'])}
        for (k, v) in ducks.items()
    ]


class Index:
    def GET(self):
        status = duck_status()
        return render.index(status)


class Report:
    def GET(self, id):
        set_reporting(id, web.ctx.ip)
        return "OK"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
