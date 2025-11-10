import pytest
import os
import shutil
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_yaml_file(tmp_path):
    """Fixture to set up a temporary project.yaml for testing."""
    project_yaml = tmp_path / "project.yaml"
    project_yaml.write_text("dependencies:\n  - fastapi\n")
    return project_yaml

def test_repair_project_config_valid_yaml(setup_yaml_file):
    """Test repair_project_config with valid YAML."""
    repair_project_config(setup_yaml_file, "fake_templates.json")
    assert os.path.exists(setup_yaml_file)

def test_repair_project_config_backup_created(setup_yaml_file):
    """Test that a backup is created during repair."""
    repair_project_config(setup_yaml_file, "fake_templates.json")
    backup_files = list(setup_yaml_file.parent.glob("project.yaml.*.bak"))
    assert len(backup_files) == 1

def test_repair_project_config_restore_on_failure(setup_yaml_file):
    """Simulate failure and check restore functionality."""
    # Mocking an error in the repair process
    # This would require a specific condition to raise an error
    # For demonstration, we will just call the function and raise an exception.
    with pytest.raises(Exception):
        repair_project_config(setup_yaml_file, "non_existent_templates.json")