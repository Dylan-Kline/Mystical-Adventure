# @ combatMA.py
# This is the combat class for the game
import random
import math
from characterMA import Character

class Combat:
    
    def __init__(self, character:Character, monster) -> None:
        
        # Player variables
        self.player = character
        self.player_action = None
        self.previous_player_action = None
        
        # Opponent variables
        self.opponent = monster
        self.opponent_action = None
        self.opponent_max_attacks = None # the number of attacks the monster will perform before defending
        self.opponent_current_attacks = None # the current number of attacks left before the monster defends
        
        #if isinstance(monster, Wolf):
            
    
    def attack(self, attacker, target):
        
        # Determine whether attack lands
        hit_chance = random.random()
        if hit_chance < attacker.miss_chance:
            print("Attack Missed")
            return 0
        
        # Determine if player has hit a critical strike
        if attacker == self.player:
            critical_chance = random.random()
            if critical_chance <= 0.3:
                critical_multi = 0.2
            else:
                critical_multi = 0.0
        
        # Counterattack scenario where both combatants attack (halves the damage they deal/take)
        if self.player_action == 'Attack' and self.opponent_action == 'Attack':
            damage_dealt = attacker.attack_damage // 2
        else:
            damage_dealt = attacker.attack_damage
            
        # Apply critical damage multiplier to player damage after dmg calcs
        if attacker == self.player: damage_dealt += int(damage_dealt * critical_multi)
            
        return self.defend(target, damage_dealt)
        
    def defend(self, defender, damage_taken):
        
        actual_dmg = max(0, damage_taken - defender.defence)
        defender.updateHP(actual_dmg)
        return actual_dmg
    
    def special_combat_effects(self):
        pass
        
    def initiate_combat(self):
        
        """
        returns: 0 for player death, 1 for player victory, 2 for player fleeing
        """  
        if self.player.isAlive() and self.opponent.isAlive() and self.player_action != 'Flee':
            
            self.determine_opponent_action()
            
            # Player's turn
            if self.player_action == "Defend":
                # If the player defends consecutively, decrease their defence
                if self.previous_player_action is not None and self.previous_player_action != 'Defend':
                    self.player.temp_buff_defence(2)
                else:
                    self.player.temp_buff_defence(-1)
                    
                player_dmg = 0
            else:
                if self.opponent_action == "Defend":
                    self.opponent.temp_buff_defence(2)
                player_dmg = self.attack(self.player, self.opponent)
                
            print(f"The player does {player_dmg} damage to the monster.")
            print(f"Player defended: Current defence {self.player.defence}")

            # If monster dies after player's turn
            if not self.opponent.isAlive():
                return 1

            # Opponent's turn   
            if self.opponent_action == "Attack":
                opponent_dmg = self.attack(self.opponent, self.player)
                print(f"Monster does {opponent_dmg} damage to player.")
                
            
            print(f"Monster defence: {self.opponent.defence}")
            if not self.player.isAlive():
                return 0
            
        else:  
            # If player decides to flee reset their defense to pre-buff value and full heal their hp
            if self.player_action == 'Flee':
                self.player.reset_defence()
                self.player.full_heal()
                return 2
            else:
                return 0
            
    def determine_opponent_action(self):
        
        decision_value = random.randint(0, 10)
        
        if decision_value in range(0, 10, 2):
            self.opponent_action = "Defend"
        else:
            self.opponent_action = "Attack"
            
        print(self.opponent_action)
        
    def set_player_action(self, action):
        self.previous_player_action = self.player_action
        self.player_action = action
        

            