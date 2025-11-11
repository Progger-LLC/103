import os
import pytest
import yaml
from modules.project_routes import fix_project_yaml

@pytest.fixture
def setup_yaml_file(tmp_path):
    """Fixture to create a temporary project.yaml file."""
    yaml_content = {'dependencies': ['example-package']}
    yaml_file = tmp_path / "project.yaml"
    with open(yaml_file, 'w') as f:
        yaml.dump(yaml_content, f)
    yield yaml_file

def test_fix_project_yaml_creates_file_when_not_exists(setup_yaml_file):
    """Test that fix_project_yaml creates a new project.yaml if it doesn't exist."""
    os.remove(setup_yaml_file)
    fix_project_yaml()
    assert os.path.exists(setup_yaml_file)

def test_fix_project_yaml_updates_fields(setup_yaml_file):
    """Test that fix_project_yaml updates project.yaml with required fields."""
    fix_project_yaml()
    with open(setup_yaml_file, 'r') as f:
        config = yaml.safe_load(f)
        assert 'template_version' in config
        assert 'dependencies' in config