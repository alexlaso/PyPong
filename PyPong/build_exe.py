import PyInstaller.__main__

PyInstaller.__main__.run([
    'pong.py',
    '--onefile',
    '--windowed',
    '--name',
    'PyPong',
    '--clean'
])