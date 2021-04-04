import pytest

from src.data_acquisition.collect_tickers_data import DataCollector


def test_create_data_collector():
    tickers = DataCollector()
    assert tickers is not None


@pytest.mark.parametrize('market', ['br', 'us'])
def test_add_market(market):
    tickers = DataCollector(symbols_list=['ITUB4.SA'], market=market)
    tickers.get_tickers_set(qty=5)

    if market == 'br':
        assert len(tickers.add_market()) == 3
        assert '^BVSP' in tickers.add_market()
    else:
        assert len(tickers.add_market()) == 4
        assert 'SPY' in tickers.add_market()
