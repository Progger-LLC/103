import os
import pytest
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Setup a temporary project.yaml for testing."""
    project_yaml = tmp_path / "project.yaml"
    project_yaml.write_text("dependencies:\n  - package1\n  - package2\n")
    yield project_yaml
    if project_yaml.exists():
        project_yaml.unlink()

def test_repair_project_config_valid(setup_project_yaml):
    """Test repairing a valid project.yaml."""
    repair_project_config()
    with open(setup_project_yaml, 'r') as file:
        data = yaml.safe_load(file)
    assert 'template_version' in data
    assert isinstance(data['dependencies'], list)

def test_repair_project_config_no_file(tmp_path):
    """Test repair when project.yaml does not exist."""
    repair_project_config()
    assert not (tmp_path / "project.yaml").exists()