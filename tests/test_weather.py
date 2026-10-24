from unittest.mock import MagicMock, patch

from utils.weather_info import WeatherForecastTool
from tools.weather_info_tool import WeatherInfoTool


def _response(status=200, payload=None):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = payload or {}
    return resp


@patch("utils.weather_info.requests.get")
def test_current_weather_returns_empty_dict_on_error(mock_get):
    mock_get.return_value = _response(status=404)
    assert WeatherForecastTool("dummy").get_current_weather("Nowhere") == {}


@patch("utils.weather_info.requests.get")
def test_forecast_requests_metric_units(mock_get):
    mock_get.return_value = _response(payload={"list": []})
    WeatherForecastTool("dummy").get_forecast_weather("Rome")
    params = mock_get.call_args.kwargs["params"]
    assert params["q"] == "Rome" and params["units"] == "metric"


def test_forecast_tool_formats_summary():
    tool = WeatherInfoTool()
    tool.weather_service = MagicMock()
    tool.weather_service.get_forecast_weather.return_value = {
        "list": [
            {"dt_txt": "2026-11-01 12:00:00", "main": {"temp": 18.5}, "weather": [{"description": "clear sky"}]},
            {"dt_txt": "2026-11-02 12:00:00", "main": {"temp": 16.0}, "weather": [{"description": "light rain"}]},
        ]
    }
    forecast = {t.name: t for t in tool._setup_tools()}["get_weather_forecast"]
    text = forecast.invoke({"city": "Rome"})
    assert "Weather forecast for Rome" in text
    assert "2026-11-01: 18.5" in text and "light rain" in text


def test_forecast_tool_handles_missing_data():
    tool = WeatherInfoTool()
    tool.weather_service = MagicMock()
    tool.weather_service.get_forecast_weather.return_value = {}
    forecast = {t.name: t for t in tool._setup_tools()}["get_weather_forecast"]
    assert forecast.invoke({"city": "Atlantis"}) == "Could not fetch forecast for Atlantis"
