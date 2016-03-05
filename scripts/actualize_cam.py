from bge import *
import bge.logic as Game

def main():
    cam = logic.getCurrentController().owner

    scene = logic.getCurrentScene()

    cam.position.z = (scene.objects[Game.scenePrefix+"player 1"].position.z + scene.objects[Game.scenePrefix+"player 2"].position.z)/2 + Game.cameraHeight

    cam.position.x = (scene.objects[Game.scenePrefix+"player 1"].position.x + scene.objects[Game.scenePrefix+"player 2"].position.x)/2

if hasattr(Game, "levelStarted"):
    if Game.levelStarted == 1:
        main()