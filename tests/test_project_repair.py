import pytest
import os
import shutil
from modules.project_repair import fix_project_yaml

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Fixture to create a sample project.yaml."""
    yaml_content = """
    project:
      name: Sample Project
      version: 1.0
      dependencies:
        - fastapi
        - sqlalchemy
    """
    file_path = tmp_path / "project.yaml"
    with open(file_path, 'w') as f:
        f.write(yaml_content)
    return str(file_path)

def test_fix_project_yaml(setup_project_yaml):
    """Test the fix_project_yaml function."""
    templates_file = 'templates.json'  # Assuming this file exists for the test
    fix_project_yaml(setup_project_yaml, templates_file)
    
    # Check if the backup is created
    assert os.path.exists(f"{setup_project_yaml}.bak")
    
    # Validate the repaired YAML
    with open(setup_project_yaml, 'r') as f:
        yaml_data = yaml.safe_load(f)
        assert 'template_version' in yaml_data  # Check if the field is added