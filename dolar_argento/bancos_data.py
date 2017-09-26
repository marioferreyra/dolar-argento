from models import Banco, add_data

galicia = Banco(
    url='http://www.infodolar.com/cotizacion-dolar-entidad-banco-galicia.aspx',
    name='Galicia')

nacion = Banco(
    url='http://www.infodolar.com/cotizacion-dolar-entidad-banco-nacion.aspx',
    name='Nación'
)

frances = Banco(
    url='http://www.infodolar.com/cotizacion-dolar-entidad-bbva-banco-frances.aspx',
    name='BBVA Francés'
)

bancos = [galicia, nacion, frances]


def load_data(session):
    add_data(bancos, session)
