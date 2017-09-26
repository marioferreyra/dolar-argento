from time import mktime, strptime
from datetime import datetime
from pyquery import PyQuery as PQ
from models import Cotizacion


def parse_cotizacion(banco, body):
    try:
        table = PQ(".GridViewCotizaciones", body)
        compra, venta = table.find(".compraVenta")
        datetime = table.find(".timeago").attr("title")

        compra = parse_value(compra.text)
        venta = parse_value(venta.text)
        datetime = parse_date(datetime)

        return Cotizacion(
            compra=compra,
            venta=venta,
            date=datetime.date(),
            time=datetime.time(),
            banco=banco,
        )
    except Exception as e:
        return None


def parse_value(value):
    return float(value.strip().replace("$", "").replace(",", "."))


def parse_date(value):
    struct_date = strptime(value, "%Y-%m-%dT%H:%M:%S")
    return datetime.fromtimestamp(mktime(struct_date))
