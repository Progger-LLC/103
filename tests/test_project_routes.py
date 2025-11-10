import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def temp_yaml_file(tmpdir):
    """Fixture to create a temporary project.yaml file for testing."""
    file_path = tmpdir.join("project.yaml")
    content = """
    dependencies:
      fastapi: 0.104.1
    """
    with open(file_path, 'w') as f:
        f.write(content)
    return str(file_path)

def test_repair_project_config_missing_template_version(temp_yaml_file):
    """Test repairing project.yaml with missing template_version."""
    repair_project_config(temp_yaml_file)
    
    with open(temp_yaml_file, 'r') as f:
        config = yaml.safe_load(f)

    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'

def test_repair_project_config_invalid_dependencies(temp_yaml_file):
    """Test repair fails with invalid dependencies format."""
    with open(temp_yaml_file, 'w') as f:
        f.write("""
        dependencies: [fastapi]
        """)
    
    with pytest.raises(ValueError):
        repair_project_config(temp_yaml_file)