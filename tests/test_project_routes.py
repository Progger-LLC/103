import pytest
import yaml
import os
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_yaml_file(tmp_path):
    """Fixture to set up a temporary project.yaml file for testing."""
    yaml_content = """
    entry_point: main.py
    dependencies:
      - fastapi
    """
    yaml_file = tmp_path / "project.yaml"
    yaml_file.write_text(yaml_content)
    yield yaml_file
    os.remove(yaml_file)

def test_repair_project_config(setup_yaml_file):
    """Test the repair_project_config function."""
    # Simulate missing template_version
    with open(setup_yaml_file, 'a') as f:
        f.write("\ntemplate_version: \n")

    repair_project_config()

    with open(setup_yaml_file, 'r') as f:
        config = yaml.safe_load(f)

    assert 'template_version' in config
    assert config['template_version'] == "1.0"
    assert 'entry_point' in config
    assert 'dependencies' in config

def test_repair_project_config_invalid_yaml(setup_yaml_file):
    """Test handling of invalid YAML."""
    with open(setup_yaml_file, 'w') as f:
        f.write("invalid_yaml: ")

    with pytest.raises(Exception):
        repair_project_config()

    # Ensure the original file still exists and is not corrupted
    with open(setup_yaml_file, 'r') as f:
        assert f.read() == "invalid_yaml: "