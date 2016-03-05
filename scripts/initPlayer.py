from bge import *
import bge.logic as Game
import Utils

player = logic.getCurrentController().owner
cont = logic.getCurrentController()

def main():
    player["class"] = Game.classes[Utils.getWord(1, player.name, 0, "_")]
    #cont.sensors["Left"].key = 
    player["checked"] = 1
    

if hasattr(Game, "levelStarted"):
    if Game.levelStarted == 1:
        if "checked" in player:
            f = 0
        else:
            main()