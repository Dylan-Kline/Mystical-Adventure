import pygame
from utilitiesMA import Clickable_text

class Scene:
    
    # File path for font library
    Haseyo_font = "Fonts\\AnnyeongHaseyo.ttf"
    eternity_font = "Fonts/Eternity.ttf"
    medusa_font = "Fonts/Medusa.otf"
    default_font = None
    
    # Image path for UI
    dialogueBox = pygame.image.load('images/UI-textbox.png')
    scaled_dialogueBox = pygame.transform.scale(dialogueBox, (1456, 816))
    
    # Image paths for scenes
    loadScreen = pygame.image.load('images/start-screen.png')
    temple_entrance = pygame.image.load('images/temple-entrance.png')
    leaving_image = pygame.image.load('images/leaving-trail.jpg')
    trial_gate = pygame.image.load('images/trial-gate.png')
    platform = pygame.image.load('images/trial1-portals.png')
    
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
        "start":
            {
                'prompt':"Before you looms a dreadful gate radiating spiritual energy. Your fellow sect members were right, the trial grounds of the Abyss truly exist." +
                            " Should you take the risk of undergoing the trial?",
                'options':['Enter the gate regardless of the potential danger...', 'Leave in haste and head back to the safety of the sect.']
            },
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
                'prompt':"Everything you wish to accomplish is on the other side of fear.",
                'options':['Return with renewed vigor.', 'Continue back to the sect...']
            },
        "gate":
            {
                'prompt':"You step inside, and before you looms a dreadful temple archway radiating a foreboding red glow. " +
                            "Sinister carvings of demonic creatures adorn the surroundings, and ancient etchings line the temple pillars." +
                            " The rumors among your sect members were right, the trial grounds of the abyss truly exist.",
                'options':['Enter the archway regardless of the potential danger...', 'Examine the etchings', 'Search the room']
                # when you examine the etchings you find out that the trial is made up of three trials
            },
        "trial1": #add another scene before the gat scene where you are traveling along a path and you arrive to a abyssal cathedral
            {
                'prompt':"Entering the gate you find yourself faced with an expansive dark room with a stone platform in the center, with what looks like two portals" +
                            " situated on each side, one glowing white, and one pitch black." +
                            " You make out the words above each portal, 'Life' and 'Death' respectively.",
                'options':['Life', 'Death']
            },
        "life portal":
            {
                'prompt':"Dark wisps swirl around the surrounding space, and screams of the damned fill your ears. You notice that your spirit is slowly dwindling. " +
                            "Reminding you of your Master's advice to never let you spirit drop below a quarter, lest you wish to die a slow death.",
                'options':['Power through the dreadful atmosphere and use it to temper your soul.', 'Head back through the portal.']
            },
        "death portal":
            {
                'prompt':"Before you looms a dreadful gate radiating spiritual energy. Your fellow sect members were right, the trial grounds of the Abyss truly exist." +
                            " Should you take the risk of undergoing the trial?",
                'options':['Enter the gate regardless of the potential danger...', 'Leave in haste and head back to the safety of the sect.']
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
        for option in self.clickable_options:
            option.hovering(mouse_pos)
    
        # Checks for mouse or keyboard input
        for event in events:
            
            if event.type == pygame.QUIT:
                pygame.quit()
                  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                try:
                    
                    for option in self.clickable_options:
                        if event.button == 1 and option.was_clicked(mouse_pos):
                            print("Option clicked")
                            
                            if option.scene is not None:
                                
                                if option.scene == 0:
                                    
                                    pygame.quit()
                                    
                                elif option.scene == 'examine':
                                    
                                    self.examine_surroundings()
                                    
                                elif option.scene == 'previous scene':
                                    
                                    return self.previous_scene()
                                
                                else:
                                    return option.scene   
                except:
                    print("Clickable text not found. (events)")
    
    def updateTimer(self, delta_time):
        if not isinstance(self, StartScene):
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
        
    def drawUI(self, surface):
        
        if not isinstance(self, StartScene):
            
            if self.drawUIDelay <= 0:
                
                # Render text box ui and options for user
                surface.blit(self.scaled_dialogueBox, (0, 150))
                
                # Draw clickable text options
                if len(self.clickable_options) < 4:
                    for option in self.clickable_options:
                        option.draw(surface)
                else:
                    self.clickable_options[3].draw(surface)
                
                self.create_text_box(surface, self.prompt, self.font)
                
        else:
            # Draw clickable text options for start scene
            for option in self.clickable_options:
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
        
        # Redraw the text box to clear it
        self.surface.blit(self.scaled_dialogueBox, (0, 150))
        
        # Draw clickable text options
        self.clickable_options[3].draw(self.surface)
        
        # Draw text prompt
        self.create_text_box(self.surface, self.prompt, self.font)
        
    def previous_scene(self):
        
        # Restore the previous prompt
        self.prompt = self.previous_prompt
        
        # Remove the clickable option for going back
        self.clickable_options = [option for option in self.clickable_options if option.scene != "previous scene"]
        
        # Return the scene ID of the previous scene
        return self.previous_scene_id
   
class SceneManager:
    def __init__(self) -> None:
        self.scenes = {
            'start': StartScene,
            'temple': TempleScene,
            'gate': GateScene,
            'trial1': Trial1,
            'coward': CowardScene
        }
        self.previous_scenes = list()
        self.current_scene = None
        
    def transition_to_scene(self, sceneID):
        
        # Grab scene class based on sceneID
        scene_class = self.scenes.get(sceneID)
        
        if scene_class:
            # Check if the scene class already exists in previous scenes list
            for scene in self.previous_scenes:
                if isinstance(scene, scene_class):
                    
                    # If the scene being transitioned to is the start scene, reset the previous scenes list
                    if isinstance(scene, StartScene):
                        self.previous_scenes.clear()
                        
                    self.current_scene = scene
                    return
                    
            # If it doesn't exist, instantiate the new scene class
            scene = scene_class()
            self.previous_scenes.append(scene)
            self.current_scene = scene
        else:
            print(f"Scene with ID {sceneID} does not exist")
        
    def process_current_scene(self, events):
        
        # Process game events for the current scene, and handle scene transition requests
        nextSceneID = self.current_scene.process_events(events)
        
        # If the current scene requests a transition to another scene
        if nextSceneID:
            self.transition_to_scene(nextSceneID)

class StartScene (Scene):
    def __init__(self) -> None:
        self.start_button = "Begin Adventure"
        self.exit_button = "Exit"
        self.image = self.loadScreen
        
        # Font for text
        self.font_path = self.Haseyo_font
        self.font = pygame.font.Font(self.font_path, 35)
        
        # Option text
        self.clickable_options = []
        self.clickable_options.append(Clickable_text(self.start_button, 700, 360, self.font, "black", 'temple'))
        self.clickable_options.append(Clickable_text(self.exit_button, 720, 390, self.font, "black", 0))
    
class TempleScene (Scene):
    def __init__(self) -> None:
        self.prompt = self.dialogue['temple']['prompt']
        self.examine_text = self.dialogue['temple']['examine']
        self.options = self.dialogue['temple']['options']
        self.image = self.temple_entrance
        
        # Holds the previous scene data 
        self.previous_prompt = None
        self.previous_scene_id = 'temple'
        
        # Font for text
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        # Option text
        self.clickable_options = []
        self.clickable_options.append(Clickable_text(self.options[0], 470, 560, self.font, "black", 'gate')) # Entering temple
        self.clickable_options.append(Clickable_text(self.options[1], 470, 600, self.font, "black", 'examine')) # Examine surroundings
        self.clickable_options.append(Clickable_text(self.options[2], 470, 640, self.font, "black", 'coward')) # Leave to sect
        
    def examine_surroundings(self):
        
        # Update Prompt to the examine text and create new clickable option to head back to main prompt.
        self.previous_prompt = self.prompt
        self.prompt = self.examine_text
        self.clickable_options.append(Clickable_text("Continue.", 675, 670, self.font, (0, 0, 0), 'previous scene'))
        
        # Update the text box with the new prompt 
        self.update_text_box()
              
class GateScene (Scene):
    
    def __init__(self) -> None:
        self.prompt = self.dialogue['gate']['prompt']
        self.options = self.dialogue['gate']['options']
        self.image = self.trial_gate
        
        # Font for text
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        # Option text
        self.clickable_options = []
        self.clickable_options.append(Clickable_text(self.options[0], 470, 560, self.font, "black", 'trial1'))
        self.clickable_options.append(Clickable_text(self.options[1], 470, 600, self.font, "black", 'coward'))


class CowardScene (Scene):
    
    def __init__(self) -> None:
        
        self.prompt = self.dialogue['coward']['prompt']
        self.options = self.dialogue['coward']['options']
        self.image = self.leaving_image
        
        # Font for text
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        # Text options for user
        self.clickable_options = []
        self.clickable_options.append(Clickable_text(self.options[0], 470, 560, self.font, "black", 'temple'))
        self.clickable_options.append(Clickable_text(self.options[1], 470, 600, self.font, "black", 'start'))

class Trial1 (Scene):
    
    def __init__(self) -> None:
        
        self.prompt = self.dialogue['trial1']['prompt']
        self.options = self.dialogue['trial1']['options']
        self.image = self.platform
        
        self.font_path = self.default_font
        self.font = pygame.font.Font(self.font_path, 27)
        
        # Dialogue box delay in seconds
        self.drawUIDelay = 1.0
        
        self.clickable_options = []
        self.clickable_options.append(Clickable_text(self.options[0], 470, 560, self.font, "black", 'life'))
        self.clickable_options.append(Clickable_text(self.options[1], 470, 600, self.font, "black", 'death'))
         
class Life (Scene):
    
    def __init__(self) -> None:
        pass
    
class Death (Scene):
    
    def __init__(self) -> None:
        pass
