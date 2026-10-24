"""Builds the real LangGraph agent with a fake LLM so the wiring is tested without API calls."""
from unittest.mock import MagicMock, patch


def test_graph_registers_all_tools_and_nodes():
    fake_llm = MagicMock()
    with patch("agent.agentic_workflow.ModelLoader") as loader, \
         patch("tools.place_search_tool.GooglePlaceSearchTool"):
        loader.return_value.load_llm.return_value = fake_llm
        from agent.agentic_workflow import GraphBuilder

        builder = GraphBuilder(model_provider="groq")
        graph = builder()

    tool_names = {t.name for t in builder.tools}
    assert {"get_current_weather", "get_weather_forecast", "search_attractions",
            "search_restaurants", "convert_currency", "calculate_total_expense"} <= tool_names
    fake_llm.bind_tools.assert_called_once()
    assert {"agent", "tools"} <= set(graph.get_graph().nodes)
