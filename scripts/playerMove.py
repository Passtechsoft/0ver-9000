from bge import *
import bge.logic as Game

def main():
    player = logic.getCurrentController().owner
    scene = logic.getCurrentScene()

    player1 = scene.objects[Game.scenePrefix + "player 1"]
    player2 = scene.objects[Game.scenePrefix + "player 2"]

    if max(player1.position.x, player2.position.x) - min(player1.position.x, player2.position.x) > Game.maxDistanceBetPlayers:
        player.position.x = player["oldPosition"]
        
    player["oldPosition"] = player.position.x

if hasattr(Game, "levelStarted"):
    if Game.levelStarted == 1:
        main()