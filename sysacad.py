# -*- coding: utf-8 -*-


class SysAcad(object):
    """SysAcad"""
    def __init__(self,
                 alum_legajo,
                 alum_password,
                 sa_url='http://sysacadweb.frre.utn.edu.ar/',
                 sa_alum_url='menuAlumno.asp',
                 sa_doc_url='menuDocente.asp',
                 alum_mat_plan_url='materiasPlan.asp',
                 alum_est_acad_url='estadoAcademico.asp',
                 alum_exam_url='examenes.asp',
                 alum_cursado_url='notasParciales.asp',
                 alum_corr_cursar_url='correlatividadCursado.asp',
                 alum_corr_rend_url='correlatividadExamen.asp',
                 alum_insc_examen_url='materiasExamen.asp',
                 alum_camb_pass_url='cambioPassword.asp',
                 alum_avisos_url='menuAvisosAlumnos.asp',
                 alum_logout_url='loginAlumno.asp',
                 alum_insc_curs_url='materiasCursado.asp'
                ):
        """
        :alum_legajo:
        :alum_password:
        :sa_url:
        :sa_alum_url:
        :sa_doc_url:
        """
        super(SysAcad, self).__init__()
        # SysAcad
        self._sa_url = sa_url
        self._sa_alum_url = sa_alum_url
        self._sa_doc_url = sa_doc_url
        self._sa_session = None
        # Links Alumno
        self._alum_id = None
        self._alum_mat_plan_url = alum_mat_plan_url
        self._alum_est_acad_url = alum_est_acad_url
        self._alum_exam_url = alum_exam_url
        self._alum_cursado_url = alum_cursado_url
        self._alum_corr_cursar_url = alum_corr_cursar_url
        self._alum_corr_rend_url = alum_corr_rend_url
        self._alum_insc_examen_url = alum_insc_examen_url
        self._alum_camb_pass_url = alum_camb_pass_url
        self._avisos_url = alum_avisos_url
        self._alum_logout_url = alum_logout_url
        self._alum_insc_curs_url = alum_insc_curs_url
        # Alumno
        self._alum_legajo = alum_legajo
        self._alum_password = alum_password
        # Cache
        self._sa_cache = {}

    @property
    def id_alumno(self):
        """
        """
        return self._alum_id

    @property
    def sysacad_url(self):
        """
        """
        return self._sa_url

    @sysacad_url.setter
    def sysacad_url(self, url):
        """
        """
        self._sa_url = url

    @property
    def alumnos_url(self):
        """
        """
        return self._sa_alum_url

    @alumnos_url.setter
    def alumnos_url(self, url):
        """
        """
        self._sa_alum_url = url

    @property
    def docentes_url(self):
        """
        """
        return self._sa_doc_url

    @docentes_url.setter
    def docentes_url(self, url):
        """
        """
        self._sa_doc_url = url

    @property
    def legajo(self):
        """
        """
        return self._alum_legajo

    @legajo.setter
    def legajo(self, numero):
        """
        :numero:
        """
        self._alum_legajo = numero

    @property
    def password(self):
        return self._alum_password

    @password.setter
    def password(self, password):
        """
        :password:
        """
        self._alum_password = password

    def login(self, legajo=None, password=None):
        """
        :legajo:
        :password:
        """
        alum_legajo = self._alum_legajo if legajo is None else legajo
        alum_password = self._alum_password if password is None else password

        self._sa_session = requests.Session()
        self._sa_session.mount('http://', HTTPAdapter(max_retries=128))
        self._sa_session.mount('https://', HTTPAdapter(max_retries=128))

        # Define browser headers
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'es-ar,es;q=0.8,en-us;q=0.5,en;q=0.3',
                   'Connection': 'keep-alive',
                   'DNT': '1'
                   }

        data = {'legajo': alum_legajo,
                'password': alum_password,
                'loginbutton': 'Ingresar'
                }

        response = None
        login_url = '{0}{1}'.format(self._sa_url, self._sa_alum_url)

        try:
            response = self._sa_session.post(login_url,
                                             headers=headers,
                                             data=data,
                                             allow_redirects=True,
                                             stream=True)
            logging.debug(u(response.content))
        except (requests.ConnectionError,
                requests.HTTPError,
                requests.Timeout) as e:
            print(e)

        try:
            soup = BeautifulSoup(response.content)
            alum_id = soup.select('ul.textoTabla li a')[0]['href']
            self._alum_id = parse_qs(urlparse(alum_id).query)['id'][0]
        except Exception:  # FIXME: Agregar excepción adecuada
            pass

        return self._sa_session

    def logout(self):
        """
        """
        # Define browser headers
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'es-ar,es;q=0.8,en-us;q=0.5,en;q=0.3',
                   'Connection': 'keep-alive',
                   'DNT': '1'
                   }

        data = {'refrescar': ''}
        logout_url = '{0}{1}'.format(self._sa_url, self._alum_logout_url)
        response = None

        try:
            response = self._sa_session.get(logout_url,
                                            headers=headers,
                                            params=data,
                                            allow_redirects=True,
                                            stream=False)
        except (requests.ConnectionError,
                requests.HTTPError,
                requests.Timeout) as e:
            print(e)

        return response

    def get_examenes_alumno(self, force_refresh=False):
        """
        """
        # Check cache
        if not force_refresh and 'examenes' in self._sa_cache:
            logging.info('Loading examenes from cache...')
            return self._sa_cache['examenes']

        # Define browser headers
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'es-ar,es;q=0.8,en-us;q=0.5,en;q=0.3',
                   'Connection': 'keep-alive',
                   'DNT': '1'
                   }

        data = {'id': self._alum_id}
        examenes_url = '{0}{1}'.format(self._sa_url, self._alum_exam_url)
        response = None

        try:
            response = self._sa_session.get(examenes_url,
                                            headers=headers,
                                            params=data,
                                            allow_redirects=True,
                                            stream=False)
        except (requests.ConnectionError,
                requests.HTTPError,
                requests.Timeout) as e:
            print(e)

        try:
            soup = BeautifulSoup(response.content)
            examenes_rows = soup.select('tr.textoTabla')
        except Exception:  # FIXME: Agregar excepción adecuada
            pass

        notas = {'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5,
                 'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10,
                 'ausen.': None}
        stripper = text_type.strip
        lowerer = text_type.lower
        examenes = {}

        # Skip table headers
        for row in examenes_rows[1:]:
            examen = row.select('td')

            examen_fecha = examen[0].text.split('/')
            examen_fecha = date(int(examen_fecha[2]),
                                int(examen_fecha[1]),
                                int(examen_fecha[0]))

            examenes[int(examen[5].text)] = Examen(int(examen[5].text),                 #  Código
                                                   int(examen[4].text),                 #  Plan
                                                   stripper(examen[3].text),            #  Especialidad
                                                   notas.get(lowerer(examen[2].text)),  #  Nota
                                                   stripper(examen[1].text),            #  Materia
                                                   examen_fecha)                        #  Fecha

        # Update cache
        self._sa_cache['examenes'] = examenes

        return examenes

    def get_promedio_alumno(self):
        """
        """
        examenes = self.get_examenes_alumno()
        sum_aprobados = 0
        sum_desaprobados = 0
        cant_mat_desaprobados = 0
        cant_mat_aprobados = 0

        for examen in itervalues(examenes):
            nota = examen.nota

            try:
                if nota < 4:
                    sum_desaprobados += nota
                    cant_mat_desaprobados += 1
                else:
                    sum_aprobados += nota
                    cant_mat_aprobados += 1
            except TypeError:
                pass

        suma_aplazos = sum_aprobados + sum_desaprobados
        cant_aplazos = cant_mat_aprobados + cant_mat_desaprobados
        promedio_sin_aplazos = sum_aprobados / cant_mat_aprobados
        promedio_con_aplazos = suma_aplazos / cant_aplazos

        return (promedio_con_aplazos, promedio_sin_aplazos)

    def get_ranking_examenes(self, ord_desc=True):
        """
        """
        # 'asc': Ordenamiento ascendente
        # 'desc': Ordenamiento descendente
        # '': Sin ordenamiento

        examenes = self.get_examenes_alumno()
        contador_examenes = {}

        for examen in itervalues(examenes):
            codigo = examen.codigo
            try:
                if examen.nota is not None:
                    contador_examenes[codigo] += 1
            except KeyError:
                contador_examenes[codigo] = 1

        if ord_desc:
            contador_examenes = self._sort_desc(contador_examenes)
        else:
            contador_examenes = self._sort_asc(contador_examenes)

        return contador_examenes

    def _sort_asc(self, data):
        """
        """
        return sorted(iteritems(data), key=operator.itemgetter(1), reverse=False)

    def _sort_desc(self, data):
        """
        """
        return sorted(iteritems(data), key=operator.itemgetter(1), reverse=True)

    def get_exam_por_anio(self):
        """
        """
        examenes = self.get_examenes_alumno()
        examenes_anio = {}

        for examen in itervalues(examenes):
            year = examen.fecha.year

            try:
                if examen.nota is not None:
                    examenes_anio[year] += 1
            except KeyError:
                examenes_anio[year] = 1

        return examenes_anio

    def get_exam_por_ciclo_lectivo(self):
        """
        """
        examenes = self.get_examenes_alumno()
        examenes_ciclo = {}

        for examen in itervalues(examenes):
            year = examen.fecha.year
            month = examen.fecha.month
            ciclo = None

            try:
                if examen.nota is not None:
                    if month > 2:
                        ciclo = year
                        examenes_ciclo[ciclo] += 1
                    else:
                        ciclo = year - 1
                        examenes_ciclo[ciclo] += 1
            except KeyError:
                examenes_ciclo[ciclo] = 1

        return examenes_ciclo

    def get_estadisticas_examenes(self):
        """
        """
        examenes = self.get_examenes_alumno()

        aprobados = 0
        desaprobados = 0
        ausentes = 0

        for examen in itervalues(examenes):
            nota = examen.nota

            if nota is None:
                ausentes += 1
            elif nota < 4:
                desaprobados += 1
            else:
                aprobados += 1

        return {'aprobados': aprobados,
                'desaprobados': desaprobados,
                'ausentes': ausentes,
                'efectividad': aprobados * 100 / (aprobados + desaprobados)
                }

    def get_examen(self, codigo):
        """
        """
        try:
            examen = self.get_examenes_alumno()[codigo]
        except KeyError:
            examen = None

        return examen


class Examen(object):
    """Examen"""
    def __init__(self, codigo, plan, especialidad, nota, materia, fecha):
        super(Examen, self).__init__()
        self._codigo = codigo
        self._plan = plan
        self._especialidad = especialidad
        self._nota = nota
        self._materia = materia
        self._fecha = fecha

    @property
    def codigo(self):
        """
        """
        return self._codigo

    @property
    def plan(self):
        """
        """
        return self._plan

    @property
    def especialidad(self):
        """
        """
        return self._especialidad

    @property
    def nota(self):
        """
        """
        return self._nota

    @property
    def materia(self):
        """
        """
        return self._materia

    @property
    def fecha(self):
        """
        """
        return self._fecha
