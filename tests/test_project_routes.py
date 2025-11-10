import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def temp_project_yaml(tmp_path):
    """Fixture to create a temporary project.yaml file."""
    project_file = tmp_path / "project.yaml"
    project_file.write_text(yaml.dump({'dependencies': []}))
    yield project_file
    if project_file.exists():
        project_file.unlink()

def test_repair_project_config_adds_template_version(temp_project_yaml):
    """Test that repair_project_config adds template_version if missing."""
    repair_project_config(str(temp_project_yaml), "templates.json")
    with open(temp_project_yaml, 'r') as file:
        config = yaml.safe_load(file)
    assert 'template_version' in config

def test_repair_project_config_backup(temp_project_yaml):
    """Test that repair_project_config creates a backup."""
    original_path = str(temp_project_yaml)
    repair_project_config(original_path, "templates.json")
    assert os.path.exists(f"{original_path}.bak")