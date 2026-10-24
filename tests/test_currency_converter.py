from unittest.mock import MagicMock, patch

import pytest

from utils.currency_converter import CurrencyConverter


def _response(status=200, payload=None):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = payload or {}
    return resp


@patch("utils.currency_converter.requests.get")
def test_convert_uses_latest_rate(mock_get):
    mock_get.return_value = _response(payload={"conversion_rates": {"INR": 90.0, "USD": 1.08}})
    result = CurrencyConverter("dummy").convert(10, "EUR", "INR")
    assert result == pytest.approx(900.0)
    assert "EUR" in mock_get.call_args.args[0]


@patch("utils.currency_converter.requests.get")
def test_unknown_target_currency_raises(mock_get):
    mock_get.return_value = _response(payload={"conversion_rates": {"USD": 1.08}})
    with pytest.raises(ValueError):
        CurrencyConverter("dummy").convert(10, "EUR", "XYZ")


@patch("utils.currency_converter.requests.get")
def test_api_failure_raises(mock_get):
    mock_get.return_value = _response(status=403, payload={"result": "error"})
    with pytest.raises(Exception):
        CurrencyConverter("dummy").convert(10, "EUR", "USD")
