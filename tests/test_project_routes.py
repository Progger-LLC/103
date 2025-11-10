import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Fixture to set up and tear down a temporary project.yaml file."""
    project_yaml = tmp_path / "project.yaml"
    backup_yaml = tmp_path / "project_backup.yaml"
    
    # Create a sample project.yaml for testing
    content = """
    dependencies:
      - fastapi
      - uvicorn
    """
    project_yaml.write_text(content)
    
    yield project_yaml, backup_yaml
    
    # Cleanup
    if project_yaml.exists():
        project_yaml.unlink()
    if backup_yaml.exists():
        backup_yaml.unlink()

def test_repair_project_config(setup_project_yaml):
    """Test the repair_project_config function."""
    project_yaml, backup_yaml = setup_project_yaml
    
    # Run the repair function
    repair_project_config()
    
    # Check that project.yaml has the correct fields
    with open(project_yaml, 'r') as file:
        config = yaml.safe_load(file)
    
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'  # Default value
    assert 'dependencies' in config
    assert isinstance(config['dependencies'], list)

def test_repair_project_config_no_file(tmp_path):
    """Test repair_project_config when project.yaml does not exist."""
    os.chdir(tmp_path)  # Change to temp path
    repair_project_config()  # Should not raise an error