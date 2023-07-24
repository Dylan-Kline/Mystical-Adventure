import pygame
from characterMA import Character
from utilitiesMA import Clickable_text
from combatMA import Combat

# Current to do list:
# create destruction trial
# - Make monster classes for combat scenes
# - later on fine tune the combat values to make it fair
# create illusion trial
# create final boss fight
# create end scene (beautiful cliff)
# you could put a black screen with a 8 bit bite animation like in some games for the end of trial 

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
    
    # Prompts, options
    # Note to self: Make the death portal be only a 30% chance of living, and if the player lives then they gain two levels more than the life portal.
    # Or maybe I should make the life portal harder to be ironic xD. Either way my idea is to gear/level the character in various ways depending on
    # what the user chooses. This will in turn make the final trial: the boss battle easier (higher percent of winning) or harder (lower percent of winning.)
    # The general outline of the text adventure will be as follows:
    # temple -> Gate -> life/death portals-> trial 2 (choice 1 or 2) -> final trial: fight against an abyss lord/demon -> if the player wins (they get a treasure that will
    # advance their cultivation immensely, while also giving them abyssal powers (make a cutscene at the end for a cool picture of abyss energy
    # whirling around a non descript person. Then at the very end teleport the player to a cliff with a beautiful view of a mystical forest and waterfall.)
    # / Else its game over for the player and they have to restart.
    # make it so that if the player reaches the boss fight while taking the life portal, they are severely disadvangtaged and barely live after the battle.
    # for the cowards end make it so your peers eventuually overtake you and your life ends in a dasterly plot for your resources.
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
                # when you examine the etchings you find a clue for the trials to come (the etching on the left side speak of great wisdom,
                # while the etchings on the right hint at power through destruction)
                # for this scene change the discription to include the door slamming shut behind you locking you in
                # have an option for trying to find a way to escape, in which it will say 'there seems to be an Array formation blocking your way
                # you try to find a way to open the formation, however your sense of danger screams at you as you get close...quickly backing away
                # you turn towards your only way out...the gate.  
            },
        "trial1": #add another scene before the gat scene where you are traveling along a path and you arrive to a abyssal cathedral
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
                
                # trial of wisdom where a player must answer a series of thought-provoking questions and philosophical dilemmas.
                # the player's answers determine their success in gaining the portal's wisdom (aka cultivation increase)
                # have the monster give a brief summary of the type of person the player is after their answers to each question
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
                            
                            "Combat."
                            
                            ],
                'options':[['Attempt to acquire the floating rune.', 'Examine the rune.', 'Explore the surroundings.'],
                           ['Explore the cave.', 'Delve deeper into the forest.', 'Return to the runic site.']
                           ]
            },
        "waiting death":
            {
                'prompt':"You decide to test your willpower by choosing to meditate in the home of what seems to be the manifestation of death itself." +
                            " Minutes turn into hours as screams of the abyss fill your ears...",
                'options':['Enter the gate regardless of the potential danger...', 'Leave in haste and head back to the safety of the sect.']
            },
        "death portal":
            {
                'prompt':"Before you looms a dreadful gate radiating spiritual energy. Your fellow sect members were right, the trial grounds of the Abyss truly exist." +
                            " Should you take the risk of undergoing the trial?",
                'options':['Enter the gate regardless of the potential danger...', 'Leave in haste and head back to the safety of the sect.']
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
            'combat':CombatScene
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
                        
                    self.current_scene = scene
                    
                    if isinstance(self.current_scene, DestructionScene):
                        self.current_scene.end_combat()
                    return
                    
            # If it doesn't exist, instantiate the new scene class
            if scene_class == DestructionScene:
                scene = scene_class(self)  
            else: 
                scene = scene_class()
                
            self.previous_scenes.append(scene)
            self.current_scene = scene
 
        else:
            print(f"Scene with ID {sceneID} does not exist")
            
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
    
    def __init__(self, scene_manager) -> None:
        # Image and text variables
        self.prompt = self.dialogue['destruction portal']['prompt'][0]
        self.image = self.destruction_trial
        self.grey_screen = pygame.image.load('images/grey-screen.png')
        self.monster_image = pygame.image.load('images/demon-wolf')
        
        # Scene manager reference 
        self.scene_manager = scene_manager
        
        # Combat variables
        self.chance = 30 # Player's chance value to obtain the rune
        self.combat_one = 0 # Flag for whether the first combat scene was fought
        
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
                Clickable_text("Loot Draconic Wolf.", 460, 570, self.font, (0, 0, 0), 'examine'),
                Clickable_text("Explore the other path.", 460, 610, self.font, (0, 0, 0), 'explore')
            ]
        ]
        
        # sets the first scene option to visible
        self.initialize_options()
    
    def next_prompt_state(self):
        
        # Attempt to acquire rune state
        if self.transition_state == 0:
            self.prompt = self.dialogue['destruction portal']['prompt'][1]
            self.updateTransitionState(1)
            
        elif self.transition_state == 1:
            self.prompt = self.dialogue['destruction portal']['prompt'][2]
            self.updateTransitionState(1)
        
        elif self.transition_state == 2:
            if self.combat_one == 0:
                self.prompt = self.dialogue['destruction portal']['prompt'][2]
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
            
            if self.combat_one == 0:
                
                # Delete option that leads to combat scene
                self.delete_clicked_option(1, 610)
                
                # Update transition state to before combat
                self.updateTransitionState(1)
                self.update_image(self.monster_image)
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
        #combat_scene.set_previous_scene('destruction')
        return combat_scene
    
    def end_combat(self):
        
        self.combat_one = 1
        
        # Update chance to obtain rune
        self.update_chance(40)
        
        # Update prompt
        self.previous_prompt = self.prompt
        self.prompt = "hi"
        
        # Increment to victory transition state
        states_increment = 5 - self.transition_state
        self.updateTransitionState(states_increment)
        self.update_image(self.monster_image)
          
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
            
            #
    
    def process_events(self, events): 
        return super().process_events(events)
          
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
    
    def reset_image(self):
        self.image = self.destruction_trial
        
    def drawUI(self, surface):
        
        if self.combat_one != 0 and self.transition_state == 5:
            surface.blit(self.grey_screen, (0, 0))
            
        super().drawUI(surface)
        
        if self.transition_state == 1 and self.previous_state == 0:
            self.draw_prompt("Gained: +10% to chance to obtain the law rune.", 520, 610)
            
        elif self.transition_state == 1 and self.previous_state == 3:
            self.draw_prompt("Gained: +20% to chance to obtain the law rune.", 520, 645)
        
    def draw_prompt(self, prompt, x, y):
        
        if self.transition_state == 1:
            text_surface = self.font.render(prompt, True, (0, 0, 0))
            self.surface.blit(text_surface, (x, y))
 
class CombatScene (Scene):
    
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
        
        options_x = 1110
        self.clickable_options = [
            [
                Clickable_text("Attack", options_x - 6, 600, self.font, (0, 0, 0), "Attack"),
                Clickable_text("Defend", options_x - 12, 640, self.font, (0, 0, 0), "Defend"),
                Clickable_text("Flee", options_x + 5, 680, self.font, (0, 0, 0), "Flee")
            ]
        ]
        
        self.initialize_options()
    
    def start_combat(self):
        
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
        bar_x = 550
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
        monster_bar_x = 550
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
        surface.blit(self.combat_options_menu, (900, 500))
        
        # Render player name
        name = self.font.render("Player", True, (0, 0, 0), None)
        surface.blit(name, (450, 650))
        
        # Renders monster combat UI such as monster name and health bar
        pygame.draw.rect(surface, (0, 0, 0), (monster_bar_x , monster_bar_y, monster_hp_default_width, monster_bar_height))
        pygame.draw.rect(surface, (175, 53, 78), (monster_bar_x + 4, monster_bar_y + 4, monster_bar_width - 10, monster_bar_height - 8))
        surface.blit(self.monster_tag, (650, 0))
        
        # Render monster name
        monster_name = self.font.render("Monster", True, (0, 0 ,0), None)
        surface.blit(monster_name, (725, 20))
        
        # Draw clickable text options
        for option in self.clickable_options[self.transition_state]:
            option.draw(surface)
    
        self.surface = surface

    def resize_image(self, image, width_scaling_factor, height_scaling_factor):
        
        width, height = image.get_size()
        new_width = round(width / width_scaling_factor)
        new_height = round(height / height_scaling_factor)
        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))  
        
        return scaled_image
     
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
        self.scene_manager.transition_to_scene('destruction')
            
    def handle_player_death(self):
        print("Player Died") 
        
    def handle_player_fled(self):
        print("Player Fled")
        
        

        