#!venv/bin/python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import logging
import sys

from sysacad import SysAcad, Examen
from utn import UTN, FRRe

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from flask.views import MethodView

# ----------------------------------------------------------------------------
# ------------------ Python 2 / Python 3 Compatibility -----------------------
# ----------------------------------------------------------------------------

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if not PY2:
    text_type = str
    string_types = (str,)
    unichr = chr
    inp = input
    _iterkeys = 'keys'
    _itervalues = 'values'
    _iteritems = 'items'
    _iterlists = 'lists'

    def b(s):
        return s.encode('utf-8')

    def u(s):
        return s

    def a(s):
        return s
else:
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr
    inp = raw_input
    _iterkeys = 'iterkeys'
    _itervalues = 'itervalues'
    _iteritems = 'iteritems'
    _iterlists = 'iterlists'

    def b(s):
        return s

    def u(s):
        return unicode(s, 'unicode_escape')

    def a(s):
        return s.encode('ascii', 'ignore')


def iterkeys(d, **kw):
    """Return an iterator over the keys of a dictionary."""
    return iter(getattr(d, _iterkeys)(**kw))

def itervalues(d, **kw):
    """Return an iterator over the values of a dictionary."""
    return iter(getattr(d, _itervalues)(**kw))

def iteritems(d, **kw):
    """Return an iterator over the (key, value) pairs of a dictionary."""
    return iter(getattr(d, _iteritems)(**kw))

def iterlists(d, **kw):
    """Return an iterator over the (key, [values]) pairs of a dictionary."""
    return iter(getattr(d, _iterlists)(**kw))
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# -------------------------- Logging Config ----------------------------------
logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)s] : %(message)s")
logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] : %(message)s")
# ----------------------------------------------------------------------------


# Flask App
app = Flask(__name__, static_url_path = "")
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'ssebastianj':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'message': 'Resource not found',
                                  'status': 404}), 404)


class CalendarListAPI(Resource):
    def get(self):
        return {}


class CalendarAPI(Resource):
    def get(self, id):
        frre = FRRe()
        calendar = frre.get_isi_iem_iq_lar_calendar()
        return {'calendar': calendar.items[1].fecha_desde}

api.add_resource(CalendarListAPI, a('/v1/calendars'), endpoint = a('calendars'))
api.add_resource(CalendarAPI, a('/v1/calendars/<int:id>'), endpoint = a('calendar'))


if __name__ == '__main__':
    app.run(debug=True)
