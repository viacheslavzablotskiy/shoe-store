from shoping.celery import app
from offer.scripts import Trading


@app.task
def make_trades():
    Trading.make_trades_for_buy_offers()

