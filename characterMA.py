# @ characterMA.py
# Player Character class

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
        self.increased_damage = 1.0 # % damage increase to current attack_damage (currently 100%)
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
        self.increased_damage = 1
        self.defence = 5
    
    # Return if character is still alive
    def isAlive(self):
        return self.alive
    
    # Exp calc
    def gainXP(self, amount):
        
        ''' xp required for level up is 10 times current level'''
        
        self.xp += amount
        if self.xp >= self.level * 10:
            self.levelUp()
         
    # Show character stats
    def status(self):
        print(f'''Name: {'Player'}, Level: {self.level}, XP: {self.xp}/{self.level * 10}, HP: {self.getHP()}, Attack Damage: {self.attack_damage},
               Defence: {self.defence}\n''')
    
    # Character Level up calc       
    def levelUp(self, amount_of_levels):
        
        self.level += amount_of_levels
        
        # Update Player stats
        self.max_hp += amount_of_levels * 10 # Increase player's max hp by 10 per new level
        self.hp = self.max_hp
        self.increase_flat_damage(amount_of_levels * 2) # Increase player attack damage by 2 per new level
        self.base_defence += amount_of_levels # Increase player's base defence by 1 point per new level
        self.reset_defence() # Update player defence to the new value
        print("You are now level: ", self.level)
        self.status()
           
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
                
            print("Current Player HP: ", self.getHP())
        
    # retrieve character hp
    def getHP(self):
        return self.hp
    
    def get_level(self):
        return self.level
    
    # retrieve maximum character hp
    def get_max_hp(self):
        return self.max_hp
    
    def set_max_hp(self, new_max):
        self.max_hp = max(new_max, self.max_hp)
     
    def increase_percent_damage(self, percent_increase:float):
        '''Increases the Increased damage percentage for the player.'''
        self.increased_damage += percent_increase
        self.increase_flat_damage(None)
           
    def increase_flat_damage(self, attack_increase):
        ''' Updates the flat damage value for the character. Attack_increase=None to update base damage after increasing percent damage'''
        if attack_increase is None:
            attack_increase = 0
            
        self.attack_damage = int((self.attack_damage + attack_increase) * self.increased_damage)
            
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
        
        
        