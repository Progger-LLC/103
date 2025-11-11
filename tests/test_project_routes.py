import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def prepare_environment():
    """Prepare the environment for testing."""
    project_yaml_path = "project.yaml"
    if os.path.exists(project_yaml_path):
        os.remove(project_yaml_path)
    yield
    if os.path.exists(project_yaml_path):
        os.remove(project_yaml_path)

def test_repair_project_yaml_creates_backup(prepare_environment):
    """Test that a backup of project.yaml is created when it doesn't exist."""
    repair_project_config()
    assert os.path.exists("project.yaml.bak.")

def test_repair_project_yaml_creates_default_config(prepare_environment):
    """Test that project.yaml is created with default values."""
    repair_project_config()
    with open("project.yaml", 'r') as file:
        config = yaml.safe_load(file)
        assert config['entry_point'] == "main.py"
        assert config['template_version'] == "1.0.0"
        assert isinstance(config['dependencies'], list)

def test_repair_project_yaml_restores_on_failure(prepare_environment):
    """Test that project.yaml is restored from backup on failure."""
    with open("project.yaml", 'w') as file:
        file.write("invalid_yaml")
    
    repair_project_config()
    assert os.path.exists("project.yaml.bak.")
    # Check that the original file still exists (restored)
    with open("project.yaml", 'r') as file:
        config = yaml.safe_load(file)
        assert config['entry_point'] == "main.py"