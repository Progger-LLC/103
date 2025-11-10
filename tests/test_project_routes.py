import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Sets up a temporary project.yaml for testing."""
    project_yaml_path = tmp_path / "project.yaml"
    project_yaml_path.write_text("dependencies:\n  - fastapi\n")
    yield project_yaml_path
    os.remove(project_yaml_path)

def test_repair_project_config_missing_template_version(setup_project_yaml):
    """Test repairing project.yaml with a missing template_version."""
    repair_project_config()

    with open(setup_project_yaml, 'r') as file:
        config = yaml.safe_load(file)

    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'
    assert isinstance(config['dependencies'], list)

def test_repair_project_config_creates_backup(setup_project_yaml):
    """Test that a backup file is created before changes."""
    backup_file = f"project_backup_*.yaml"
    
    repair_project_config()
    
    assert len(list(tmp_path.glob(backup_file))) == 1