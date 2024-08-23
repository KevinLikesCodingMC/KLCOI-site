import datetime
import os
from . import get_rd
from KLC.settings import BASE_DIR


def update():
    now = datetime.datetime.now()

    with open(os.path.join(BASE_DIR, "data/lst_date.txt"), "r", encoding='utf-8') as f:
        lst = f.readline()

    if lst != now.strftime("%Y-%m-%d"):
        with open(os.path.join(BASE_DIR, "data/lst_date.txt"), "w", encoding='utf-8') as f:
            f.write(now.strftime("%Y-%m-%d"))
        get_rd.write_prob(20)

