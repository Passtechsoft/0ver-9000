from bge import *
import bge.logic as Game
import Utils
from player import Player

def main():
    #those are global variables you can modify for change the behaviour of the game:
    Game.maxDistanceBetPlayers = 25 #The maximal distance between players
    cameraHeight = -1 #Added to the height of the camera

    cam = logic.getCurrentController().owner
    scene = logic.getCurrentScene()
    
    Game.nbrPlayers = 2

    ### CONFIGURE KEYS ###
    
    

    ### CONFIGURE LEVEL ###

    Game.scenePrefix = Utils.getWord(1, cam.name, 0, "_")+"_"

    print("<================= Over 9000: running level \""+Game.scenePrefix+"\" ==================>")

    Game.cameraHeight = cam.position.z - scene.objects[Game.scenePrefix + "spawnPos_p1"].position.z+cameraHeight
    
    ### CONFIGUER PLAYERS ###
    Game.classes = {"player 1" : Player("player 1"), "player 2" : Player("player 2")}
    
    #put the players to their spawn point
    for i in range(1, Game.nbrPlayers+1):
        scene.objects[Game.scenePrefix + "player "+str(i)].position = scene.objects[Game.scenePrefix + "spawnPos_p"+str(i)].position
    
    Game.levelStarted = 1
