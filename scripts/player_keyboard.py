from bge import *
import bge.logic as Game
import Utils
import initPlayer


player = Game.getCurrentController().owner

def main():
    player["class"].update()
        
if hasattr(Game, "levelStarted") and "checked" in player:
    if Game.levelStarted == 1:
        main()