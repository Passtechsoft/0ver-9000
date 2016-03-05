from bge import *
import Utils
import bge.logic as Game
from math import *

def getKeyProp(playerName, propName):
    return Game.keys["p"+Utils.getWord(1, playerName)+".key."+propName]

def checkKeyboard(keyCode):
    return logic.KX_INPUT_ACTIVE == keyboard.events[keyCode]

class Player:
    
    def __init__(self, player="player 1", name = "Jostophe"):
	self.create(player, name)
        
    def create(self, player, name):
        self.name = name
        self.className = "default"
        self.player = player # player 1 or player 2
        self.prefix = "p" + Utils.getWord(1,player)
        
        #argument, life and mana:
        self.argumentNbr = 3
        
        self.default_life = 100
        self.default_mana = 100
        self.default_argument = 100
        
        self.life = 100
        self.mana = 100
        self.argument = 100
        
        self.old_life = 100
        self.old_mana = 100
        self.old_argument = 100
        
        #some class related properties:
        self.hitPower = 10
        self.jumpForce = 20
        self.doubleJump = 0
        
        self.waitKey = 1000000
        self.beHit = 1
            
        self.className = "default"
            
        self.tmpCombo = [] # A integrer table storing the actuall key strokes    
        self.cPowers = {"Z,S:Z,S", "S,space,S,S", "Z,Z", "Z,S,Z,S"}
        self.cCPowers = [[],[],[],[]]
        self.cPowerCheck = [0, 0, 0, 0]
        self.dPower = 30 # implement later 
        self.cUltimate = "Z,Z:S,Z:space,space"# The ultimate combo
        self.dUltimate = 300
        
        self.compileCPower()
        self.updateLifeBar()
        
    #Called when changes are made to CPower
    def compileCPower(self):
        #Here we convert the absolute Keys cPower into keys relative to the actual player
        for cp, i in enumerate(self.cPowers):
            for cptr, v in enumerate(i):
                tmp = str()
                if v == ",":
                    continue
                if v == ":":
                    self.cCPowers[cp].append(666)
                    continue
                    
                if v == "Z":
                    self.cCPowers[cp].append( getKeyProp(self.player, "spe1"))
                elif v == "S":
                    self.cCPowers[cp].append( getKeyProp(self.player, "spe2"))
                elif v == "A":
                    self.cCPowers[cp].append( getKeyProp(self.player, "spe3"))
                elif v == "E":
                    self.cCPowers[cp].append( getKeyProp(self.player, "spe4"))
                elif v == "G":
                    self.cCPowers[cp].append( getKeyProp(self.player, "spe5"))
                elif v == "C":
                    self.cCPowers[cp].append( getKeyProp(self.player, "spe6"))
                elif v == "s":
                    if len(i) > cptr+3:
                        if v+i[cptr+1]+ i[cptr+2]+i[cptr+3] == "space":
                            self.cCPowers[cp].append( getKeyProp(player, "space"))
                    else:
                        print("Warning!!! in Player::CompileCPower, unknown key "+v+", input ignored")
                elif v == "p" and i[cptr-1] == "s" or v == "a" and i[cptr-1] == "p" or v == "c" and i[cptr-1] == "a" or v == "e" and i[cptr-1] == "c":
                    continue
                elif v == "Q":
                    self.cCPowers[cp].append(getKeyProp(self.player, "left"))
                elif v == "D":
                    self.cCPowers[cp].append(getKeyProp(self.player, "right"))
                else:
                    print("Warning!!! in Player::CompileCPower, unknown key"+v+", input ignored")
        print("cCpower for "+self.player+":")
        for i in self.cCPowers:
            print(i)
            
    def update(self):
        ###Checking keyboard:
        scene = Game.getCurrentScene()
            
        keyboard = Game.keyboard
        
        sensor = Game.getCurrentController().sensors["collision joueur"]
        if self.waitKey >= 10:
            
            if logic.KX_INPUT_ACTIVE == keyboard.events[Game.keys[self.prefix+".key.left"]]:
                self.checkAttacks(Game.keys[self.prefix+".key.left"])
            if logic.KX_INPUT_ACTIVE == keyboard.events[Game.keys[self.prefix+".key.right"]]:
                self.checkAttacks( Game.keys[self.prefix+".key.right"])
            if sensor.positive: # collision
                if logic.KX_INPUT_ACTIVE == keyboard.events[Game.keys[self.prefix+".key.spe1"]]:
                    self.checkAttacks( Game.keys[self.prefix+".key.spe1"])
                    player = Game.getCurrentController().owner
                    if self.player == "player 1":
                        self.hitEnemy("player 2", self.hitPower)
                    elif self.player == "player 2":
                        self.hitEnemy("player 1", self.hitPower)
                    self.waitKey = 0
        else:
            self.waitKey += 1
        if self.waitKey == 0:
            print("WAIT KEY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    def hitEnemy(self, playerName, power):
        scene = Game.getCurrentScene()
        self.beHit = 0
        if self.argument <= 0:
            if self.beHit == 0:
                if self.argumentNbr >= 0:
                    self.argument = self.default_argument
        scene.objects[ Game.scenePrefix+playerName]["class"].attack(power)
        self.updateLifeBar()
        
    #called by the enemy, this function substract the attackPower amount of life from argument or life bar
    def attack(self, attackPower):
        print("attack:::  "+str(self.life)+" ::::: "+str(self.argument))
        
        if self.argument > 0:
            self.argument -= attackPower
            suppMnlife = 0
            if self.argument < 0:
                self.life -= abs(self.argument)
                self.argument = 0
        else:
            self.life -= attackPower
        
        if self.argument <= 0:
            print("BEHIT!!!!! :  "+str(self.beHit)+" :: " + str(self.argumentNbr))
            if self.old_argument > 0:
                self.argumentNbr -= 1
            elif self.beHit == 0:
                if self.argumentNbr >= 0:
                     self.argument = self.default_argument
        
        self.beHit = 1
        self.updateLifeBar()
        
    def checkAttacks(self, char):
        print("checkCombo!!!"+str(self.checkCombo(char)))
        #if checkKeyboard(Game.keys[self.prefix+".key.left"])
        
    #Called when a key is pressed, check if there is a combo
    def checkCombo(self, char):
        print(char)
        checkCombos = 0
        returnTrue = 0
        
        for cptr, i in enumerate(self.cCPowers):
	    #If the current key is the combo, we just play it
            if i == self.tmpCombo+char:
                returnTrue = 1
                self.power(cptr)
	    #if we are in te way to complete a combo
            else:
		checker = 1
		for tr, co in enumerate(self.tmpCombo):
		    if co != i[tr]:
			checker = 0
		if checker == 1:
		    self.cPowerCheck[cptr] += 1
		    checkCombos = 1
        
        
        if self.cUltimate == tmpCombo+char:
            checkCombo = 1
            self.ultimate()
	else:
	    checker = 1
	    for tr, co in enumerate(self.tmpCombo):
		if co != cUltimate[tr]:
		    checker = 0
	    if checker == 1:
		checkCombo = 1
	      
        if checkCombo == 0:
            self.tmpCombo = []
        self.updateLifeBar()
        return returnTrue

    #Called to apply a power-effect
    def power(self, nbr, target):
        print("F-F-F-F-FATALITY!")
        print("power "+str(nbr)+" to "+target.name)

    #Called to apply the ULTIMATE effect
    def ultimate(self, target):
        print("U-U-U-Ulitimate from "+player+" to "+target.name+" with love <3")

    #called when the life has been changed
    def updateLifeBar(self):
        scene = Game.getCurrentScene()
        # You will die potato!
        if self.life <= 0:
            print("Life of "+self.player+" life reach 0 !!!")
            if self.player == "player 1":
                scene.objects["Camera_"+ Utils.getWord(0,Game.scenePrefix,0,"_")]["winner"] = "player 2"
            else:
                scene.objects["Camera_"+ Utils.getWord(0,Game.scenePrefix,0,"_")]["winner"] = "player 1"
                
        #scene.active_camera = scene.objects["CAMERANAME"]
        overLayScene = Game.getSceneList()[1]
        
        #applying the amount of argument on the argument bar & shields:
        if self.old_argument <= 0 and self.argument == self.default_argument:
            overLayScene.objects["player 2_argument_bar_hide"].playAction(self.player+"_argument_action", 0, 20)
        else:
            limit = overLayScene.objects[self.player+"_limite_jauge_argument"].position.z
            overLayScene.objects[self.player+"_argument_bar_hide"].position.z = self.argument/self.default_argument * (overLayScene.objects[self.player+"_base_jauge_argument"].position.z-limit)+limit
        
        for i in range (1,4):
            ob = overLayScene.objects[self.player+"_argument "+str(i)]
            if self.argumentNbr < i and ob.position.z < overLayScene.objects[self.player+"_position_default_argument"].position.z+10:
                overLayScene.addObject(overLayScene.objectsInactive["broken shield"], ob, 60)
                ob.position.z += 40
            elif self.argumentNbr >= i:
                ob.position.z = overLayScene.objects[self.player+"_position_default_argument"].position.z
            
        #applying the amount of life on the life bar:
        lifeQuarters = self.default_life/6
        remainingQuarters = ceil(self.life/self.default_life*6)
        print(" !! remaining quarters: "+str(remainingQuarters))
        for i in range(1,7):
            ob = overLayScene.objects[self.player+"_slot vie "+str(i)]
            ref = overLayScene.objects[self.player+"_life_position"]
            if ob.position.z >= ref.position.z + 10:
                if remainingQuarters >= i:
                    ob.position.z = ref.position.z
            elif ob.position.z < ref.position.z + 10:
                if remainingQuarters < i:
                    for y in range(1,9):
                        overLayScene.addObject( overLayScene.objectsInactive["explode_life_"+str(y)], ob, 30)
                    ob.position.z += 20
        self.old_life = self.life
        self.old_mana = self.mana
        self.old_argument = self.argument
                        

#class PyroBarbare : Player