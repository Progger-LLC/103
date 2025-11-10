import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_temp_yaml(tmp_path):
    """Set up a temporary YAML file for testing."""
    yaml_content = """
    dependencies:
      - fastapi
      - uvicorn
    """
    yaml_file = tmp_path / "project.yaml"
    with open(yaml_file, 'w') as file:
        file.write(yaml_content)
    return yaml_file

def test_repair_project_config(setup_temp_yaml):
    """Test repairing the project.yaml configuration."""
    file_path = setup_temp_yaml
    repair_project_config(str(file_path))

    # Load the modified YAML file to check its content
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    assert 'template_version' in config
    assert config['template_version'] == "1.0.0"
    assert 'dependencies' in config