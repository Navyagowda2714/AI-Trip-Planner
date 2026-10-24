from pathlib import Path

from utils.config_loader import load_config
from utils.save_to_document import save_document


def test_config_defines_both_llm_providers():
    config = load_config()
    assert {"groq", "openai"} <= set(config["llm"])
    for provider in config["llm"].values():
        assert provider["model_name"]


def test_save_document_writes_markdown(tmp_path):
    path = save_document("## Day 1\nVisit the Colosseum", directory=str(tmp_path))
    assert path is not None
    content = Path(path).read_text(encoding="utf-8")
    assert path.endswith(".md")
    assert "Visit the Colosseum" in content
    assert "AI Travel Plan" in content
