import pytest

from src.data_acquisition.collect_tickers_data import TickersCollector


def test_create_data_collector():
    tickers = TickersCollector()
    assert tickers is not None


@pytest.mark.parametrize('market', ['br', 'us', 'jp'])
def test_add_market(market):
    tickers = TickersCollector(market=market, qty=0)

    if market == 'br':
        assert len(tickers.add_market()) == 2
        assert '^BVSP' in tickers.add_market()
    else:
        assert len(tickers.add_market()) == 3
        assert 'SPY' in tickers.add_market()
