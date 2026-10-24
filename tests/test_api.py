from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


def _fake_graph_builder(answer="Day 1: Arrive in Goa"):
    react_app = MagicMock()
    react_app.get_graph.return_value.draw_mermaid_png.return_value = b"png"
    react_app.invoke.return_value = {"messages": [SimpleNamespace(content=answer)]}
    builder = MagicMock(return_value=react_app)
    return MagicMock(return_value=builder), react_app


def test_query_returns_last_agent_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # main.py writes my_graph.png to the CWD
    import main

    graph_builder_cls, react_app = _fake_graph_builder()
    with patch.object(main, "GraphBuilder", graph_builder_cls):
        response = TestClient(main.app).post("/query", json={"question": "Plan 5 days in Goa"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Day 1: Arrive in Goa"}
    react_app.invoke.assert_called_once_with({"messages": ["Plan 5 days in Goa"]})


def test_query_returns_500_when_agent_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import main

    with patch.object(main, "GraphBuilder", side_effect=RuntimeError("missing GROQ_API_KEY")):
        response = TestClient(main.app).post("/query", json={"question": "Plan a trip"})

    assert response.status_code == 500
    assert "missing GROQ_API_KEY" in response.json()["error"]


def test_query_validates_payload():
    import main

    response = TestClient(main.app).post("/query", json={"wrong": "field"})
    assert response.status_code == 422
