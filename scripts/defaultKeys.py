from bge import *
import bge.logic as Game
import Utils

def initDefKeys():
    minKeys = "left right jump spe1 spe2 spe3 spe4 spe5 spe6"
    Game.minKeys = minKeys.split(" ")

    Game.defaultKeys = {}

    Game.defaultKeys["left"] = Utils.strToEvent("Q")
    Game.defaultKeys["right"] = Utils.strToEvent("D")
    Game.defaultKeys["spe1"] = Utils.strToEvent("S")
    Game.defaultKeys["spe2"] = Utils.strToEvent("Z")
    Game.defaultKeys["spe3"] = Utils.strToEvent("A")
    Game.defaultKeys["spe4"] = Utils.strToEvent("E")
    Game.defaultKeys["spe5"] = Utils.strToEvent("G")
    Game.defaultKeys["spe6"] = Utils.strToEvent("C")
    Game.defaultKeys["jump"] = Utils.strToEvent("space")
