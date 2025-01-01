import logging


def pars_arg(mes: str):
    mes_split = mes.split()
    logging.info(mes_split)
    return mes_split[-1] if len(mes_split) > 1 else None
