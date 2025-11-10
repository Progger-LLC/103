import pytest
import os
import shutil
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_test_environment(tmp_path):
    """Setup a test environment for project config."""
    config_file = tmp_path / 'project.yaml'
    config_content = """
    dependencies:
      - fastapi
      - pydantic
    """
    config_file.write_text(config_content)
    yield config_file
    # Cleanup after tests
    if config_file.exists():
        os.remove(config_file)

def test_repair_project_config(setup_test_environment):
    """Test repairing project.yaml configuration."""
    project_yaml = setup_test_environment
    
    # Run repair function
    repair_project_config(str(project_yaml))
    
    # Reload the config to check the updates
    with open(project_yaml, 'r') as f:
        config = yaml.safe_load(f)
    
    # Assertions
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'
    assert 'dependencies' in config
    assert isinstance(config['dependencies'], list)