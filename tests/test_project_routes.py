import pytest
import os
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config_valid_yaml(monkeypatch):
    # Setup
    test_project_yaml = {
        'dependencies': {'fastapi': '0.104.1'},
    }
    with open('project.yaml', 'w') as f:
        yaml.safe_dump(test_project_yaml, f)

    # Mock templates.json existence
    monkeypatch.setattr(os, 'path.exists', lambda x: x == 'templates.json')
    with open('templates.json', 'w') as f:
        json.dump({'template_version': '1.0.1'}, f)

    # Act
    repair_project_config()

    # Assert
    with open('project.yaml', 'r') as f:
        config = yaml.safe_load(f)
    assert config['template_version'] == '1.0.1'
    assert config['dependencies'] == {'fastapi': '0.104.1'}

def test_repair_project_config_missing_version(monkeypatch):
    # Setup
    test_project_yaml = {
        'dependencies': {'fastapi': '0.104.1'},
    }
    with open('project.yaml', 'w') as f:
        yaml.safe_dump(test_project_yaml, f)

    # Act
    repair_project_config()

    # Assert
    with open('project.yaml', 'r') as f:
        config = yaml.safe_load(f)
    assert config['template_version'] == '1.0.0'