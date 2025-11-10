import pytest
import os
import shutil
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Setup a temporary project.yaml for testing."""
    project_yaml = tmp_path / "project.yaml"
    project_yaml.write_text("dependencies:\n  - package1\n")
    yield project_yaml
    if project_yaml.exists():
        os.remove(project_yaml)

def test_repair_project_config_missing_template_version(setup_project_yaml):
    """Test repairing project.yaml when template_version is missing."""
    # Move to the temporary directory
    os.chdir(setup_project_yaml.parent)

    # Call the repair function
    repair_project_config()

    # Load the repaired project.yaml
    with open("project.yaml", 'r') as file:
        config = yaml.safe_load(file)

    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'  # Check default version
    assert 'dependencies' in config