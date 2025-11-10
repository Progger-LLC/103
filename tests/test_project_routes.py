import pytest
import os
import shutil
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Setup a temporary project.yaml for testing."""
    project_yaml = tmp_path / "project.yaml"
    project_yaml.write_text("dependencies:\n  - fastapi\n")
    yield project_yaml
    if project_yaml.exists():
        os.remove(project_yaml)

@pytest.fixture
def setup_templates_json(tmp_path):
    """Setup a temporary templates.json for testing."""
    templates_json = tmp_path / "templates.json"
    templates_json.write_text('{"version": "1.0.1"}')
    yield templates_json
    if templates_json.exists():
        os.remove(templates_json)

def test_repair_project_config(setup_project_yaml, setup_templates_json):
    """Test the repair_project_config function."""
    repair_project_config()
    
    with open(setup_project_yaml, 'r') as file:
        config = yaml.safe_load(file)
        
    assert 'template_version' in config
    assert config['template_version'] == "1.0.1"

def test_backup_creation(setup_project_yaml):
    """Test if backup is created before changes."""
    original_backup_path = "backup/project_backup_*.yaml"
    repair_project_config()
    
    assert len(glob.glob(original_backup_path)) == 1