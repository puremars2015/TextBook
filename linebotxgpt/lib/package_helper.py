import subprocess
import sys

def install_package(package_name):
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")