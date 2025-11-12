#!/usr/bin/env python3
"""
Startup script for the project.
This script creates a virtual environment, installs dependencies, and runs the application.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description, check=True):
    """Run a shell command with output."""
    print(f"\n============================================================")
    print(f"{description}")
    print(f"============================================================")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")
        if check:
            sys.exit(1)
        return False

def main():
    """Main startup routine."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║               Project Startup Script                       ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    project_root = Path(__file__).parent
    venv_path = project_root / "venv"
    requirements_file = project_root / "requirements.txt"
    
    # Step 1: Check Python version
    python_version = sys.version.split()[0]
    print(f"✓ Using Python {python_version}")
    
    # Step 2: Create virtual environment if it doesn't exist
    if not venv_path.exists():
        run_command(
            f"{sys.executable} -m venv venv",
            "📦 Creating virtual environment..."
        )
    else:
        print("\n✓ Virtual environment already exists")
    
    # Step 3: Determine pip executable path
    if os.name == 'nt':  # Windows
        pip_executable = venv_path / "Scripts" / "pip.exe"
        python_executable = venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        pip_executable = venv_path / "bin" / "pip"
        python_executable = venv_path / "bin" / "python"
    
    # Step 4: Upgrade pip
    run_command(
        f'"{python_executable}" -m pip install --upgrade pip',
        "⬆️  Upgrading pip..."
    )
    
    # Step 5: Install dependencies
    if requirements_file.exists():
        run_command(
            f'"{pip_executable}" install -r requirements.txt',
            "📥 Installing dependencies from requirements.txt..."
        )
    else:
        print("\n⚠️  No requirements.txt found, skipping dependency installation")
    
    # Step 6: Run the application
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║               Starting Application                         ║
    ╚════════════════════════════════════════════════════════════╝
    
    Running: {"main.py"}
    
    Press Ctrl+C to stop the application.
    """)
    
    try:
        subprocess.run(
            f'"{python_executable}" {"main.py"}',
            shell=True,
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Application exited with error code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
