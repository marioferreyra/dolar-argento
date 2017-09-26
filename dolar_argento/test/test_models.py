import unittest
import datetime
from ..models import (get_engine, get_session, get_bancos,
                      get_last_cotizaciones, Banco, Cotizacion)


class TestModels(unittest.TestCase):
    """docstring for TestModels"""

    def setUp(self):
        engine = get_engine('sqlite://')
        self.session = get_session(engine)

    def test_bancos(self):
        self.session.add(
            Banco(
                url='www.galicia.com',  # noqa
                name='Galicia')
        )
        self.session.commit()

        self.assertEqual(1, len(get_bancos(self.session)))

    def test_cotizaciones(self):
        galicia = Banco(
            url='www.galicia.com',
            name='Galicia')
        self.session.add(galicia)
        self.session.commit()

        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        one_hour_ago = now - datetime.timedelta(hours=1)

        g_now = Cotizacion(
            compra=1,
            venta=1,
            date=now.date(),
            time=now.time(),
            banco=galicia,
        )

        g_yesterday = Cotizacion(
            compra=1,
            venta=1,
            date=yesterday.date(),
            time=yesterday.time(),
            banco=galicia,
        )

        g_one_hour_ago = Cotizacion(
            compra=1,
            venta=1,
            date=one_hour_ago.date(),
            time=one_hour_ago.time(),
            banco=galicia,
        )

        self.session.add_all([g_now, g_yesterday, g_one_hour_ago])
        self.session.commit()

        cotizaciones = get_last_cotizaciones(now, self.session)
        self.assertEqual(1, len(cotizaciones))
        cotizacion_galicia = cotizaciones[0]
        self.assertEqual(g_now, cotizacion_galicia)

    def test_cotizaciones_multiples_bancos(self):
        galicia = Banco(
            url='www.galicia.com',
            name='Galicia')
        nacion = Banco(
            url='www.nacion.com',
            name='Nación')

        self.session.add_all([galicia, nacion])
        self.session.commit()

        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        one_hour_ago = now - datetime.timedelta(hours=1)

        g_now = Cotizacion(
            compra=1,
            venta=1,
            date=now.date(),
            time=now.time(),
            banco=galicia,
        )
        g_yesterday = Cotizacion(
            compra=1,
            venta=1,
            date=yesterday.date(),
            time=yesterday.time(),
            banco=galicia,
        )
        g_one_hour_ago = Cotizacion(
            compra=1,
            venta=1,
            date=one_hour_ago.date(),
            time=one_hour_ago.time(),
            banco=galicia,
        )

        n_now = Cotizacion(
            compra=1,
            venta=1,
            date=now.date(),
            time=now.time(),
            banco=nacion,
        )
        n_yesterday = Cotizacion(
            compra=1,
            venta=1,
            date=yesterday.date(),
            time=yesterday.time(),
            banco=nacion,
        )
        n_one_hour_ago = Cotizacion(
            compra=1,
            venta=1,
            date=one_hour_ago.date(),
            time=one_hour_ago.time(),
            banco=nacion,
        )

        self.session.add_all([g_now, g_yesterday, g_one_hour_ago,
                              n_now, n_yesterday, n_one_hour_ago])
        self.session.commit()

        cotizaciones = get_last_cotizaciones(now, self.session)
        self.assertEqual(2, len(cotizaciones))

        cotizacion_galicia = next(
            (c for c in cotizaciones if c.banco_id == galicia.id), None
        )
        self.assertEqual(g_now, cotizacion_galicia)

        cotizacion_nacion = next(
            (c for c in cotizaciones if c.banco_id == nacion.id), None
        )
        self.assertEqual(n_now, cotizacion_nacion)

    def tearDown(self):
        self.session = None
