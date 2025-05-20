import os, sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from orchestrators.export_orchestrator import run_massive_exporter

if __name__ == "__main__":
    run_massive_exporter()
