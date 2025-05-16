import os, sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from orchestrators.outlet_orchestrator import run_outlet_manager

if __name__ == "__main__":
    run_outlet_manager()