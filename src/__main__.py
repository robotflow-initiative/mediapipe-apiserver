import sys
sys.path.append('./')
from src.cmd.main import entrypoint

if __name__ == '__main__':
    # sys.argv.append('serve') # for testing purpose
    entrypoint()