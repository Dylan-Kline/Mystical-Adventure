# @ characterMA.py
# This is the character class for the game
############################## Work in progress ####################################
from inventoryMA import Inventory

class Character:
    
    def __init__(self) -> None:
        
        # Character HP
        self.max_hp = 100
        self.hp = 100
        
        # Character Inventory
        self.inventory = Inventory(25)
        
        # Character level and xp
        self.level = 1
        self.xp = 0
        
        self.miss_chance = .1 # 10% chance to miss attack
        self.attack_damage = 25  # Attack Damage
        self.defence = 5 # Defence is how much damage the character can block from one attack
        self.base_defence = 5 # Base defence value
        
        # Live status for character
        self.alive = True
        
    def reset_character(self):
        del self.inventory
        self.inventory = Inventory(25)
        self.max_hp = 100
        self.hp = 100
        self.level = 1
        self.xp = 0
        self.miss_chance = .1
        self.alive = True
        self.attack_damage = 25
        self.defence = 5
    
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
            
            if self.hp <= 0:
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
        
    def increase_damage(self, attack_increase):
        self.attack_damage += attack_increase
        print("New damage: ", self.attack_damage)
        
    def get_attack_damage(self):
        return self.attack_damage

    def full_heal(self):
        self.hp = self.max_hp
        
    def temp_buff_defence(self, buff_value):
        ''' Buffs player defence for the duration of the battle'''
        self.defence += buff_value
        
    def reset_defence(self):
        self.defence = self.base_defence
        
        
        