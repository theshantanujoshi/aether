import pytest
import json
from pathlib import Path
from pydantic import TypeAdapter, ValidationError
import rocketride as rr

PIPELINES_DIR = Path(__file__).parent / "pipelines"

def get_pipeline_files():
    if not PIPELINES_DIR.exists():
        return []
    return list(PIPELINES_DIR.glob("*.pipe"))

@pytest.mark.parametrize("pipe_file", get_pipeline_files(), ids=lambda p: p.name)
def test_pipeline_schema_validity(pipe_file: Path):
    """Test that the pipeline file is valid JSON and matches the RocketRide PipelineConfig schema."""
    with open(pipe_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    adapter = TypeAdapter(rr.PipelineConfig)
    try:
        adapter.validate_python(data)
    except ValidationError as e:
        pytest.fail(f"Schema validation failed for {pipe_file.name}:\n{e}")

@pytest.mark.parametrize("pipe_file", get_pipeline_files(), ids=lambda p: p.name)
def test_pipeline_has_required_components(pipe_file: Path):
    """Test that the pipeline has at least a webhook source and a response component."""
    with open(pipe_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    components = data.get("components", [])
    assert len(components) > 0, "Pipeline must have components"
    
    providers = [c.get("provider") for c in components]
    assert "webhook" in providers, "Pipeline must have a webhook source"
    assert "response_text" in providers, "Pipeline must have a response_text component"

def test_structuring_pipeline_specifics():
    """Test specifics of the structuring.pipe"""
    pipe_path = PIPELINES_DIR / "structuring.pipe"
    if not pipe_path.exists():
        pytest.skip("structuring.pipe not found")
        
    with open(pipe_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    providers = [c.get("provider") for c in data.get("components", [])]
    assert "embedding_transformer" in providers, "Structuring pipeline should have an embedding component"
    assert "qdrant" in providers, "Structuring pipeline should have a qdrant component"

def test_synthesis_pipeline_specifics():
    """Test specifics of the synthesis.pipe"""
    pipe_path = PIPELINES_DIR / "synthesis.pipe"
    if not pipe_path.exists():
        pytest.skip("synthesis.pipe not found")
        
    with open(pipe_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    providers = [c.get("provider") for c in data.get("components", [])]
    assert "llm_openai" in providers, "Synthesis pipeline should use llm_openai"
