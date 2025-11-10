import os
import pytest
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Fixture to set up a temporary project.yaml for testing."""
    project_yaml = tmp_path / 'project.yaml'
    project_yaml.write_text('dependencies:\n  fastapi: 0.104.1\n')
    yield project_yaml
    if project_yaml.exists():
        os.remove(project_yaml)

def test_repair_project_config(setup_project_yaml):
    """Test the repair_project_config function."""
    repair_project_config()
    with open(setup_project_yaml, 'r') as file:
        config = yaml.safe_load(file)
    
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'
    assert 'dependencies' in config