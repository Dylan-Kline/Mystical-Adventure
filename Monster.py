# @Monster.py
# Wolf monster class for destruction trial scene in @ScenesMA.py

class Monster:
    
    def __init__(self, mtype:str, max_hp:int, miss_chance:float, attack_damage:int, defence:int) -> None:
        
        self.monster_type = mtype
        
        # Monster HP
        self.max_hp = max_hp
        self.hp = self.max_hp
        
        # Combat variables #
        self.miss_chance = miss_chance # 10% chance to miss attack
        self.attack_damage = attack_damage # Attack Damage
        self.increased_damage = 1.0 # % damage increase to current attack_damage (currently 100%)
        self.defence = defence # Defence is how much damage the character can block from one attack
        self.base_defence = self.defence # Base defence value
        
        # Live status for monster
        self.alive = True
        
    # Return if character is still alive
    def isAlive(self):
        return self.alive
        
    # Show character stats
    def status(self):
        print(f'''Name: {self.monster_type}, Level: {self.level}, XP: {self.xp}/{self.level * 10}, HP: {self.getHP()}, Attack Damage: {self.attack_damage},
               Defence: {self.defence}\n''')
         
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
        
    def get_attack_damage(self):
        return self.attack_damage
    
    def temp_buff_defence(self, buff_value):
        ''' Buffs monster defence for the duration of the battle'''
        self.defence += buff_value
        
    def reset_defence(self):
        self.defence = self.base_defence