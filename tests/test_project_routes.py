import os
import pytest
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def set_up_project_yaml(tmp_path):
    """Set up a temporary project.yaml for testing."""
    project_yaml_content = """
    name: sample_project
    dependencies:
      fastapi: 0.104.1
    """
    project_yaml_path = tmp_path / "project.yaml"
    with open(project_yaml_path, 'w') as f:
        f.write(project_yaml_content)
    return project_yaml_path

def test_repair_project_config_adds_template_version(set_up_project_yaml):
    """Test that repair_project_config adds template_version if missing."""
    repair_project_config(set_up_project_yaml)
    
    with open(set_up_project_yaml) as f:
        config = yaml.safe_load(f)
    
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'

def test_repair_project_config_creates_backup(set_up_project_yaml):
    """Test that a backup is created before changes."""
    original_file = set_up_project_yaml
    repair_project_config(original_file)

    backup_file = f"{original_file}.{int(os.path.getmtime(original_file))}.bak"
    assert os.path.exists(backup_file)

def test_repair_project_config_invalid_yaml(set_up_project_yaml):
    """Test that repair_project_config raises an error on invalid YAML."""
    invalid_yaml_path = set_up_project_yaml
    with open(invalid_yaml_path, 'w') as f:
        f.write("invalid_yaml: [")

    with pytest.raises(Exception):
        repair_project_config(invalid_yaml_path)