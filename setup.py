import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == '__main__':
    install('Pillow')
    install('html5lib')
    install('requests')
    install('beautifulsoup4')
    install('fuzzywuzzy')
    install('soundex')
    install('chatterbot==1.0.4')
