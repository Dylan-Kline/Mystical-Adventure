import pygame
from inventoryMA import Inventory
from characterMA import Character
from ScenesMA import SceneManager

def main():
    # pygame setup
    pygame.init()

    # Window Constants
    WINDOW_WIDTH = 1456
    WINDOW_HEIGHT = 816
    FPS = 60

    # Window mode and Clock
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Scene manager
    scene_manager = SceneManager()
    scene_manager.transition_to_scene('illusion')
    
    # Make another outer loop while True: to allow for restarting the game if a player dies.
    running = True # Game Status (off/on)
    while running:
        
        # timer for dialogue drawing in scene class
        delta_time = clock.tick(FPS) / 1000.0
        
        # Process events and update timer in scene class
        events = pygame.event.get()    
        scene_manager.process_current_scene(events)
        scene_manager.current_scene.updateTimer(delta_time)
        
        # Draw current scene
        scene_manager.current_scene.drawScene(screen)
        
        # Draw UI, update display and set tick rate
        scene_manager.current_scene.drawUI(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
        
             
if __name__ == "__main__":
    main()
    
