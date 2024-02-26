import csv
from models.mics import Taqvim
from models.base import db


# update time
def create_taqvim():

    for i in range(6, 8):
        date = f"2024-02-{20 + i}" if i < 21 else f"2024-04-{i - 20}"
        Taqvim.create(
            img=f"{i:03d}.jpg",
            date=date,
            region="xorazm")


if __name__ == '__main__':
    db.connect()
    db.create_tables([Taqvim])
    create_taqvim()
    db.close()
