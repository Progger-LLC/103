import pytest
import os
import shutil
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_yaml_file(tmp_path):
    """Fixture to set up a temporary project.yaml file."""
    yaml_content = """
    required_field_1: old_value
    """
    yaml_file = tmp_path / "project.yaml"
    yaml_file.write_text(yaml_content)
    yield yaml_file
    os.remove(yaml_file)

def test_repair_project_config(setup_yaml_file):
    """Test the repair_project_config function."""
    # Move the yaml file to the expected location
    shutil.move(str(setup_yaml_file), "project.yaml")
    
    # Call the repair function
    repair_project_config()
    
    # Check if the file was repaired correctly
    with open("project.yaml", 'r') as file:
        config = yaml.safe_load(file)
    
    assert 'required_field_2' in config
    assert config['required_field_2'] == "default_value_2"