import asyncio
from aiohttp import ClientSession
from models import get_session, get_bancos, add_data
from bancos_data import load_data
from scraper import parse_cotizacion
from logger_factory import get_logger

logger = get_logger(__name__)
sem = asyncio.Semaphore(5)
db_session = get_session()
load_data(db_session)
bancos = get_bancos(db_session)


# @asyncio.coroutine
# def get(*args, **kwargs):
#     response = yield from aiohttp.request('GET', *args, **kwargs)
#     return (yield from response.text())

async def get(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


@asyncio.coroutine
def save_cotizacion(banco):
    with (yield from sem):
        body = yield from get(banco.url)
        cotizacion = parse_cotizacion(banco, body)
        if cotizacion and cotizacion.check_unique():
            logger.info("Intentando guardar cotización para Banco %s",
                        banco.name)
            try:
                add_data(cotizacion, db_session)
                logger.info("Guardada cotización %s", cotizacion)
            except Exception as e:
                logger.exception(e)
                raise e
        else:
            msj = ("No se pudo obtener cotización para Banco %s"
                   if not cotizacion
                   else "Ya existe cotización actualizada para Banco %s")
            logger.info(msj, banco.name)


def main():
    pages = [save_cotizacion(__) for __ in bancos]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(pages))


if __name__ == '__main__':
    main()
