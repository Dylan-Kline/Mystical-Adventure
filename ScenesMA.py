import pygame
import random
import numpy as np
import math
from characterMA import Character
from utilitiesMA import Clickable_text
from combatMA import Combat

# Current to do list:
# - Make monster classes for combat scenes
# - later on fine tune the combat values to make it fair (tweaked the combat system to include more variety,
#   now I need to create each monster class and adjust their attack/defence values and include their attack patterns
#   in determine_opponent_action() in @combatMA.py
# create final boss fight (the porci trial of pine)
# Add background music to the game

class Scene:
    
    # File path for font library
    Haseyo_font = "Fonts\\AnnyeongHaseyo.ttf"
    default_font = None
    
    # Image path for UI
    dialogueBox = pygame.image.load('images/UI-textbox.png')
    scaled_dialogueBox = pygame.transform.scale(dialogueBox, (1456, 816))
    
    # Image paths for scenes
    loadScreen = pygame.image.load('images/start-screen.png')
    startButton = pygame.image.load('images/start-button.png')
    temple_entrance = pygame.image.load('images/temple-entrance.png')
    leaving_image = pygame.image.load('images/cowards-path.png')
    trial_gate = pygame.image.load('images/trial-gate.png')
    platform = pygame.image.load('images/trial1-portals.png')
    wisdom_trial = pygame.image.load('images/wisdom-dragon.png')
    destruction_trial = pygame.image.load('images/rune-of-destruction.png')
    cave_skeleton = pygame.image.load('images/cave-skeleton.png')
    
    # Surface variable
    surface = None
    
    dialogue = {
        "temple":
            {
                'prompt':"Venturing on your first adventure beyond the confines of the sect, you stumble upon an eerie, abandoned temple." +
                            " Moss and vines crawl along its surfaces, and a heavy air of mysticism and antiquity weighs upon your" +
                            " shoulders. The silent call of adventure compels you forward.",
                'examine':" Your gaze wanders from the temple to the vibrant life that surrounds it. You find yourself immersed in a dense jungle," +
                            " a verdant maze of towering trees and bamboo clusters that reach for the heavens, their leaves whispering secrets of " +
                            "ancient times. In the distance, an immense mountain looms, its peak veiled in emerald foliage that appears almost like" +
                            " a crown under the ever-changing sky.",
                'options':['Enter the temple', 'Examine the surroundings', 'Leave back to the sect']
            },
        "coward":
            {
                'prompt':"As you stand on the path back to the sect, you hear a distant voice resounding through your mind." +
                         " 'Everything you wish to accomplish is on the other side of fear.'",
                'pondering':"You pause upon the path towards your sect, your heart heavy with the weight of indecision." +
                            " As you stand there, the surroundings seem to hold their breath, allowing you a moment of introspection." +
                            " The path back to the sect beckons, offering comfort and familiarity, while the path towards the temple " +
                            "promises the unknown, challenges, and the potential for cultivation growth.",
                'options':['Summon your courage and turn back to the temple.', 'Continue along the path to the safety of your sect...', 
                           "Pause and reflect upon the mysterious voice's words."]
            },
        "gate":
            {
                'prompt':"You step inside, and before you looms a dreadful temple archway radiating a foreboding red glow. " +
                            "Sinister carvings of demonic creatures adorn the surroundings, and ancient etchings line the temple pillars." +
                            " The rumors among your sect members were right, the trial grounds of the abyss truly exist. As you walk further inside" +
                            " the sound of the entrance slamming shut echos from behind, you are now trapped.",
                'examine':"The etchings adorning the abyssal temple archway depict a haunting tapestry of ancient symbols and twisted patterns," +
                            " seemingly carved by the claws of abyssal creatures. Intricate and foreboding, the etchings exude an aura of primal"+
                            " power and enigmatic purpose. Each stroke reveals a glimpse into the unfathomable depths of the abyss, " +
                            "as if warning those who dare to tread within of the perilous trials that lie ahead.",
                'escape':"You quickly turn around to examine the now shut entrance, the faint orange glow of an array formation covers your only way out. " +
                            "You attempt to find a way to the open the formation, however as you get close your sense of danger screams at you. " +
                            "Quickly backing away, you turn towards your only way out...the mysterious archway.",
                'options':['Enter the archway regardless of the potential danger...', 'Examine the etchings', 'Attempt to open the door and leave', 'Continue']
  
            },
        "trial1": 
            {
                'prompt':"Entering the archway, you find a descending staircase that guides you into the depths of darkness." +
                            " As you venture downwards, a faint purple glow emerges, casting an eerie light on path ahead. " +
                            "Reaching the bottom of the stairs, you are immediately confronted with two massive portals, pulsating with an " +
                            "eerie, etheral glow. There are intricate carvngs depicting wisdom on the left portal, and" +
                            " destruction on the right.",
                'voice':"Abruptly, a deep almost demonic voice sounds out within your mind. \n" +
                            "'Welcome, potential inheritor of the abyss. The Trials await, where destiny and power intertwine. " +
                            "Choose your path wisely, for within each portal lies the path to ascendance or oblivion.'",
                'options':['Wisdom', 'Destruction']
            },
        "wisdom portal":
            {
                'prompt':"As you pass through your portal of choice, the world transforms around you. " +
                            "A breathtaking landscape unfolds, adorned with stunning red trees that seem to glow with an otherworldly radiance. " +
                            "The air is filled with the gentle sound of flowing water, drawing your attention to the serene waterfall ahead. " +
                            "Amidst this serene setting, a colossal draconic demon beast looms, dwarfing the old temple beside it." +
                            " Its imposing form exuding an aura of ancient knowledge and profound enlightenment.",
                            
                'beast':["Welcome, young mortal cultivator, to your first trial. Within this realm of wisdom and enlightenment, you shall" +
                         " face a series of questions that delve deep into the essence of your very being. " +
                         "Do well to offer answers that carry the weight of profound contemplation, for they" +
                         " will shape not only the outcome of this trial but also your very fate." +
                         " *The age-old demon beast reveals a sinister grin as his ominous words echo throughout the valley*" +
                         " Shall we begin?",
                         "Well done mortal, you have traversed the depths of wisdom and emerged victorious. " +
                         "Your answers have demonstrated a profound understanding of the intricate balance between power and enlighenment." +
                         " The abyss acknowledges your wisdom and rewards you accordingly. " +
                         "May this triumph serve as a testament to your potential and ignite the flame of your journey." +
                         " Yet, remember that the true test lies ahead. So prepare yourself well mortal, for the trials ahead" +
                         " hold greater danger, but equally greater rewards.",
                         "You've truly disappointed me mortal...it seems your cultivation is wasted on you. " +
                         "*the age-old demon beast growls these words at you as it draws closer until...CHOMP* " +
                         " Ah...it seems this time's challenger is a failure as well, at least they can serve to further the abyss" +
                         " in another way."],
                            
                'options':['Power through the dreadful atmosphere and use it to temper your soul.', 'Head back through the portal.'],
                
                'questions':['What defines true strength: the ability to destroy or the ability to protect?', 
                             "Can true enlightenment be achieved without facing the depths of one's own inner darkness?",
                             "In the pursuit of immortality, what is the greatest sacrifice one must be willing to make?"],
                
                'answers':["True strength lies in the ability to wield destructive force.",
                           "The mark of true strength is the ability to protect and nurture.",
                           "Strength is defined by one's ability to adapt to any situation.",
                           "True enlightenment comes from transcending darkness, not facing it.",
                           "Facing one's inner darkness is a necessary step towards true enlightenment.",
                           "Enlightenment can be achieved through various paths, darkness being just one of them.",
                           "One must be willing to sacrifice personal relationships",
                           "To relinquish one's humanity, embracing a path of detachment and isolation.",
                           "Rid oneself of worldy desires and ambitions."]
                
            },
        "destruction portal":
            {
                'prompt':[
                            "Entering the portal you find yourself within a desolate forest full of colossal trees. " +
                            "In the distance floats a mysterious rune shard that radiates what feels like pure destruction. " +
                            "You quickly deduce that it's a law shard that would allow you to comprehend the law of destruction. " +
                            "It seems you must obtain the rune in order to pass.",
                            
                            "As you examine the rune, its surface pules with energy, emanating an aura of destruction. Intricate symbols" +
                            " are etched upon its surface, depicting chaos and entropy. Studying these etchings you being to grasp " +
                            "insights into the law of destruction, a fundamental force that dismantles and reshapes the fabric of " +
                            "existence.",
                            
                            "As you investigate the surroundings, you find two paths leading into the forest. " +
                            "One seems to lead to a quiet mountain cave in the distance. While the other path heads deeper " +
                            "into the forest and from time to time you hear beastial sounds coming from within.",
                            
                            "Within the dimly lit cave, a ray of sunlight penetrates through a small hole in the ceiling, " +
                            "casting a slender beam of warm illumination upon the somber scene. In the gentle embrace of this" +
                            " ethereal light, a solitary skeleton adorned in tattered, bright red robes lies peacefully upon " +
                            "the rocky floor. Lying nearby, you spot a worn-out scroll.",
                            
                            "You approach the skeletal remains adorned in vibrant red robes. Carefully searching the skeleton," +
                            " you discover a worn-out scroll lying by its side. Unfolding the delicate parchment, " + 
                            "you delve into the words of a once powerful Qi cultivator, gaining profound insights on the nature of" +
                            " destruction and its role in the cultivation journey. The scroll's teachings resonate deep within, " +
                            "enlightening your understanding and igniting a flicker of newfound potential in the path of harnessing" +
                            " destructive energies.",
                            
                            "Undeterred by the potential lurking monsters, you bravely venture deeper into the forest, determined to face " +
                            "whatever challenges lie ahead. As you travel, a chilling glare holding killing intent emanates from the " +
                            "trees ahead, signaling imminent danger. Without delay, a massive dragon-like wolf springs forward, " +
                            "forcing you to assume a defensive stance. It seems like a fight to the death is the only way out...",
                            
                            "As you approach the corpse it begins to slowly fade away, leaving a pair of daggers in its place.",
                            
                            '"In fleeing from battle, one may find temporary respite, but the shadows of their fear shall linger."' +
                            " You now find yourself back at the entrance of the two paths, though the path deeper into the forest seems " +
                            "to have become overgrown with foliage after your swift exit.",
                            
                            "Approaching the rune of destruction suspended in the air above, a surge of powerful energy courses through your body," +
                            " compelling you to shroud yourself in spiritual energy as a shield against its pure, destructive force." +
                            " As you reach out to grasp onto the rune, the world around you slowly warps, becoming a desolate expanse " +
                            "of grey mist and fragmented stones. Within this surreal realm, your mind sinks into the profundities of destruction," +
                            " enchancing your destructive power."
                            
                            ],
                'options':[['Attempt to acquire the floating rune.', 'Examine the rune.', 'Explore the surroundings.'],
                           ['Explore the cave.', 'Delve deeper into the forest.', 'Return to the runic site.']
                           ]
            },
        "illusion trial":
            {
                'prompt':[
                    # Garden scene prompt
                    " After obtaining profound knowledge in destruction you find yourself transported to a serene garden." +
                    " Before you awaits a lady with a gentle smile. 'Congratulations brave soul, you have succeeded in overcoming the challenges " +
                    "of the abyss. The abyss recognizes your valor; an award awaits you ahead.'" +
                    " Her eyes flicker momentarily, a hint of something more lurking behind her composed facade.",
                    
                    # Stone walkway scene prompt
                    "Following the mysterious woman, you find yourself on a stone walkway before a grand temple, a breathtaking landscape unfolds around you. " +
                    "The woman's voice, soft yet compelling, sounds out, 'The beauty here reflects your triumph; " +
                    "the temple just ahead hosts the treasure befitting your achievement.'",
                    
                    # Temple room prompt
                    " Entering the temple, you find yourself inside an intricately decoration room"
                    
                ],
                
                'dialogue':[
                            # State 0 dialogue
                            [   
                                # complement option response
                                "With a graceful bow and a blush that seems to enhance her ethereal beauty, the woman responds to the compliment, " +
                                "'Your kind words honor me, courageous one. But come, the treasure that awaits you is far more alluring. " +
                                "Follow me to the chamber of rewards, and let the fruits of your valor be revealed.' Her voice carries a melodic charm as the wind carries it to your ears.",
                                
                                # Trial difficulty response
                                "A glimmer of intrigue in her gaze as she responds to your inquiry. 'Ah, your curiosity is matched by your courage." +
                                " The trial you have faced was indeed one of great difficulty, a challenge few have conquered. Yet here you stand, victorious." +
                                " Come now, the treasure room awaits, and the reward within is a fitting tribute to your prowess.'",
                                
                                # Expressing suspicion response
                                "The smile on the face of the woman falters for a split second, a tiny crack in the otherwise perfect façade. " +
                                "But she quickly regains her composure, her eyes softening as she addresses your suspicion. 'Your doubt is not unwarranted, wise challenger. " +
                                "The trials of the abyss are mysterious and ever-changing, reflecting the deepest parts of those who face them. " +
                                "The path you've tread was unique to you. Now, let us proceed to your well-earned reward.'"
                            ],
                            
                            # State 1 dialogue
                            [
                                "The woman's eyes momentarily cloud with a hidden emotion as she speaks, 'My past is but a shadow, dear challenger, " +
                                "a fleeting whisper in the wind. What matters now is your remarkable " + 
                                "achievement and the reward that awaits you. Shall we enter the temple?'",
                                "As you follow the mysterious woman cautiously, subtle glitches begin to manifest in the surroundings." +
                                " Sensing your caution, the woman smiles gently and says, 'Fear not the path, brave one; it is but a" +
                                " reflection of life's imperfections.'",
                                "You proceed to follow the lady as she leads you inside of the temple."
                            ],
                            
                            # State 2 dialogue
                            [
                                "Entering the temple with the woman, your eyes are drawn to a dazzling purple gemstone resting upon an intricate pedestral." +
                                " The sheer spiritual pressure emanating from the gem tells you of its power. You notice the woman extend her hand, and" +
                                " with a subtle manipulation of spiritual energy, she gracefully guides the gem towards you." +
                                " 'Behold the Amethyst Soul' she intones, her voice resonating with power. 'This gem holds the key to great power, especially" +
                                " for someone of your cultivation realm.'",
                                "taking the gem you begin to grow weaker rapidly as it sucks away your life force. You try to let go, but the gems power is too strong.",
                                "The lady grows visibly angry as the world around you begins to shake and warp. Eventually the world around you" +
                                " shatters revealing a dark and sinister room with a disgusting wraith in the center. "
                            ],
                            
                            # State 3 dialogue
                            [
                                '''The refusal of the gem sends a shock through the illusionary woman, her carefully composed visage flickering with a sudden flash of rage.
                                 The air in the temple room begins to crackle with tension, and the once-stable illusion starts to waver and distort. "You... refuse?" she stammers, 
                                 her voice losing its melodic charm. "Such a gift is not to be denied." Her eyes narrow, and the beautiful surroundings begin to crumble, 
                                 hints of the true wraithlike nature breaking through as the illusion's control slips.''',
                                 '''With a decisive strike, you pierces the wraith's core, causing it to let out an otherworldly scream. 
                                 Its form disintegrates into shadowy wisps, the illusion fully broken, leaving behind only the chilling echo of its death as a sudden 
                                 surge of pure spiritual energy enters your core. It seems to be your reward for this trial.'''
                            ]
                ]                
            },
        'final trial':
            {
                'prompt':[
                    
                    # Final boss encounter text - 0 
                    "Before you is porcupine of massive proportions, guarding what seems to be a extremely precious cosmic fruit.",
                    
                    # Final boss battle victory text - 1
                    "After a fierce battle the cosmic fruit lays within your hands" +
                    ", the pure energy emanating from it causes your cultivation bottleneck to shift." +
                    " Biting into the fruit, you feel vast amounts of spiritual energy surging into your" +
                    " spiritual sea, pushing your cultivation through multiple stages, until finally" +
                    "you feel your spiritual energy begin to rapidly condense towards the center, forming a spherical shape." +
                    " A few moments pass inside your inner world as the condensation reaches the peak, " +
                    "now situated at the center of your spiritual scape is a luminous golden sphere, signaling your breakthrough to the Golden Core Realm.",
                    
                    # Mutated golden core text - 2
                    " Admiring your newly achieved golden core, you begin to notice red smoke proliferating throughout your spiritual scape, corrupting your spiritual energy" +
                    " and core as it does. It seems the abyss has given you another reward, your golden core has mutated into one of a destruction nature."
                ]
            },
        'end':
            {
                'prompt':[
                    "Exiting the trials, you emerge atop a divine-like mountain peak, a realm untouched by mortal gaze. Before you lies a breathtaking panorama—a vast " +
                    "expanse of lush forests, cascading waterfalls, and towering mountains adorned with veils of clouds. In this moment of triumph, you find yourself gazing " +
                    "upon a world of untamed beauty, a testament to your journey's completion in the Trials of the Abyss."
                ]
            }
    }
     
    def process_events(self, events):
        
        # Current mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Creates color change hover effect
        for option in self.clickable_options[self.transition_state]:
            option.hovering(mouse_pos)
    
        # Checks for mouse or keyboard input
        for event in events:
            
            if event.type == pygame.QUIT:
                pygame.quit()
                  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                try:
                    
                    for option in self.clickable_options[self.transition_state]:
                        if event.button == 1 and option.was_clicked(mouse_pos):
                            print("Option clicked")
                            
                            if option.scene is not None:
                                
                                if option.scene == 0:
                                    pygame.quit()
                                    
                                elif option.scene == 'examine':
                                    self.examine()
                                    
                                elif option.scene == 'explore':
                                    self.explore()
                                    
                                elif option.scene == 'previous scene':
                                    return self.previous_scene()
                                
                                elif option.scene == 'escape':
                                    self.attempt_escape()
                                
                                elif option.scene == 'next':
                                    if isinstance(self, WisdomScene):
                                        self.next_text()
                                    else:
                                        self.next_prompt_state()
                                
                                elif option.scene == 'combat':
                                    return self.start_combat()
                                
                                elif option.scene == 'death':
                                    self.scene_manager.transition_to_death(self.death_prompt)
                                
                                elif option.scene in range(1, 6):
                                    self.rating += option.scene
                                    self.next_text()
                          
                                else:
                                    return option.scene   
                except:
                    print("Clickable text not found. (events)")
    
    def updateTimer(self, delta_time):
        if not isinstance(self, StartScene):
            if self.drawUIDelay > 0:
                self.drawUIDelay -= delta_time
        else:
            pass
        
    def drawScene(self, surface):
    
        # Clear previous scene
        surface.fill((0, 0, 0))
        
        # Render background image
        surface.blit(self.image, (0,0))
        
        # Update class surface
        self.surface = surface
        
    def updateTransitionState(self, state_increment):
        
        # Hide previous text options
        for option in self.clickable_options[self.transition_state]:
            option.change_visibility()
            
        # store previous state and increment to next state of scene
        self.previous_state = self.transition_state
        self.transition_state += state_increment
        print(f"Previous state: {self.previous_state}")
        print(f"New state: {self.transition_state}")
        
        # Set new text options for current state of scene to visible
        for option in self.clickable_options[self.transition_state]:
            option.change_visibility()
    
    def initialize_options(self):
        
        for option in self.clickable_options[self.transition_state]:
            option.change_visibility()
            
    def drawUI(self, surface):
        
        if not isinstance(self, StartScene):
            
            if self.drawUIDelay <= 0:
                
                # Render text box ui and options for user
                surface.blit(self.scaled_dialogueBox, (0, 150))
                
                # Draw clickable text options
                for option in self.clickable_options[self.transition_state]:
                    option.draw(surface)
                
                self.create_text_box(surface, self.prompt, self.font)
                
        else:
            # Draw start and exit buttons
            surface.blit(self.startButton, (500, 580))
            surface.blit(self.startButton, (500, 670))
            
            # Draw clickable text options for start scene
            for option in self.clickable_options[self.transition_state]:
                if option is not None:
                    option.draw(surface)
                    
        # Update class surface
        self.surface = surface
             
    def create_text_box(self, surface, text, fontObject):
        
        # Max width and height of text for dialogue box
        maxWidth = 515 
        maxHeight = 50
        
        words = text.split() # word list
        
        lines = list()
        currentLine = ""
        for word in words:
            
            # Add current word to test line
            testLine = currentLine + word + " "
            
            # Grab text width and height to check if it fits within maximum width/height
            text_width, text_height = fontObject.size(testLine)
            
            if text_width <= maxWidth and text_height <= maxHeight:
                # If it fits update current line
                currentLine = testLine
            else:
                # If it doesn't fit, start a new line
                lines.append(currentLine)
                currentLine = word + " "
                
        # Add the last line
        lines.append(currentLine)
        
        # Blit lines of text onto the dialogue box surface
        y = 410
        for line in lines:

            text_surface = fontObject.render(line, True, (0, 0, 0))
            surface.blit(text_surface, (475, y))
            y += text_surface.get_height() + 5 # Adjusts for line spacing
            
    def update_text_box(self):
        
        print("Updating text box.")
        # Redraw the text box to clear it
        self.surface.blit(self.scaled_dialogueBox, (0, 150))
        
        # Draw clickable text options
        for option in self.clickable_options[self.transition_state]:
            option.draw(self.surface)

        # Draw text prompt
        self.create_text_box(self.surface, self.prompt, self.font)
        
    def previous_scene(self):
        
        # Restore the previous prompt
        self.prompt = self.previous_prompt
        
        # hide text options of current scene
        for option in self.clickable_options[self.transition_state]:
            option.change_visibility()
            
        # Restore transition state to previous scene
        self.transition_state = self.previous_state
        
        # make text options of previous scene visible
        for option in self.clickable_options[self.transition_state]:
            option.change_visibility()
            
        # Return the scene ID of the previous scene
        return self.previous_scene_id
   
    def resize_image(self, image, width_scaling_factor, height_scaling_factor):
            
        width, height = image.get_size()
        new_width = round(width / width_scaling_factor)
        new_height = round(height / height_scaling_factor)
        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))  
        
        return scaled_image
    
    def draw_prompt(self, prompt:str|bytes|None, x:int, y:int, color):

        if color is None:
            color = (0, 0, 0)
            
        text_surface = self.font.render(prompt, True, color)
        self.surface.blit(text_surface, (x, y))
        
class SceneManager:
    def __init__(self) -> None:
        self.scenes = {
            'start': StartScene,
            'temple': TempleScene,
            'gate': GateScene,
            'trial1': Trial1,
            'coward': CowardScene,
            'wisdom': WisdomScene,
            'destruction':DestructionScene,
            'illusion':IllusionScene,
            'final-trial':FinalTrial,
            'combat':CombatScene,
            'death':DeathScene,
            'end':EndScene
        }
        self.previous_scenes = list()
        self.current_scene = None
        
        # Player
        self.player = Character()
    
    def transition_to_scene(self, sceneID):
        
        print("Transition_to_scene function start.")
        
        # Grab scene class based on sceneID
        scene_class = self.scenes.get(sceneID)
        
        if scene_class:
            print(f"Transitioning to {scene_class}")
            
            # Check if the scene class already exists in previous scenes list
            for scene in self.previous_scenes:
                if isinstance(scene, scene_class):
                    # If the scene being transitioned to is the start scene, reset the previous scenes list and reset character
                    if isinstance(scene, StartScene):
                        self.previous_scenes.clear()
                        self.player.reset_character()
                    
                    # Checks whether the current scene is a combat one and updates the combat outcome for the previous scene's logic   
                    elif isinstance(self.current_scene, CombatScene):
                        combat_flag = self.current_scene.combat_outcome
                        
                    self.current_scene = scene
                    if isinstance(self.current_scene, DestructionScene) or isinstance(self.current_scene, IllusionScene) or isinstance(self.current_scene, FinalTrial):
                        self.current_scene.end_combat(combat_flag)
                    return
                    
            # If it doesn't exist, instantiate the new scene class
            if scene_class == DestructionScene or scene_class == IllusionScene or scene_class == FinalTrial:
                scene = scene_class(self)  
            else: 
                scene = scene_class()
                
            self.previous_scenes.append(scene)
            self.current_scene = scene
 
        else:
            print(f"Scene with ID {sceneID} does not exist")
     
    def transition_to_death(self, prompt):
        
        scene = DeathScene(prompt)
        self.current_scene = scene
               
    def process_current_scene(self, events):
        
        # Process game events for the current scene, and handle scene transition requests
        nextSceneID = self.current_scene.process_events(events)
        
        if nextSceneID is not None:
            print(f"new scene id: {nextSceneID}")
            
        # If the current scene requests a transition to another scene
        if isinstance(nextSceneID, CombatScene):
            self.current_scene = nextSceneID
            
        elif nextSceneID:
            print(f"next scene id: {nextSceneID}")
            self.transition_to_scene(nextSceneID)
            
    def get_character(self):
        return self.player

class StartScene (Scene):
    def __init__(self) -> None:
        # Text for clickable options
        self.start_button_text = "Begin Adventure"
        self.exit_button_text = "Exit"
        
        # Images for scene
        self.image = self.loadScreen
        
        # Scene transition state variable
        self.transition_state = 0
        
        # Font for text
        self.font_path = self.Haseyo_font
        self.font = pygame.font.Font(self.font_path, 35)
        
        # Option text
        self.clickable_options = [
            [   # first state options
                Clickable_text(self.start_button_text, 604, 605, self.font, "black", 'temple'), 
                Clickable_text(self.exit_button_text, 680, 695, self.font, "black", 0) 
            ]
        ]
        
        # Sets the options for the first scene to visible
        self.initialize_options()
    
class TempleScene (Scene):
    
    def __init__(self) -> None:
        self.prompt = self.dialogue['temple']['prompt']
        self.examine_text = self.dialogue['temple']['examine']
        self.options = self.dialogue['temple']['options']
        self.image = self.temple_entrance 
        
        # Scene transition state variable
        self.transition_state = 0
        
        # Holds the previous scene data 
        self.previous_prompt = None
        self.previous_scene_id = 'temple'
        self.previous_state = 0
        
        # Font for text
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        # Option text
        self.clickable_options = [
            # first state options
            [
                Clickable_text(self.options[0], 470, 560, self.font, "black", 'gate'), # Entering temple
                Clickable_text(self.options[1], 470, 600, self.font, "black", 'examine'), # Examine surroundings
                Clickable_text(self.options[2], 470, 640, self.font, "black", 'coward') # Leave to sect
            ],
            # examine state options
            [
                Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'previous scene')
            ]
        ]
        
        # Sets the options for the first scene to visible
        self.initialize_options()
        
    def examine(self):
        
        # Update Prompt to the examine text
        self.previous_prompt = self.prompt
        self.prompt = self.examine_text
        
        # Update transition state
        self.updateTransitionState(1)
        
        # Update the text box with the new prompt 
        self.update_text_box()
         
class GateScene (Scene):
    
    def __init__(self) -> None:
        
        # Text and image variables
        self.prompt = self.dialogue['gate']['prompt']
        self.examine_text = self.dialogue['gate']['examine']
        self.escape_text = self.dialogue['gate']['escape']
        self.options = self.dialogue['gate']['options']
        self.image = self.trial_gate
        
        # Scene transition state variable
        self.transition_state = 0
        
        # Previous scene data
        self.previous_prompt = None
        self.previous_scene_id = 'gate'
        self.previous_state = 0
        
        # Font for text
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        # Option text
        self.clickable_options = [
            # first state options
            [
                Clickable_text(self.options[0], 465, 600, self.font, "black", 'trial1'), # enter archway
                Clickable_text(self.options[1], 465, 640, self.font, "black", 'examine'), # examine etchings
                Clickable_text(self.options[2], 465, 680, self.font, (0, 0, 0), 'escape') # Attempt to leave
            ],
            # examine state options
            [
                Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'previous scene')
            ],
            # escape state options
            [
                Clickable_text("Proceed through the archway.", 465, 600, self.font, (0, 0, 0), 'trial1'),
                Clickable_text("Examine the etchings", 465, 640, self.font, (0, 0, 0), 'examine')
            ]
        ]
        
        # Sets the options for the first scene to visible
        self.initialize_options()
        
    def examine(self):
        print('examining')
        
        # Update text box to examine text for the gate scene
        self.previous_prompt = self.prompt
        self.prompt = self.examine_text
        
        # Update transition state
        if self.transition_state == 0:
            self.updateTransitionState(1)
        else:
            self.updateTransitionState(-1)
        
        # Update the text box with the new prompt 
        self.update_text_box()
        
    def attempt_escape(self):
        print('escaping')
        
        # Update tet box to escape text for the gate scene
        self.prompt = self.escape_text
        
        # Update transition state and text box
        self.updateTransitionState(2)
        self.update_text_box()
        
class CowardScene (Scene):
    
    def __init__(self) -> None:
        
        self.prompt = self.dialogue['coward']['prompt']
        self.pondering_text = self.dialogue['coward']['pondering']
        self.options = self.dialogue['coward']['options']
        self.image = self.leaving_image
        
        # Scene transition state variable
        self.transition_state = 0
        
        # Previous scene data
        self.previous_prompt = None
        self.previous_state = 0
        
        # Font for text
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        # Text options for user
        self.clickable_options = [
            # first state options
            [
                Clickable_text(self.options[0], 470, 560, self.font, "black", 'temple'), # Entering temple
                Clickable_text(self.options[1], 470, 600, self.font, "black", 'start'), # Examine surroundings
                Clickable_text(self.options[2], 470, 640, self.font, (0, 0, 0), 'examine') # Leave to sect
            ],
            # examine state options
            [
                Clickable_text("Head back to the temple.", 470, 600, self.font, (0, 0, 0), 'temple'),
                Clickable_text("Continue along the coward's path.", 470, 640, self.font, (0, 0, 0), 'start')
            ]
        ]
        
        # Sets the options for the first scene to visible
        self.initialize_options()
        
    def examine(self):
        
        print('examining')
        # Update Prompt to the pondering text and create new clickable options for the user to choose from.
        self.previous_prompt = self.prompt
        self.prompt = self.pondering_text
   
        # Update transition state
        self.updateTransitionState(1)
        
        # Update the text box with the new prompt 
        self.update_text_box()

class Trial1 (Scene):
    
    def __init__(self) -> None:
        
        self.prompt = self.dialogue['trial1']['prompt']
        self.next_prompt = self.dialogue['trial1']['voice']
        self.options = self.dialogue['trial1']['options']
        self.image = self.platform
        
        # Scene transition state variable
        self.transition_state = 0
        self.previous_state = 0
        
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        # Text options for user
        self.clickable_options = [
            # first state option
            [
                Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'next')
            ],
            # choice state options
            [
                Clickable_text(self.options[0] + " (left)", 465, 560, self.font, (0, 0, 0), 'wisdom'), # wisdom portal
                Clickable_text(self.options[1] + " (right)", 465, 600, self.font, (0, 0, 0), 'destruction') # destruction portal
            ]
        ]
        
        # Sets the options for the first scene to visible
        self.initialize_options()
        
    def next_prompt_state(self):
        print('next ->')
        
        # Update transition state, text box, and prompt
        self.updateTransitionState(1)
        self.prompt = self.next_prompt
        self.update_text_box()
         
class WisdomScene (Scene):
    
    def __init__(self) -> None:
        
        # Image and text variables
        self.prompt = self.dialogue['wisdom portal']['prompt']
        self.options = self.dialogue['wisdom portal']['options']
        self.image = self.wisdom_trial
        
        # score variable to determine if the player passes the trial
        self.rating = 0
        
        # Font
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Scene transition state variable
        self.transition_state = 0
        self.previous_state = 0
        
        # Delays in seconds
        self.drawUIDelay = 1.0
        self.deathSceneDelay = 1.9
        
        # Clickable options
        self.clickable_options = [
            # first state option
            [
                Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'next')
            ],
            # dialogue from the demon beast
            [
                Clickable_text("Begin trial of wisdom.", 630, 670, self.font, (0, 0, 0), 'next')
            ],
            # Answers to the first trial question, the integer for the scene variable of clickable text represents the degree of "correctness"
            # based on the age old draconic beast's beliefs
            [
                Clickable_text(self.dialogue['wisdom portal']['answers'][0], 460, 560, self.font, (0, 0, 0), 3),
                Clickable_text(self.dialogue['wisdom portal']['answers'][1], 460, 600, self.font, (0, 0, 0), 4),
                Clickable_text(self.dialogue['wisdom portal']['answers'][2], 460, 640, self.font, (0, 0, 0), 5)
            ],
            # Answers to the second trial question
            [
                Clickable_text(self.dialogue['wisdom portal']['answers'][3], 465, 560, self.font, (0, 0, 0), 2),
                Clickable_text(self.dialogue['wisdom portal']['answers'][4], 465, 600, self.font, (0, 0, 0), 4),
                Clickable_text(self.dialogue['wisdom portal']['answers'][5], 465, 640, self.font, (0, 0, 0), 5)
            ],
            # Answers to the third trial question
            [
                Clickable_text(self.dialogue['wisdom portal']['answers'][6], 465, 560, self.font, (0, 0, 0), 4),
                Clickable_text(self.dialogue['wisdom portal']['answers'][7], 465, 600, self.font, (0, 0, 0), 3),
                Clickable_text(self.dialogue['wisdom portal']['answers'][8], 465, 640, self.font, (0, 0, 0), 1)
            ],
            # option to advance to the next trial
            [
                Clickable_text("Advance to the next trial" , 610, 670, self.font, (0, 0, 0), 'trial2')
            ],
            # options for failure of trial
            [
                Clickable_text("Begin anew", 665, 640, self.font, (0, 0, 0), 'start'),
                Clickable_text("Give up", 680, 670, self.font, (0, 0, 0), 0)
            ]
        ]
        
        # set first scene option to visible
        self.initialize_options()

    def next_text(self):
        print("next question")
        
        # Update transition state, text box, and prompt
        self.updateTransitionState(1)
            
        if self.transition_state == 1:
            self.prompt = self.dialogue['wisdom portal']['beast'][0]
        elif self.transition_state == 5:
            
            # Check whether the player has passed the trial or not: Score to pass = 10 minimum
            if self.rating >= 10:
                self.prompt = self.dialogue['wisdom portal']['beast'][1]
            else:
                self.updateTransitionState(1)
                self.prompt = self.dialogue['wisdom portal']['beast'][2]
                 
        else:
            self.prompt = self.dialogue['wisdom portal']['questions'][self.transition_state - 2]
            
        self.update_text_box()
           
    def updateTimer(self, delta_time):
        if self.transition_state != 6:
            super().updateTimer(delta_time)
        else:
            if self.deathSceneDelay > 0:
                self.deathSceneDelay -= delta_time
       
    def drawScene(self, surface):
        
        # Draws scene depending on whether the player is in the trial / passed the trial, or they have failed the trial
        if self.transition_state in range(0, 6):
            # Clear previous scene
            surface.fill((0, 0, 0))
            
            # Render background image
            surface.blit(self.image, (0,0))
        
        else:
            if self.deathSceneDelay > 0:
                # Hide clickable options until death delay is 0
                for option in self.clickable_options[6]:
                    option.set_visibility(False)
                    
                # Clear previous scene
                surface.fill((0, 0, 0))
                
                # Render background image
                surface.blit(self.image, (0,0))
            else:
                # Unhide clickable options for death scene
                for option in self.clickable_options[6]:
                    option.set_visibility(True)
                    
                # Change to full black death screen
                surface.fill((0, 0, 0))
        
        # Update class surface
        self.surface = surface       
    
class DestructionScene (Scene):
    
    def __init__(self, scene_manager:SceneManager) -> None:
        # Image and text variables
        self.prompt = self.dialogue['destruction portal']['prompt'][0]
        self.image = self.destruction_trial
        self.grey_screen = pygame.image.load('images/grey-screen.png')
        self.monster_image = pygame.image.load('images/demon-wolf')
        self.daggers_image = self.resize_image(pygame.image.load('images/fang-daggers.png'), 4.5, 4.5)
        self.rune_image = pygame.image.load('images/rune-shard.png').convert_alpha()
        
        # Set initial alpha value (0 = fully transparent, 255 = fully visible)
        self.alpha = 0
        
        # Scene manager reference 
        self.scene_manager = scene_manager
        
        # Rune collection flag
        self.rune_obtained = False
        
        # Combat variables
        self.chance = 100 # Player's chance value to obtain the rune
        self.combat_one = 0 # Flag for whether the first combat scene was fought
        self.combat_outcome = None # Updated from the scene manager class
        self.corpse_looted = False
        
        # Font
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Scene transition state variable
        self.transition_state = 0
       
        # Previous state variables 
        self.previous_image = None
        self.previous_state = 0
        self.previous_prompt = None
        
        # Delays in seconds
        self.drawUIDelay = 1.0
        self.promptDelay = self.drawUIDelay - .5
        self.image_delay = 0.0
        
        # Clickable options
        self.clickable_options = [
            # first state option
            [
                Clickable_text(self.dialogue['destruction portal']['options'][0][0], 460, 570, self.font, (0, 0, 0), 'next'),
                Clickable_text(self.dialogue['destruction portal']['options'][0][1], 460, 610, self.font, (0, 0, 0), 'examine'),
                Clickable_text(self.dialogue['destruction portal']['options'][0][2], 460, 650, self.font, (0, 0, 0), 'explore')
            ],
            [
                Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'previous scene')
            ],
            [
                Clickable_text(self.dialogue['destruction portal']['options'][1][0], 460, 550, self.font, (0, 0, 0), 'explore'),
                Clickable_text(self.dialogue['destruction portal']['options'][1][1], 460, 590, self.font, (0, 0, 0), 'next'),
                Clickable_text(self.dialogue['destruction portal']['options'][1][2], 460, 630, self.font, (0, 0, 0), 'previous scene')
            ],
            [
                # Find a better spiritual sword and cultivation manual which will make fighting the monsters easier
                Clickable_text("Search the skeleton.", 460, 570, self.font, (0, 0, 0), 'examine'),
                Clickable_text("Go back and take the other path.", 460, 610, self.font, (0, 0, 0), 'explore'),
                Clickable_text(self.dialogue['destruction portal']['options'][1][2], 460, 650, self.font, (0, 0, 0), 'next')
            ],
            [
                Clickable_text("Begin Battle.", 670, 670, self.font, (0, 0, 0), 'combat')
            ],
            [
                Clickable_text("Loot the Draconic Wolf.", 460, 570, self.font, (0, 0, 0), 'examine'),
                Clickable_text("Explore the cave.", 460, 610, self.font, (0, 0, 0), 'explore'),
                Clickable_text("Return to the runic site.", 460, 650, self.font, (0, 0, 0), 'previous scene')
            ],
            [
                Clickable_text("Continue", 675, 670, self.font, (0, 0, 0), 'illusion')
            ]
        ]
        
        # sets the first scene option to visible
        self.initialize_options()
    
    def next_prompt_state(self):
        
        # Attempt to acquire rune state
        if self.transition_state == 0:
            
            random_chance = random.randint(0, 100)
            
            # if random_chance is less than chance value then the player obtains the rune
            if random_chance <= self.chance:
                
                # Set prompt for obtaining the rune, set flag to indicate rune was obtained, and update transition state to end of trial
                self.prompt = self.dialogue['destruction portal']['prompt'][8]
                self.rune_obtained = True
                self.updateTransitionState(6)
                
                # Set image delay to # seconds
                self.image_delay = 4.0
                
                # Player gains +20% increased damage overall
                self.scene_manager.player.increase_percent_damage(.2)
                
                # Increase player level by 1
                self.scene_manager.player.levelUp(1)
                self.scene_manager.player.status()
                
                # the floating surroundings begin to show a fragmented reality as you get closer to the rune
            else:
                prompt = "Luck favors the brave...atleast most of the time."
                self.scene_manager.transition_to_death(prompt)
                
        elif self.transition_state == 1:
            self.prompt = self.dialogue['destruction portal']['prompt'][2]
            self.updateTransitionState(1)
        
        elif self.transition_state == 2:
            if self.combat_one == 0 and self.combat_outcome is None:
                self.prompt = self.dialogue['destruction portal']['prompt'][5]
                self.image_delay = 2.5
                self.updateTransitionState(2)
            
        elif self.transition_state == 3:
            self.prompt = self.dialogue['destruction portal']['prompt'][0]
            self.reset_image()
            self.updateTransitionState(-3)
            
    def explore(self):
        
        if self.transition_state == 0:
            transition_increment = 2
            
        elif self.transition_state == 2:
            transition_increment = 1
            self.update_image(self.cave_skeleton)
            
        elif self.transition_state == 3:
            
            if self.combat_one == 0 and self.combat_outcome == None:
                
                # Delete option that leads to combat scene
                self.delete_clicked_option(1, 610)
                
                # Update transition state to before combat
                self.updateTransitionState(1)
                self.reset_image()
                self.image_delay = 2.0
                self.previous_prompt = self.dialogue['destruction portal']['prompt'][0]
                self.prompt = self.dialogue['destruction portal']['prompt'][self.transition_state + 1]
                self.update_text_box()
            return
        
        elif self.transition_state == 5:
            transition_increment = -2
            self.image = self.cave_skeleton
            
        # Update scene state and prompt
        self.updateTransitionState(transition_increment)
        self.previous_prompt = self.prompt
        self.prompt = self.dialogue['destruction portal']['prompt'][self.transition_state]
        self.update_text_box()
        
    def start_combat(self):
        
        if self.combat_one == 0:
            opponent = Character()
            monster_image = self.monster_image
        
        # Create Combat scene object with opponent to fight
        combat_scene = CombatScene(opponent, monster_image, self.scene_manager)
        combat_scene.set_previous_scene('destruction')
        return combat_scene
    
    def end_combat(self, combat_outcome):
        
        self.combat_outcome = combat_outcome
        
        if combat_outcome == 1:
            self.combat_one = 1
            
            # Update chance to obtain rune
            self.update_chance(40)
            self.scene_manager.player.full_heal()
            
            # Update prompt
            self.previous_prompt = self.prompt
            self.prompt = "hi"
            
            # Increment to victory transition state
            states_increment = 5 - self.transition_state
            self.updateTransitionState(states_increment)
            self.update_image(self.monster_image)
            
        else:
            self.prompt = self.dialogue['destruction portal']['prompt'][7]
            states_increment = 0 - self.transition_state
            self.updateTransitionState(states_increment)
            self.reset_image()
            
    def examine(self):
        
        if self.transition_state == 0:
            
            # Delete option that was clicked
            self.delete_clicked_option(1, 610)
            
            # Update scene state and prompt
            self.updateTransitionState(1)
            self.previous_prompt = self.prompt
            self.prompt = self.dialogue['destruction portal']['prompt'][1]
            self.update_text_box()
            
            # update chance value
            self.update_chance(10)
            
        elif self.transition_state == 3:
            
            self.delete_clicked_option(0, None)
            
            # Update scene state and prompt
            self.updateTransitionState(-2)
            self.previous_prompt = self.prompt
            self.prompt = self.dialogue['destruction portal']['prompt'][4]
            self.update_text_box()
            
            # Update chance value and update options
            self.update_chance(20)
            
        elif self.transition_state == 5:
            
            self.delete_clicked_option(0, None)
            
            # increase player base damage by 3 and set corpse looted flag to true
            self.scene_manager.player.increase_flat_damage(3)
            self.corpse_looted = True
            self.prompt = "As you approach the wolf's corpse it begins to fade away, leaving behind a pair of daggers. "
            
            # make prompt blank, draw a prompt message at top saying Loot from draconic wolf: then put a picture of fang daggers
            # underneath tell the player they gained the Draconis Fangs which gives them a base damage increase of 3
            
    def process_events(self, events): 
        return super().process_events(events)
    
    def previous_scene(self):
        
        if self.transition_state == 5:
            # Set previous image and prompt for previous scene transition
            self.previous_image = self.reset_image()
            self.previous_prompt = self.dialogue['destruction portal']['prompt'][0]
            self.previous_state = 0
            
        return super().previous_scene()  
        
    def delete_clicked_option(self, option_index, y):
        
        ''' Deletes the clickable option for the given index inside of the current transition state options'''
        
        del self.clickable_options[self.transition_state][option_index]  
        
        if option_index == 0:
            pass
        
        elif option_index == 1:
            self.clickable_options[self.transition_state][option_index - 1].set_y(y)
            self.clickable_options[self.transition_state][option_index - 1].wrap_text()
            
        elif option_index == 2:
            self.clickable_options[self.transition_state][option_index - 1].set_y(y + 40)
            self.clickable_options[self.transition_state][option_index - 2].set_y(y)
            self.clickable_options[self.transition_state][option_index - 1].wrap_text()
            self.clickable_options[self.transition_state][option_index - 2].wrap_text()
            
        else:
            print("Invalid Index")
                         
    def update_chance(self, chance_increase):
        self.chance += chance_increase
        print(f"New chance value: {self.chance}")
    
    def update_image(self, image):
        if image is not None:
            self.previous_image = self.image
            self.image = image
    
    def updateTimer(self, delta_time):
        super().updateTimer(delta_time)
        
        if self.image_delay > 0:
            self.image_delay -= delta_time
            
        if self.promptDelay > 0:
            self.promptDelay -= delta_time
        
    def reset_image(self):
        self.image = self.destruction_trial
        
        if self.transition_state == 5:
            return self.destruction_trial
        
    def drawUI(self, surface):
        
        if self.combat_one != 0 and self.transition_state == 5:
            surface.blit(self.grey_screen, (0, 0))
            
        super().drawUI(surface)
        
        if self.transition_state == 1 and self.previous_state == 0:
            self.draw_prompt("Gained: +10% to chance to obtain the law rune.", 520, 610, None)
            
        elif self.transition_state == 1 and self.previous_state == 3:
            self.draw_prompt("Gained: +20% to chance to obtain the law rune.", 520, 645, None)
            
        elif self.transition_state == 5 and self.corpse_looted:
            pygame.draw.rect(surface, (0, 0, 0), (478, 20, 500, 333))
            surface.blit(self.daggers_image, (483, 25))
            self.draw_prompt("You've obtained", 748, 145, (255, 255, 255))
            self.draw_prompt("Draconis' Fangs", 748, 175, (255, 255, 255))
            self.draw_prompt("+3 to Attack Damage", 728, 205, (255, 255, 255))
            
        # Draw reward prompt for successfully obtained the rune when rune-shard image is almost visible    
        elif self.transition_state == 6 and self.alpha >= 240:
            self.draw_prompt("Gained: +20% Increased Attack Damage", 555, 645, None)
        
    def drawScene(self, surface):
        
        if self.transition_state == 4  and self.image_delay <= 0.0:
            
            surface.fill((0, 0, 0))
            self.update_image(self.monster_image)
            surface.blit(self.image, (0, 0))
            self.surface = surface
        
        elif self.rune_obtained:
            
            # Set the alpha value of the rune shard image
            self.rune_image.set_alpha(self.alpha)
            
            # Render background image (destruction trial image) and foreground image that slowly fades in (rune-shard)
            surface.fill((0, 0, 0))
            surface.blit(self.image, (0, 0))
            surface.blit(self.rune_image, (0, 0))
            
            # Increase alpha to fade in foreground image
            if self.image_delay <= 0:
                self.alpha += 1
                if self.alpha > 255:
                    self.alpha = 255
                  
        else:
            super().drawScene(surface)
    
class IllusionScene (Scene):
    
    def __init__(self, scene_manager:SceneManager) -> None:
        # Scene text
        self.prompt = self.dialogue['illusion trial']['prompt'][0]
        self.death_prompt = '''You reach out and grab the gem, triggering a soul wrenching pain, quickly you notice that your very soul is being siphoned away 
        by the deathly beautiful gem. In desperation you attempt to remove the soul-devouring gem from your hand. However, the gem does not budge in the slightest. 
        Time seems to pass by slowly as your life fades away to darkness.'''
        
        # Scene images
        self.image = pygame.image.load('images/illusion-woman.png')
        self.illusion_woman_image = pygame.image.load('images/illusion-woman.png')
        self.frown_image = pygame.image.load('images/illusion-woman-frown2.png')
        self.illusion_woman_no_background = pygame.image.load('images/illusion-woman-no-background.png').convert_alpha()
        self.walkway_image = pygame.image.load('images/walkway-to-room.png').convert_alpha()
        self.temple_room_image = pygame.image.load('images/temple-room.png').convert_alpha()
        self.wraith_image = pygame.image.load('images/evil-ghost.png').convert_alpha()
        self.gem = pygame.image.load('images/illusion-gem.png')
        
        # Set initial alpha values (0 = fully transparent, 255 = fully visible)
        self.alpha = 0
        self.gem_alpha = 0
        self.temple_alpha = 255
        self.woman_alpha = 255
        
        # Create mask_surface for glitch effect
        self.mask_surface = pygame.Surface((1456, 816), pygame.SRCALPHA)
        self.create_glitch_mask(self.mask_surface, num_glitches=1, max_size=35)
        self.mask_indicator = False # Flag for whether to have the glitch effect occur
        
        # Scene Manager reference
        self.scene_manager = scene_manager
        
        # Combat variables
        self.combat_one = 0 # Flag for whether the first combat scene was fought
        self.combat_outcome = None # Updated by the scene manager class after combat
        
        # Font
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Scene transition state variable
        self.transition_state = 0 # 0 for start of illusion scene, 1 for walkway scene, 2 for temple room scene, 3 for mini boss battle scene
       
        # Previous state variables 
        self.previous_image = None
        self.previous_state = 0
        self.previous_prompt = None
        
        # Delays in seconds
        self.drawUIDelay = 1.0
        self.promptDelay = 0.0
        self.image_delay = 0.0
        
        # Clickable options
        self.clickable_options = [
            # State 0
            [
                Clickable_text("Compliment the woman.", 460, 590, self.font, (0, 0, 0), 'next'),
                Clickable_text("Inquire about the difficulty of the trial.", 460, 630, self.font, (0, 0, 0), 'examine'),
                Clickable_text("Express suspicion about the trials.", 460, 670, self.font, (0, 0, 0), 'explore')
            ],
            # State 1
            [
                Clickable_text("Follow.", 675, 670, self.font, (0, 0, 0), 'next')
            ],
            # State 2
            [
                Clickable_text("Ask about her past.", 460, 570, self.font, (0, 0, 0), 'next'),
                Clickable_text("Proceed following her cautiously.", 460, 610, self.font, (0, 0, 0), 'examine'),
                Clickable_text("Follow her.", 460, 650, self.font, (0, 0, 0), 'explore')
            ],
            # State 3
            [
                Clickable_text("Take the gem.", 460, 630, self.font, (0, 0, 0), 'death'),
                Clickable_text("Refuse to take the gem.", 460, 670, self.font, (0, 0, 0), 'next')
            ]
            
            # Implement a few flashes of the real wraith image after taking the gem, and then include a swooshing sound effect like your energy is being sucked away
            ,
            # State 4 - illusion breaking scene
            [
                Clickable_text("Fight for your life.", 630, 670, self.font, (0, 0, 0), 'combat')
            ],
            # State 5
            [
                Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'previous scene')
            ],
            # State 6 - Victory state
            [
                Clickable_text("Move on to the final trial.", 610, 670, self.font, (0, 0, 0), 'final-trial')
            ],
            # State 7 - Continue button for temple scene
            [
                Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'previous scene')
            ]
        ]
        
        # sets the first scene option to visible
        self.initialize_options()
        
    def next_prompt_state(self):
        
        if self.transition_state == 0:
            self.prompt = self.dialogue['illusion trial']['dialogue'][0][0]
            self.updateTransitionState(1)
           
        elif self.transition_state == 2:
            self.previous_prompt = self.prompt
            self.prompt = self.dialogue['illusion trial']['dialogue'][1][0]
            self.updateTransitionState(3)
            
        elif self.transition_state == 3:
            if self.promptDelay <= 0.0:
                self.prompt = self.dialogue['illusion trial']['dialogue'][3][0]
                self.updateTransitionState(1)
                self.update_image(self.wraith_image)
                self.gem_alpha = 255 # Set the gem alpha to max incase the player quickly clicks on the refuse gem option
                self.image_delay = 2.0
            
        elif self.previous_state == 0 and self.transition_state == 1 and self.image_delay <= 0.0:
            self.prompt = self.dialogue['illusion trial']['prompt'][1]
            self.updateTransitionState(1)
            self.update_image(self.walkway_image)
            self.illusion_woman_image = self.illusion_woman_no_background
            
        elif self.previous_state == 2 and self.transition_state == 1:
            self.prompt = self.dialogue['illusion trial']['dialogue'][0][0]
            self.updateTransitionState(2)
            self.update_image(self.temple_room_image)
                 
    def examine(self):
        
        if self.transition_state == 0:
            self.prompt = self.dialogue['illusion trial']['dialogue'][0][1]
            self.updateTransitionState(1)
            
        elif self.transition_state == 1:
            self.prompt = self.dialogue['illusion trial']['dialogue'][1][1]
            self.updateTransitionState(-1)
            
        elif self.transition_state == 2:
            if not self.mask_indicator:
                
                # Update to new prompt
                self.previous_prompt = self.dialogue['illusion trial']['dialogue'][1][1]
                self.prompt = self.dialogue['illusion trial']['dialogue'][2][0]
        
                # Transition to state 3 (Temple room) and set previous state
                self.updateTransitionState(1)
                self.previous_state = 3
                
                # Update the image to temple room, create delay for next prompt, and trigger glitch effect flag
                self.update_image(pygame.image.load('images/temple-room.png'))
                self.mask_indicator = True
                self.image_delay = 1.0
                self.promptDelay = 5.0
                
        elif self.transition_state == 3:
            self.previous_prompt = self.prompt
            self.prompt = "Lady explains about the gem and the power it can give."
            self.updateTransitionState(2)
    
    def explore(self):
        
        if self.transition_state == 0:
            self.prompt = self.dialogue['illusion trial']['dialogue'][0][2]
            self.updateTransitionState(1)
            self.image_delay = 0.5
            self.previous_image = self.illusion_woman_image
            
        elif self.transition_state == 2:
            
            # Update dialogue
            self.previous_prompt = "'Take your reward challenger' - Woman"
            self.prompt = self.dialogue['illusion trial']['dialogue'][2][0]
            
            # Update image and state, and set previous state
            self.updateTransitionState(5)
            self.previous_state = 3
            self.update_image(pygame.image.load('images/temple-room.png'))
    
    def start_combat(self):
        
        if self.combat_one == 0:
            monster = Character()
        
        # Create wraith mini-boss combat scene and return it to the scene manager  
        combat_scene = CombatScene(monster, self.wraith_image, self.scene_manager)
        combat_scene.set_previous_scene('illusion')
        return combat_scene
    
    def end_combat(self, combat_outcome):

        self.combat_outcome = combat_outcome
        
        if combat_outcome == 1:
            
            # Update combat flag
            self.combat_one = 1
        
            # Update prompt
            self.previous_prompt = self.prompt
            self.prompt = self.dialogue['illusion trial']['dialogue'][3][1]
            
            # Increased player's level by 2 from victory and heal the player back to full
            self.scene_manager.player.levelUp(2)
            self.scene_manager.player.full_heal()
            self.scene_manager.player.status()
            
            # Increment to victory transition state
            states_increment = 6 - self.transition_state
            self.updateTransitionState(states_increment)
            self.update_image(self.wraith_image)
                      
    def updateTimer(self, delta_time):
        super().updateTimer(delta_time)
        
        if self.image_delay > 0:
            self.image_delay -= delta_time
            
        if self.promptDelay > 0:
            self.promptDelay -= delta_time
                
    def drawScene(self, surface):
        
        if not self.mask_indicator:
               
            # Draw background of scene
            super().drawScene(surface)
            
            if self.promptDelay <= 0.0 and (self.transition_state == 3 or self.transition_state == 7):
                # Reshow clickable options after glitches and prompt switch occur
                for option in self.clickable_options[self.transition_state]:
                    option.set_visibility(True)
                    
                # Show the reward gem
                reward_gem = self.resize_image(self.gem, 3, 3)
                reward_gem.set_alpha(self.gem_alpha)
                surface.blit(reward_gem, (555, 20))
                
                # Update alpha value of gem
                if self.gem_alpha < 255:
                    self.gem_alpha += 1
                else:
                    self.gem_alpha = 255
                    
            if self.transition_state == 4:
                
                if self.temple_alpha > 0:
                    self.initialize_glitch(surface, self.frown_image, 2, 1.0, 15, 50)
                    
                # Draw the temple room, gem, and woman images over the wraith image
                surface.blit(self.temple_room_image, (0, 0))
                
                woman = pygame.transform.flip(self.illusion_woman_image, True, False)
                surface.blit(woman, (500, 0))
                
                reward_gem = self.resize_image(self.gem, 3, 3)
                surface.blit(reward_gem, (555, 20))
                
                
                # Update the alpha value of the temple, gem, and woman images
                self.temple_room_image.set_alpha(self.temple_alpha)
                self.illusion_woman_image.set_alpha(self.woman_alpha)
                self.gem.set_alpha(self.gem_alpha)
                
                if self.temple_alpha > 0 and self.woman_alpha > 0 and self.gem_alpha > 0:
                    alpha_decrease = 2
                    self.temple_alpha -= alpha_decrease
                    self.woman_alpha -= alpha_decrease
                    self.gem_alpha -= alpha_decrease

        else:
            
            # Hide clickable options for the duration of the glitch
            for option in self.clickable_options[self.transition_state]:
                option.set_visibility(False)
                
            # Create glitch effect for state 3
            if self.image_delay > 0.0:
                
                self.initialize_glitch(surface, self.wraith_image, 2, 1.0, 1, 50)
            
            else:   
                self.mask_indicator = False
        
        # Draw image of illusionist woman
        if self.transition_state == 0 or self.transition_state == 1:
            if self.image_delay <= 0.0:
                woman = self.illusion_woman_image
            else:
                woman = self.frown_image
        else:
            woman = self.illusion_woman_image
        
        if self.transition_state == 3 or self.transition_state == 7 or (self.transition_state == 5 and self.previous_state == 3):
            # flip the woman image horizontally
            woman = pygame.transform.flip(woman, True, False)
            surface.blit(woman, (500, 0))
            
        elif self.transition_state != 4 and self.transition_state != 6:     
            surface.blit(woman, (0, 0))
    
    def drawUI(self, surface):
        
        if self.promptDelay > 0.0:
           # Render text box ui and options for user
            surface.blit(self.scaled_dialogueBox, (0, 150))
            
            # Draw clickable text options
            for option in self.clickable_options[self.transition_state]:
                option.draw(surface)
            
            self.create_text_box(surface, self.previous_prompt, self.font) 
        
        else:
            
            super().drawUI(surface)
            
            if self.combat_outcome == 1:
                self.draw_prompt("You have advanced two cultivation stages!", 535, 600, None)
     
    def update_image(self, image):
        if image is not None:
            self.previous_image = self.image
            self.image = image   
    
    def initialize_glitch(self, surface, glitch_image, intervals:int, duration:float, num_of_glitches:int, max_size_of_glitch:int):
        
        glitch_duration = duration / intervals
        
        # Create a temporary surface to draw the glitch effect on
        glitch_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
        # Determine the glitch state based on current image_delay
        glitch_state = int(self.image_delay / glitch_duration) % 2
        
        if glitch_state == 1:
            self.mask_surface.fill((0, 0, 0, 0))
        
            self.create_glitch_mask(self.mask_surface, num_glitches=1, max_size=50)
        
            # Apply the burn-through effect to the static image
            image = self.glitch_effect(glitch_image, self.image, self.mask_surface)
            
        else:
            image = self.image
            
        #surface.fill((0, 0, 0))
        glitch_surface.blit(image, (0, 0))
        # Draw the static image on the screen
        surface.blit(glitch_surface, (0, 0))
        #surface.blit(image, (0, 0))
    
    def glitch_effect(self, foreground_image, background_image, mask_surface):
        # Apply the glitch mask to the foreground image using the BLEND_RGBA_MULT blending mode
        glitched_foreground = foreground_image.copy()
        glitched_foreground.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Apply the background image to the glitched foreground image with transparency
        glitched_foreground.blit(background_image, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        return glitched_foreground
        
    def create_glitch_mask(self, surface, num_glitches, max_size):
        for _ in range(num_glitches):
            glitch_size = random.randint(1, max_size)
            x = random.randint(0, surface.get_width() - glitch_size)
            y = random.randint(0, surface.get_height() - glitch_size)
            pygame.draw.rect(surface, (100, 100, 100), pygame.Rect(x, y, glitch_size/2, glitch_size*100))

class FinalTrial (Scene):
    def __init__(self, scene_manager:SceneManager) -> None:
        
        # Image and text variables
        self.prompt = self.dialogue['final trial']['prompt'][0]
        self.image = pygame.image.load('images/porcupine-demon.png')
        self.golden_core = pygame.image.load('images/golden-core.png')
        self.desturction_core = pygame.image.load('images/destruction-core.png').convert_alpha()
        self.death_prompt = "Dead."
        
        # Set initial alpha value (0 = fully transparent, 255 = fully visible)
        self.alpha = 0
        
        # Scene Manager reference
        self.scene_manager = scene_manager
        
        # Combat variables
        self.combat_one = 0 # Flag for whether the first combat scene was fought
        self.combat_outcome = None # Updated by the scene manager class after combat
        
        # Font
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Scene transition state variable
        self.transition_state = 0
       
        # Previous state variables 
        self.previous_image = None
        self.previous_state = 0
        self.previous_prompt = None
        
        # Delays in seconds
        self.drawUIDelay = 1.0
        self.promptDelay = 0.0
        self.image_delay = 0.0
        
        # Clickable options
        self.clickable_options = [
            # state 0 - boss battle
            [
                Clickable_text("Fight for the millenium-old cosmic fruit.", 560, 670, self.font, (0, 0, 0), 'combat')
            ],
            # state 1 - victory scene
            [
                Clickable_text("Exit the trial grounds.", 655, 670, self.font, (0, 0, 0), 'next')
            ],
            # state 2 - corrupted core scene
            [
                Clickable_text("Trek onwards.", 670, 670, self.font, (0, 0, 0), 'end')
            ]
        ]
        
        # sets the first scene option to visible
        self.initialize_options()
    
    def next_prompt_state(self):
        
        # Update to the corrupted core scene and setup the corruption effect
        self.updateTransitionState(1)
        self.prompt = self.dialogue['final trial']['prompt'][2]
        
    def drawScene(self, surface):
    
        super().drawScene(surface)
        
        # Slowly have the red spiritual core take over the image of the regular golden core
        if self.transition_state == 2:
            self.corruption_effect(surface)
        
        
    def start_combat(self):
        
        if self.combat_one == 0:
            monster = Character()
        
        # Create porcupine boss combat scene and return it to the scene manager  
        combat_scene = CombatScene(monster, self.image, self.scene_manager)
        combat_scene.set_previous_scene('final-trial')
        return combat_scene
    
    def end_combat(self, combat_outcome):
        
        if combat_outcome == 1:
            
            self.combat_outcome = combat_outcome
        
            # Update combat flag
            self.combat_one = 1
        
            # Update prompt
            self.prompt = self.dialogue['final trial']['prompt'][1]
            
            # Increment to victory transition state
            self.updateTransitionState(1)
            self.update_image(self.golden_core)
    
    def update_image(self, image):
        if image is not None:
            self.previous_image = self.image
            self.image = image 
            
    def corruption_effect(self, surface:pygame.Surface):
        
        self.desturction_core.set_alpha(self.alpha)
        surface.blit(self.desturction_core, (0, 0))
        
        if self.alpha < 255:
            self.alpha += 2
        else:
            self.alpha = 255

class EndScene(Scene):
    def __init__(self) -> None:
        # Image and text variables
        self.prompt = self.dialogue['end']['prompt'][0]
        self.image = pygame.image.load('images/end-view.png')
        self.end_button = self.startButton
        
        # Set initial alpha value (0 = fully transparent, 255 = fully visible)
        self.alpha = 0
        
        # Font
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        self.defaultF = self.font
        self.haseyo = pygame.font.Font(self.Haseyo_font, 35)
        
        # Scene transition state variable
        self.transition_state = 0
       
        # Previous state variables 
        self.previous_image = None
        self.previous_state = 0
        self.previous_prompt = None
        
        # Delays in seconds
        self.drawUIDelay = 1.0
        self.promptDelay = 0.0
        self.image_delay = 0.0
        
        # Clickable options
        self.clickable_options = [
            # state 0 - end scene
            [
                Clickable_text("Continue.", 675, 670, self.defaultF, (0, 0, 0), 'next')
            ],
            [
                Clickable_text("End Adventure.", 610, 605, self.haseyo, (0, 0, 0), 0)
            ]
        ]
        
        # sets the first scene option to visible
        self.initialize_options()
    
    def next_prompt_state(self):
        self.updateTransitionState(1)
        
    def drawUI(self, surface):
        
        if self.transition_state == 0:
            super().drawUI(surface)
            
        else:
            # Draw exit button
            surface.blit(self.end_button, (500, 580))
            
            # Draw clickable text options for end scene
            for option in self.clickable_options[self.transition_state]:
                if option is not None:
                    option.draw(surface)     
                               
class CombatScene (Scene):
    
    # Add a defence UI bar to show the player their current defence
    def __init__(self, opponent, monster_image, scene_manager):
        
        # Scene image and prompt 
        self.prompt = ""
        self.image = monster_image
        self.drawUIDelay = 0.0
        
        # Scene manager reference
        self.scene_manager = scene_manager
        
        # Combat UI elements
        self.combat_tag = self.resize_image(pygame.image.load('images/combat-ui-name.png'), 1.3, 1.3)
        self.combat_options_menu = self.resize_image(pygame.image.load('images/combat-options-scroll.png'), 2, 3)
        self.monster_tag = self.resize_image(self.startButton, 1.5, 1.5)
        
        # Font
        self.font_path = self.Haseyo_font
        self.font = pygame.font.Font(self.font_path, 30)
        
        # Combat Variables
        self.combat = None 
        self.combat_outcome = None
        self.player = None
        self.opponent = opponent
        self.combat_active = False
        
        # State and scene holders
        self.transition_state = 0
        self.previous_state = 0
        self.previous_scene = None
        
        options_x = 1028
        self.clickable_options = [
            [
                Clickable_text("Attack", options_x - 6, 600, self.font, (0, 0, 0), "Attack"),
                Clickable_text("Defend", options_x - 12, 640, self.font, (0, 0, 0), "Defend"),
                Clickable_text("Flee", options_x + 5, 680, self.font, (0, 0, 0), "Flee")
            ],
            [
                Clickable_text("Attack", options_x - 6, 615, self.font, (0, 0, 0), "Attack"),
                Clickable_text("Defend", options_x - 12, 660, self.font, (0, 0, 0), "Defend")
            ]
        ]
        
        self.initialize_options()
    
    def start_combat(self):
        
        # Change combat options to those without the flee option since the mini boss and final boss battles are unfleeable
        print(self.previous_scene)
        if self.previous_scene != 'destruction':
            self.updateTransitionState(1)
            
        self.combat_active = True
        scene_manager_obj = SceneManager()
        self.player = scene_manager_obj.get_character()
        self.combat = Combat(self.player, self.opponent)
        
    def process_events(self, events):
        
        # Current mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Creates color change hover effect
        for option in self.clickable_options[self.transition_state]:
            option.hovering(mouse_pos)
            
        # Checks for mouse input
        for event in events:
            
            if event.type == pygame.QUIT:
                pygame.quit()
                  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                for option in self.clickable_options[self.transition_state]:
                    
                    if event.button == 1 and option.was_clicked(mouse_pos):
                        print("Combat option clicked")
                        
                        if option.scene == "Attack":
                            self.combat.set_player_action("Attack")
                            self.combat_outcome = self.combat.initiate_combat()
                            
                        elif option.scene == "Defend":
                            self.combat.set_player_action("Defend")
                            self.combat_outcome = self.combat.initiate_combat()
                            
                        else:
                            self.combat.set_player_action("Flee")
                            self.combat_outcome = self.combat.initiate_combat()
                           
        if self.combat is None:
            self.start_combat()
        elif self.combat_active:
            pass
            
        if self.combat_outcome is not None:
            self.combat_active == False
            
            if self.combat_outcome == 1:
                self.handle_player_victory()
            elif self.combat_outcome == 0:
                self.handle_player_death()
            else:
                self.handle_player_fled()

    def drawUI(self, surface):

        # player Hp bar dimensions
        bar_x = 468
        bar_y = 640
        default_width = 520
        bar_width = self.update_hp_bar(self.player, default_width)  
        bar_height = 50
        
        # # player current HP, and x,y position
        # if self.player is not None:
        #     player_hp = self.player.getHP()
        # else:
        #     player_hp = 0
        # player_hp_x = 790
        # player_hp_y = 655
        
        # # Sets the hp text color based on current hp
        # if player_hp_x > bar_width:
        #     hp_text_color = (255, 255, 255)
        # else:
        #     hp_text_color = (0, 0, 0)
        
        # # Renders the current player HP for later drawing
        # hp_text_surface = self.font.render(str(player_hp), True, hp_text_color)
        
        # Monster hp bar dimensions
        monster_bar_x = 468
        monster_bar_y = 45
        monster_hp_default_width = 500
        monster_bar_width = self.update_hp_bar(self.opponent, monster_hp_default_width)
        monster_bar_height = 40
        #monster_hp = self.opponent.getHP()
        
        # Renders player combat UI such as name tag, health bar, and combat options scroll
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, default_width, bar_height))
        pygame.draw.rect(surface, (175, 53, 78), (bar_x + 10, bar_y + 5, bar_width - 15, bar_height - 10))
        #surface.blit(hp_text_surface, (player_hp_x, player_hp_y))
        surface.blit(self.combat_tag, (90, 272))
        surface.blit(self.combat_options_menu, (818, 500))
        
        # Render player name
        name = self.font.render("Player", True, (0, 0, 0), None)
        surface.blit(name, (450, 650))
        
        # Renders monster combat UI such as monster name and health bar
        pygame.draw.rect(surface, (0, 0, 0), (monster_bar_x , monster_bar_y, monster_hp_default_width, monster_bar_height))
        pygame.draw.rect(surface, (175, 53, 78), (monster_bar_x + 4, monster_bar_y + 4, monster_bar_width - 10, monster_bar_height - 8))
        surface.blit(self.monster_tag, (568, 0))
        
        # Render monster name
        monster_name = self.font.render("Monster", True, (0, 0 ,0), None)
        surface.blit(monster_name, (643, 20))
        
        option_group = self.clickable_options[self.transition_state]
        # Draw clickable text options
        for option in option_group:
            option.draw(surface)
    
        self.surface = surface

    def update_hp_bar(self, entity, width):
        
        if self.player is not None:
            bar_width = (entity.getHP() / entity.get_max_hp()) * width
        else:
            bar_width = width
            
        return bar_width
                           
    def set_previous_scene(self, sceneID):
        self.previous_scene = sceneID
        
    def handle_player_victory(self):
        print("Player Won.")
        self.scene_manager.transition_to_scene(self.previous_scene)
            
    def handle_player_death(self):
        print("Player Died") 
        self.scene_manager.transition_to_death('''As your vision fades to darkness you find yourself inside of a 
                                               hellish landscape, with no end in sight. From your fragmented memories and the 
                                               stories of immortals you've heard since young, you piece together that you are 
                                               in the mythical underworld. Perhaps you can find a way to reincarnate.''')
        
    def handle_player_fled(self):
        print("Player Fled")
        self.scene_manager.transition_to_scene(self.previous_scene)
       
class DeathScene (Scene):
    
    def __init__(self, prompt):
        
        # Scene image and prompt 
        self.prompt = prompt
        self.image = pygame.image.load('images/death-world.png')
        self.drawUIDelay = 0.0
        
        # Font
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # State and scene holders
        self.transition_state = 0
        self.previous_state = 0
        self.previous_scene = None
        
        self.clickable_options = [
            [
                Clickable_text("Begin anew.", 665, 640, self.font, (0, 0, 0), 'start'),
                Clickable_text("Exit.", 697, 670, self.font, (0, 0, 0), 0)
            ]
        ]
        
        self.initialize_options()
        
        

        