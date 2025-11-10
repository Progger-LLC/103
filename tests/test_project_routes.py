import os
import pytest
import tempfile
import shutil
from modules.project_routes import repair_project_config

@pytest.fixture
def temp_project_yaml():
    """Creates a temporary project.yaml file for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_file = os.path.join(temp_dir, 'project.yaml')
        with open(project_file, 'w') as f:
            f.write("dependencies:\n  - package_a\n  - package_b\n")
        yield project_file

def test_repair_project_config(temp_project_yaml):
    """Tests the repair_project_config function."""
    # Test valid YAML structure
    repair_project_config(temp_project_yaml)
    
    # Check if template_version is added
    with open(temp_project_yaml, 'r') as f:
        config = yaml.safe_load(f)
        assert 'template_version' in config

def test_repair_project_config_backup(temp_project_yaml):
    """Tests that a backup is created before repairs."""
    backup_file = f"{temp_project_yaml}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    
    # Perform repair
    repair_project_config(temp_project_yaml)
    
    # Check if backup file exists
    assert os.path.exists(backup_file)