#!/usr/bin/python3

class Character:
    def __init__(self, user):
        self.user = user # Discord user object (display_name, name, id, mention, etc)
            
        self.health = 100
        self.rage = 0
        self.role = None
        self.invulnerable= False
        self.gm = False
        self.cover = None

    def isAlive(self):
        if(self.health > 0):
            return True
        else:
            return False
    def isDead(self):
        if(self.health == 0):
            return True
        else:
            return False
            
    def isInvulnerable(self):
        if(self.invulnerable):
            return True
        else:
            return False

    def isGameMaster(self):
        if(self.gm == True):
            return True
        else:
            return False

