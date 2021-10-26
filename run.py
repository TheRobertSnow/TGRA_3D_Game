from src.main import FpsGame
from src.essentials.settings import MODES, GAMER_MODE
import sys

if __name__ == ("__main__"):
    mode = GAMER_MODE
    argv = sys.argv
    if len(argv) > 1:
        if argv[1] == '-m':
            if argv[2] in MODES:
                mode = argv[2]
            else:
                print("Error: Wrong run option")
                exit()
    game = FpsGame(mode).start()