import subprocess
import sys

# List of libraries to install
libraries_to_install = [
    'tqdm',
    'scipy',
    'soundfile',
    'numpy',
]

def install_libraries():
    print("Installing required libraries...")
    for library in libraries_to_install:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
            print(f'{library} installed successfully')
        except subprocess.CalledProcessError:
            print(f'Error installing {library}. Continuing with next library...')
            continue

    # Check standard modules
    print("\nChecking standard modules:")
    std_modules = ['tkinter', 'webbrowser', 'shutil', 'os', 're', 'threading']
    for module in std_modules:
        try:
            __import__(module)
            print(f'{module} available (standard module)')
        except ImportError:
            print(f'ERROR: {module} not found (should be part of Python)')

if __name__ == "__main__":
    install_libraries()
