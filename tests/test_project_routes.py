import os
import pytest
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Fixture to set up a temporary project.yaml file for testing."""
    yaml_content = {
        'template_version': '1.0',
        'dependencies': {
            'existing-package': '1.0.0'
        }
    }
    yaml_file = tmp_path / "project.yaml"
    with open(yaml_file, 'w') as file:
        yaml.dump(yaml_content, file)
    return yaml_file

def test_repair_project_config(setup_project_yaml):
    """Test the repair_project_config function."""
    repair_project_config()
    
    with open(setup_project_yaml, 'r') as file:
        config = yaml.safe_load(file)
    
    assert config['template_version'] == '1.0'
    assert 'default-package' in config['dependencies']
    assert config['dependencies']['default-package'] == 'latest'

def test_repair_project_config_no_file(tmp_path):
    """Test the repair_project_config function when project.yaml does not exist."""
    repair_project_config()
    assert os.path.exists('project.yaml')