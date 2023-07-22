# @ characterMA.py
# This is the character class for the game
############################## Work in progress ####################################

class Character:
    
    def __init__(self) -> None:
        self.max_hp = 10.0
        self.hp = 10.0
        self.level = 1
        self.xp = 0
        self.spirit = 10
        self.alive = True
        self.attack_value = 1.0
        self.defence_value = .3
        
    def reset_character(self):
        self.max_hp = 10.0
        self.hp = 10.0
        self.level = 1
        self.xp = 0
        self.spirit = 10
        self.alive = True
        self.attack_value = 1.0
        self.defence_value = .3
         
    # Return if character is still alive
    def isAlive(self):
        return self.alive
    
    # Exp calc
    def gainXP(self, amount):
        self.xp += amount
        if self.xp >= self.level * 10:
            self.levelUp()
         
    # Show character stats
    def status(self):
        print(f'''Name: {self.name}, Level: {self.level}, XP: {self.xp}/{self.level * 10}, HP: {self.getHP()}, 
                  Stamina: {self.stamina}, Spirit: {self.spirit}\n''')
     
    # Character Level up calc       
    def levelUp(self):
        self.level += 1
        print("You are now level: ", self.level)
           
    # Kill character if status is false, returns isAlive status
    def death(self):
        self.alive = False
    
    # Update character hp
    def updateHP(self, dmg_taken):
        
        if dmg_taken is not None:
            print("Dmg taken: ", dmg_taken)
            self.hp -= dmg_taken
            
            if self.hp <= 0.0:
                self.death()
                
            print("Current HP: ", self.getHP())
        
    # retrieve character hp
    def getHP(self):
        return self.hp
    
    # retrieve maximum character hp
    def get_max_hp(self):
        return self.max_hp
    
    def set_max_hp(self, new_max):
        self.max_hp = max(new_max, self.max_hp)
        