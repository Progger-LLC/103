import pytest
import os
import yaml
from modules.project_repair import repair_project_yaml

@pytest.fixture
def setup_yaml_file(tmp_path):
    """Setup a temporary YAML file for testing."""
    yaml_content = """
    entry_point: main.py
    dependencies:
      - fastapi==0.104.1
    """
    yaml_file = tmp_path / "project.yaml"
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
    return yaml_file

@pytest.fixture
def templates_json_file(tmp_path):
    """Setup a temporary templates.json file for testing."""
    templates_content = '{"template_version": "1.0.0"}'
    templates_file = tmp_path / "templates.json"
    with open(templates_file, 'w') as f:
        f.write(templates_content)
    return templates_file

def test_repair_project_yaml(setup_yaml_file, templates_json_file):
    """Test repairing project.yaml."""
    repair_project_yaml(str(setup_yaml_file), str(templates_json_file))
    
    with open(setup_yaml_file, 'r') as f:
        config = yaml.safe_load(f)
    
    assert config['template_version'] == "1.0.0"
    assert 'dependencies' in config
    assert 'entry_point' in config

def test_repair_with_missing_template_version(setup_yaml_file, templates_json_file):
    """Test repairing project.yaml when template_version is missing."""
    yaml_content = """
    entry_point: main.py
    """
    with open(setup_yaml_file, 'w') as f:
        f.write(yaml_content)
    
    repair_project_yaml(str(setup_yaml_file), str(templates_json_file))
    
    with open(setup_yaml_file, 'r') as f:
        config = yaml.safe_load(f)

    assert config['template_version'] == "1.0.0"