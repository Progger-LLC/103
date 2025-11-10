import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_files(tmp_path):
    """Prepare test files for the repair function."""
    # Create a sample project.yaml with missing template_version
    project_yaml = tmp_path / "project.yaml"
    project_yaml.write_text("dependencies: []\n")
    
    templates_json = tmp_path / "templates.json"
    templates_json.write_text('{"version": "2.0.0"}\n')

    yield project_yaml, templates_json

def test_repair_project_config(setup_files):
    """Test the repair_project_config function."""
    project_yaml, templates_json = setup_files

    # Run the repair function
    repair_project_config()

    # Check if the template_version field was added
    with open(project_yaml, 'r') as file:
        config = yaml.safe_load(file)
    
    assert 'template_version' in config
    assert config['template_version'] == "2.0.0"

def test_backup_creation(setup_files, caplog):
    """Test that a backup is created before changes."""
    project_yaml, templates_json = setup_files

    # Run the repair function and check for backup log
    repair_project_config()
    
    assert any("Backup created:" in message for message in caplog.text)