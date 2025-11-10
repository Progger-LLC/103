import pytest
import os
import shutil
from modules.project_routes import repair_project_config

def test_repair_project_config_valid_file():
    """Test the repair of a valid project.yaml file."""
    original_file = 'tests/test_files/project.yaml'
    backup_file = f"{original_file}.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    repair_project_config(original_file, 'tests/test_files/templates.json')

    assert os.path.exists(original_file)
    assert os.path.exists(backup_file)

def test_repair_project_config_invalid_yaml():
    """Test the repair of an invalid project.yaml file."""
    original_file = 'tests/test_files/invalid_project.yaml'
    with pytest.raises(Exception):
        repair_project_config(original_file, 'tests/test_files/templates.json')

    assert not os.path.exists(original_file)