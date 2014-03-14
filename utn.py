# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import operator
import requests
import sys

from bs4 import BeautifulSoup
from datetime import datetime, date
from requests.adapters import HTTPAdapter

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

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


class UTN(object):
    """UTN"""
    def __init__(self, website_url='', cv_url=''):
        """
        :website_url:
        :cv_url:
        """
        super(UTN, self).__init__()
        self._website_url = website_url
        self._cv_url = cv_url

    @property
    def website_url(self):
        return self._website_url

    @website_url.setter
    def website_url(self, url):
        """
        :url:
        """
        self._website_url = url

    @property
    def cv_url(self):
        return self._cv_url

    @cv_url.setter
    def cv_url(self, url):
        """
        :url:
        """
        self._cv_url = url


class FRRe(UTN):
    """FRRe"""
    def __init__(self,
                 website_url='http://frre.utn.edu.ar',
                 cv_url='http://frre.cvg.utn.edu.ar'):
        """
        :website_url:
        :cv_url:
        """
        super(FRRe, self).__init__()
        self._website_url = website_url
        self._cv_url = cv_url
        self._session = None

    def _get_html_calendar(self, calendar_url):
        """
        :calendar_url:
        """
        if self._session is None:
            self._session = requests.Session()
            self._session.mount('http://', HTTPAdapter(max_retries=128))
            self._session.mount('https://', HTTPAdapter(max_retries=128))

        # Define browser headers
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'es-ar,es;q=0.8,en-us;q=0.5,en;q=0.3',
                   'Connection': 'keep-alive',
                   'DNT': '1'
                   }

        response = None

        try:
            curr_year = datetime.now().year
            retrieve_url = '{0}{1}{2}'.format(self._website_url,
                                              calendar_url,
                                              curr_year)
            response = self._session.get(retrieve_url,
                                         headers=headers,
                                         allow_redirects=False,
                                         stream=False)
        except (requests.ConnectionError,
                requests.HTTPError,
                requests.Timeout) as e:
            print(e)

        if response is not None:
            soup = BeautifulSoup(response.content)

            return soup.select('div.xw_content table tbody tr')
        else:
            return None

    def get_isi_iem_iq_lar_calendar(self):
        """
        """
        calendar_html = self._get_html_calendar('/www/paginas/view/item/isi_iem_iq_lar_')
        calendar = []
        calendar_append = calendar.append
        stripper = text_type.strip

        for row in calendar_html:
            columns = row.select('td')

            try:
                fecha_desde = columns[0].text.split('-')
                fd_year = int(fecha_desde[2])
                fd_month = int(fecha_desde[1])
                fd_day = int(fecha_desde[0])
                fecha_desde = {'year': fd_year,
                               'month': fd_month,
                               'day': fd_day
                               }
            except ValueError:
                fd_days = fecha_desde[0].replace('y', ',').split(',')
                fecha_desde = [{'year': fd_year, 'month': fd_month, 'day': fd_day}
                              for fd_day in fd_days]
            except (IndexError, TypeError):
                fecha_desde = None

            try:
                fecha_hasta = columns[1].text.split('-')
                fh_year = int(fecha_hasta[2])
                fh_month = int(fecha_hasta[1])
                fh_day = int(fecha_hasta[0])
                fecha_hasta = {'year': fh_year, 'month': fh_month, 'day': fh_day}
            except ValueError:
                fh_days = fecha_hasta[0].replace('y', ',').split(',')
                fecha_hasta = [{'year': fh_year, 'month': fh_month, 'day': fh_day}
                              for fh_day in fh_days]
            except (IndexError, TypeError):
                fecha_hasta = None

            calendar_append({'fecha_desde': fecha_desde,
                             'fecha_hasta': fecha_hasta,
                             'actividad': stripper(columns[-1].text)})

        return calendar

    def get_tsa_gies_tsp_calendar(self):
        """
        """
        calendar_html = self._get_html_calendar('/www/paginas/view/item/tsa_y_gies_tsp_')
        calendar = []
        calendar_append = calendar.append
        stripper = text_type.strip

        for row in calendar_html:
            columns = row.select('td')

            try:
                fecha_desde = columns[0].text.split('-')
                fd_year = int(fecha_desde[2])
                fd_month = int(fecha_desde[1])
                fd_day = int(fecha_desde[0])
                fecha_desde = {'year': fd_year,
                               'month': fd_month,
                               'day': fd_day
                               }
            except ValueError:
                fd_days = fecha_desde[0].replace('y', ',').split(',')
                fecha_desde = [{'year': fd_year, 'month': fd_month, 'day': fd_day}
                              for fd_day in fd_days]
            except (IndexError, TypeError):
                fecha_desde = None

            try:
                fecha_hasta = columns[1].text.split('-')
                fh_year = int(fecha_hasta[2])
                fh_month = int(fecha_hasta[1])
                fh_day = int(fecha_hasta[0])
                fecha_hasta = {'year': fh_year,
                               'month': fh_month,
                               'day': fh_day
                               }
            except ValueError:
                fh_days = fecha_hasta[0].replace('y', ',').split(',')
                fecha_hasta = [{'year': fh_year, 'month': fh_month, 'day': fh_day}
                              for fh_day in fh_days]
            except (IndexError, TypeError):
                fecha_hasta = None

            calendar_append({'fecha_desde': fecha_desde,
                             'fecha_hasta': fecha_hasta,
                             'actividad': stripper(columns[-1].text)})

        return calendar

    def get_feriados_calendar(self):
        """
        """
        calendar_html = self._get_html_calendar('/www/paginas/view/item/feriados_dias_no_laborables_y_conmemorativos_')
        calendar = []
        calendar_append = calendar.append
        stripper = text_type.strip
        months = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
                  'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
                  'octubre': 10, 'noviembre': 11, 'diciembre': 12}
        calendar_year = datetime.now().year

        for row in calendar_html:
            columns = row.select('td')

            fer_date = columns[0].text.split()
            days = fer_date[:-1]
            month_str = fer_date[-1].lower()

            fecha_feriado = [{'year': calendar_year,
                              'month': months.get(month_str, 1),
                              'day': int(dia)}
                             for dia in days
                             if dia.isdigit()]

            calendar_append({'fecha_desde': fecha_feriado,
                             'actividad': stripper(columns[-1].text)})

        return calendar


class Calendario(object):
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items_list):
        self._items = items_list

    def add_item(self, item):
        if isinstance(item, ItemCalendario):
            self._items.append(item)


class ItemCalendario(object):
    def __init__(self, fecha_desde, fecha_hasta, actividad):
        self._fecha_desde = fecha_desde
        self._fecha_hasta = fecha_hasta
        self._actividad = actividad

    @property
    def fecha_desde(self):
        return self._fecha_desde

    @fecha_desde.setter
    def fecha_desde(self, fecha):
        self._fecha_desde = fecha

    @property
    def fecha_hasta(self):
        return self._fecha_hasta

    @fecha_hasta.setter
    def fecha_hasta(self, fecha):
        self._fecha_hasta = fecha

    @property
    def actividad(self):
        return self._actividad

    @actividad.setter
    def actividad(self, descripcion):
        self._actividad = descripcion


if __name__ == '__main__':
    import logging

    # -------------------------- Logging Config ----------------------------------
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(levelname)s] : %(message)s")
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] : %(message)s")
    # ----------------------------------------------------------------------------

    frre = FRRe()
    logging.debug(frre.get_isi_iem_iq_lar_calendar())
