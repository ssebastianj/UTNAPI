# -*- coding: utf-8 -*-


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
                fecha_desde = date(fd_year, fd_month, fd_day)
            except ValueError:
                fd_days = fecha_desde[0].replace('y', ',').split(',')
                fecha_desde = tuple(date(fd_year, fd_month, int(fd_day))
                                    for fd_day in fd_days)
            except (IndexError, TypeError):
                fecha_desde = None

            try:
                fecha_hasta = columns[1].text.split('-')
                fh_year = int(fecha_hasta[2])
                fh_month = int(fecha_hasta[1])
                fh_day = int(fecha_hasta[0])
                fecha_hasta = date(fh_year, fh_month, fh_day)
            except ValueError:
                fh_days = fecha_hasta[0].replace('y', ',').split(',')
                fecha_hasta = tuple(date(fh_year, fh_month, int(fd_day))
                                    for fd_day in fh_days)
            except (IndexError, TypeError):
                fecha_hasta = None

            calendar_append((fecha_desde, fecha_hasta, stripper(columns[-1].text)))
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
                fecha_desde = date(fd_year, fd_month, fd_day)
            except ValueError:
                fd_days = fecha_desde[0].replace('y', ',').split(',')
                fecha_desde = tuple(date(fd_year, fd_month, int(fh_day))
                                    for fh_day in fd_days)
            except (IndexError, TypeError):
                fecha_desde = None

            try:
                fecha_hasta = columns[1].text.split('-')
                fh_year = int(fecha_hasta[2])
                fh_month = int(fecha_hasta[1])
                fh_day = int(fecha_hasta[0])
                fecha_hasta = date(fh_year, fh_month, fh_day)
            except ValueError:
                fh_days = fecha_hasta[0].replace('y', ',').split(',')
                fecha_hasta = tuple(date(fh_year, fh_month, int(fh_day))
                                    for fh_day in fh_days)
            except (IndexError, TypeError):
                fecha_hasta = None

            calendar_append((fecha_desde, fecha_hasta, stripper(columns[-1].text)))
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

            fecha_feriado = tuple(date(calendar_year,
                                       months.get(month_str, 1),
                                       int(dia))
                                  for dia in days
                                  if dia.isdigit())

            calendar_append((fecha_feriado, stripper(columns[-1].text)))
        return calendar
