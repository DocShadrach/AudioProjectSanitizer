import subprocess

# List of libraries to install
libraries_to_install = [
    'tqdm',
    'scipy',
    'soundfile',
    'numpy',
]

for library in libraries_to_install:
    try:
        subprocess.check_call(['pip3', 'install', library])
        print(f'{library} installed successfully')
    except subprocess.CalledProcessError:
        print(f'Error installing {library}. Continuing with the next library...')
        continue

# Check if are available

try:
    import tkinter
    print('tkinter is already available.')
except ImportError:
    print('tkinter is not available. Installing...')
    subprocess.check_call(['pip3', 'install', 'tkinter'])
    print('tkinter installed successfully.')

try:
    import webbrowser
    print('webbrowser is already available.')
except ImportError:
    print('webbrowser is not available. Installing...')
    subprocess.check_call(['pip3', 'install', 'webbrowser'])
    print('webbrowser installed successfully.')

try:
    import shutil
    print('shutil is already available.')
except ImportError:
    print('shutil is not available. Installing...')
    subprocess.check_call(['pip3', 'install', 'shutil'])
    print('shutil installed successfully.')
