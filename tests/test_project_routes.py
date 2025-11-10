import pytest
import os
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config_valid():
    """Test repairing a valid project.yaml."""
    test_file = 'test_project.yaml'
    with open(test_file, 'w') as file:
        yaml.dump({'dependencies': {}}, file)

    result = repair_project_config(test_file)
    
    with open(test_file, 'r') as file:
        config = yaml.safe_load(file)

    assert result is True
    assert 'template_version' in config
    assert config['template_version'] == '1.0.0'
    assert isinstance(config['dependencies'], dict)

    os.remove(test_file)

def test_repair_project_config_invalid_yaml():
    """Test repairing an invalid YAML file."""
    test_file = 'invalid_test_project.yaml'
    with open(test_file, 'w') as file:
        file.write("not: valid: yaml:")

    result = repair_project_config(test_file)
    assert result is False

    os.remove(test_file)