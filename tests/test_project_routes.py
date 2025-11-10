import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Setup a temporary project.yaml for testing."""
    config_data = {
        'dependencies': {
            'fastapi': '0.104.1',
            'uvicorn': '0.24.0'
        }
    }
    config_path = tmp_path / "project.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    return config_path

def test_repair_project_config(setup_project_yaml):
    """Test the repair of project.yaml."""
    config_path = setup_project_yaml
    repair_project_config(config_path)

    # Reload the config to check changes
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    assert config['template_version'] == "1.0.0"  # Check default version
    assert 'dependencies' in config  # Ensure dependencies are intact