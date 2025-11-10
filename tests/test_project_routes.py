import pytest
import os
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config_valid():
    """Test repairing a valid project.yaml."""
    # Create a mock project.yaml for testing
    with open("project.yaml", "w") as f:
        yaml.dump({"dependencies": {"fastapi": "0.68.0"}}, f)
    
    repair_project_config()

    with open("project.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    assert "template_version" in config
    assert config["template_version"] == "1.0.0"

def test_repair_project_config_missing_dependencies():
    """Test repairing with missing dependencies."""
    with open("project.yaml", "w") as f:
        yaml.dump({}, f)
    
    repair_project_config()

    with open("project.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    assert "template_version" in config
    assert "dependencies" in config
    assert config["dependencies"] == {}

def test_repair_project_config_backup():
    """Test that a backup is created before repairs."""
    if os.path.exists("project.yaml"):
        os.remove("project.yaml")
    
    with open("project.yaml", "w") as f:
        yaml.dump({}, f)

    repair_project_config()
    
    backup_files = [f for f in os.listdir() if f.startswith("project_backup_")]
    assert len(backup_files) > 0