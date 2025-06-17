"""
Script to run integration tests for the Statistics Service
"""

import os
import sys
import subprocess

def run_integration_tests():
    """Run integration tests with proper configuration"""
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/integration_tests/test_integration_statistics.py',
        '-v',
        '--tb=short',
        '-c', 'pytest_integration.ini'
    ]
    
    print("Running integration tests for Statistics Service...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("-" * 60)
        print("All integration tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print("-" * 60)
        print(f"Integration tests failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
