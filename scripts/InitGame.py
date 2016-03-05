#This file should be run only once per game session.
from bge import *
import bge.logic as Game
import Utils
import defaultKeys as DKeys

def main():
    if hasattr(Game, "gameStarted"):
        return
    Game.gameStarted = 1
    Game.nbrePlayers = 2

    cam = logic.getCurrentController().owner

    # If you want to make your own properties and global variables, follow those advices:
        #If your propertie is related to a player, wrote for example "p1." for player 1 in first
        #Then, add your personnal sub-sections

    ### READING CONFIG FILE ###

    config_file_path = cam["config_file_path"]

    inFile = open(config_file_path, "r")

    fileContent = inFile.read()
    b = fileContent.split("\n")# Creating a iterable version of the file
    DKeys.initDefKeys()
    #We set up the key table
    Game.keys = {}

    for i in b:
        if len(i) == 0:
            continue
        
        keyWord = Utils.getWord(0, i) # The index of the value
        value = Utils.getWord(2, i)
        
        # We check if the file synthax isn't broken
        if Utils.getWord(1, i) != "=":
            print("syntaxe du fichier abimée, relisez vous didiou!")
            break
        
        y=0 # The actual level in the value
        
        # Looking if the key is reafering to a player
        if Utils.getWord(0, keyWord, 0, ".")[0] == "p":
            s = "player "+Utils.getWord(0, keyWord, 0, ".")[1] # Searching for the layer number.
            y += 1
            
        # Searching the first modifier
        first = Utils.getWord(y, keyWord, 0, ".")
        
        if first == "key":
            Game.keys[keyWord] = Utils.strToEvent(value) 

    #Check the keys, replace the missing keys by the default keys
    print("==========================================\n")
    for i in range(1, Game.nbrePlayers+1):
        connerie = []
        for c in Game.keys:
            connerie.append(Utils.getWord(2,c,0,"."))
        for c in Game.keys:
            if Utils.getWord(0, c, 0, ".") == "p"+str(i):
                cptr = 0
                for d in Game.minKeys:
                    if d in connerie:
                        cptr+=1
                    else:
                        break
                if cptr != len(Game.minKeys):
                    print("Warning!!! Some keys are undefined for player "+str(i))
                    Game.keys[c] = Game.defaultKeys[Utils.getWord(2,c,0,".")]
    print("==========================================\n")
    import initLevel

    initLevel.main()