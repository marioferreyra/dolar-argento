import emoji


def format_cotizaciones_for_telegram(cotizaciones):
    formated = []
    for cotizacion in cotizaciones:
        formated.append(_format_cotizacion(cotizacion))
    return "\n\n".join(formated)


def _format_cotizacion(cotizacion):
    banco = emoji.emojize(":bank: *{0}*".format(cotizacion.banco.name),
                          use_aliases=True)
    compra = emoji.emojize(
        ":dollar: Compra: $*{0}*".format(
            _format_numbers(cotizacion.compra)
        ),
        use_aliases=True
    )
    venta = emoji.emojize(
        ":dollar: Venta: $*{0}*".format(
            _format_numbers(cotizacion.venta)
        ),
        use_aliases=True
    )

    updated = emoji.emojize(
        ":alarm_clock: Actualizado: {0}".format(cotizacion.timestamp),
        use_aliases=True
    )

    return "\n".join([banco, compra, venta, updated])


def _format_numbers(value):
    return "{0:.2f}".format(value).replace(".", ",")
