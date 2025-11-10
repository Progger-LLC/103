import pytest
import yaml
import os
from modules.project_routes import repair_project_config

@pytest.fixture
def mock_project_yaml(tmp_path):
    """Create a mock project.yaml file for testing."""
    yaml_content = """
    name: example_project
    version: 1.0
    dependencies:
      - fastapi
      - uvicorn
    """
    yaml_file = tmp_path / "project.yaml"
    yaml_file.write_text(yaml_content)
    return yaml_file

def test_repair_project_config(mock_project_yaml):
    """Test the repair_project_config function."""
    repair_project_config(str(mock_project_yaml))
    
    with open(mock_project_yaml) as f:
        config = yaml.safe_load(f)
    
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'  # Check default version
    assert config['dependencies'] == ['fastapi', 'uvicorn']  # Check dependencies preserved

def test_repair_project_config_backup(mock_project_yaml):
    """Test that a backup is created during repair."""
    original_file = str(mock_project_yaml)
    repair_project_config(original_file)
    assert os.path.exists(f"{original_file}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak")