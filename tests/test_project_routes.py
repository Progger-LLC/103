import pytest
import os
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_project_yaml(tmp_path):
    """Fixture to set up a sample project.yaml for testing."""
    project_yaml_content = """
    dependencies:
      some_dependency: 1.0.0
    """
    project_yaml_path = tmp_path / "project.yaml"
    project_yaml_path.write_text(project_yaml_content)
    return project_yaml_path

def test_repair_project_config(setup_project_yaml):
    """Test repair_project_config function."""
    # Ensure the initial file is valid
    assert os.path.exists(setup_project_yaml), "project.yaml should exist"

    # Perform the repair
    repair_project_config()

    # Load the repaired project.yaml
    with open(setup_project_yaml, 'r') as file:
        config = yaml.safe_load(file)

    # Validate the changes
    assert 'template_version' in config, "template_version should be added"
    assert isinstance(config['dependencies'], dict), "Dependencies should be a dictionary"