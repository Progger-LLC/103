import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_yaml_file(tmp_path):
    """Fixture to setup a temporary project.yaml file."""
    project_yaml = tmp_path / "project.yaml"
    project_yaml.write_text("dependencies:\n  packageA: 1.0.0\n")
    yield project_yaml
    # Cleanup
    if project_yaml.exists():
        project_yaml.unlink()

def test_repair_project_config(setup_yaml_file):
    """Test repair_project_config adds missing template_version."""
    original_yaml = setup_yaml_file.read_text()
    repair_project_config()
    
    # Load the updated yaml
    updated_yaml = yaml.safe_load(setup_yaml_file.read_text())
    
    assert 'template_version' in updated_yaml
    assert updated_yaml['template_version'] == "1.0.0"  # default version added
    assert original_yaml != setup_yaml_file.read_text()  # Ensure the file was modified

def test_invalid_yaml_handling(setup_yaml_file):
    """Test handling of invalid YAML."""
    setup_yaml_file.write_text("invalid_yaml: [")
    repair_project_config()
    
    # Check that the file hasn't changed due to invalid YAML
    assert setup_yaml_file.read_text() == "invalid_yaml: ["

def test_backup_creation(setup_yaml_file):
    """Test that backup file is created."""
    repair_project_config()
    assert os.path.exists(f'project_backup_*.yaml')  # Check for backup

@pytest.mark.parametrize("bad_dependency", [
    ("packageB", None),  # Invalid version
    (None, "1.0.0"),     # Invalid name
])
def test_validate_dependencies(bad_dependency):
    """Test invalid dependency formats."""
    with pytest.raises(ValueError):
        validate_dependencies({bad_dependency[0]: bad_dependency[1]})