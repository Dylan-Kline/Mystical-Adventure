# @ combatMA.py
# This is the combat class for the game
import random
from characterMA import Character

class Combat:
    
    def __init__(self, character, monster) -> None:
        
        # Player variables
        self.player = character
        self.player_action = None
        
        # Opponent variables
        self.opponent = monster
        self.opponent_action = None
        
    def calc_dmg(self, attacker, defender):
        
        if self.attacker == self.player and self.opponent_action != "Defend":
            dmg_taken = attacker.attack_value
        
        elif self.attacker == self.opponent and self.player_action != "Defend":
            dmg_taken = attacker.attack_value
            
        elif self.attacker == self.player:
            dmg_taken = attacker.attack_value * defender.defence_value
            print("Opponent defended")
            
        else:
            dmg_taken = attacker.attack_value * defender.defence_value
            print("Player defended")
        
        return dmg_taken
        
    def initiate_combat(self):
        
        if self.player.isAlive() and self.opponent.isAlive() and self.player_action != 'Flee':
            
            self.determine_opponent_action()
            
            # Player's turn
            player_dmg = self.calc_dmg(self.player, self.opponent)   
            self.opponent.updateHP(player_dmg)
            print(f"The player does {player_dmg} damage to the monster.")
          
            # Opponent's turn   
            opponent_dmg = self.calc_dmg(self.opponent, self.player)
            self.player.updateHP(opponent_dmg)
            print(f"Opponent does {opponent_dmg} damage to player.")
            
        else:  
            
            # If player decides to flee
            return 0
    
    def determine_opponent_action(self):
        
        random_val = random.randint(0, 10)
        
    def set_player_action(self, action):
        self.player_action = action
        

#------------------------ Ideas for combat scenes and the destruction trial combat in particular ----------------------------#     
        
# Have this class be connected to the combat scene that will be used throughout the game for the boss battles and minions.
# you can have it so the player can flee in minion battles but not boss battles, 
# the scene tranisitions back to the scene used to initiate combat if the player does decide to do so. Then I need to delete the
# option used to enter combat so the player can no longer gain the rewards from defeating the monster.
# Though I will need to figure out how to allow the player to continue through the forest. Or maybe not since if they choose to flee
# in the first place then they are most likely either dumb and low hp and can no longer fight. In this case for the destruction trial
# the player will be missing the extra chance gained from fighting abyssal mobs, and therefore will have a chance to die from the rune
# energy destroying them from within. 
            