import pygame
from pygame import mixer

from abc import ABC, abstractmethod
from typing import Any


from time import sleep
from _types import EventInfo
from ui import Button
from player import player



class GameState(ABC):

    # You pass in `None` to use the default font
    FONT = pygame.font.Font(None, 50)

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.is_over = False

    @abstractmethod
    def update(self, event_info: EventInfo) -> None:
        pass

    @abstractmethod
    def next_game_state(self) -> Any:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


class MapScreen(GameState):
    

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)



        self.text = self.FONT.render("MAP", False, "purple")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.screen.get_rect().center

        self.load_BG = pygame.image.load("assets/images/world-map.jpg")
        self.load_BG_size = pygame.transform.scale(self.load_BG,(pygame.display.get_window_size()))

        

        self.main_menu_btn = Button(pygame.Vector2(self.screen.get_rect().centerx, 600), "MAIN MENU")

    def update(self, event_info: EventInfo) -> None:

        player.update(event_info)
        
        self.main_menu_btn.update(event_info)

        if self.main_menu_btn.clicked:
            self.is_over = True
            

   
            

    def next_game_state(self) -> Any:
        
        if self.main_menu_btn.clicked:

            player.select_character("none")

            return MainMenu

    def draw(self) -> None:
        
        self.screen.blit(self.load_BG_size,(0,0))

        self.screen.blit(self.text, (self.text_rect.x, 75))

        player.draw(self.screen)


        self.main_menu_btn.draw(self.screen)

        



class GamePrologScreen(GameState):
    

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        player = None

        self.text = self.FONT.render("PROLOG", False, "white")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.screen.get_rect().center

        self.load_BG = pygame.image.load("assets/images/Vereden2.png")
        self.load_BG_size = pygame.transform.scale(self.load_BG,(pygame.display.get_window_size()))

        
        self.prolog_choice1 = Button(pygame.Vector2(self.screen.get_rect().centerx, 100), "Mage")

        self.prolog_choice2 = Button(pygame.Vector2(self.screen.get_rect().centerx, 200), "Archer")

        self.prolog_choice3 = Button(pygame.Vector2(self.screen.get_rect().centerx, 300), "Warrior")

        self.main_menu_btn = Button(pygame.Vector2(self.screen.get_rect().centerx, 450), "MAIN MENU")

    def update(self, event_info: EventInfo) -> None:
        
        self.main_menu_btn.update(event_info)
        self.prolog_choice1.update(event_info)
        self.prolog_choice2.update(event_info)
        self.prolog_choice3.update(event_info)

        if self.main_menu_btn.clicked or self.prolog_choice1.clicked:
            self.is_over = True
            

    def next_game_state(self) -> Any:
        
        if self.main_menu_btn.clicked:
            return MainMenu

        elif self.prolog_choice1.clicked:

            player.select_character("mage")

            return MapScreen

    def draw(self) -> None:
        self.screen.blit(self.text, (self.text_rect.x, 100))
        self.screen.blit(self.load_BG_size,(0,0))

        self.prolog_choice1.draw(self.screen)

        self.prolog_choice2.draw(self.screen)

        self.prolog_choice3.draw(self.screen)

        self.main_menu_btn.draw(self.screen)

        if player is not None:
            player.draw(self.screen)


class GameLoadScreen(GameState):
    

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.stop_menu_music = mixer.music.stop()

        self.load_load_music = mixer.music.load("assets/music/dagger.mp3")

        self.start_load_music = mixer.music.play()

        self.load_BG = pygame.image.load("assets/images/Vereden2.png")
        self.load_BG_size = pygame.transform.scale(self.load_BG,(pygame.display.get_window_size()))

        self.text = self.FONT.render("LOAD SCREEN", False, "white")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.screen.get_rect().center

        
        self.newgame_btn = Button(pygame.Vector2(self.screen.get_rect().centerx, 300), "NEW GAME")

        self.loadgame_btn = Button(pygame.Vector2(self.screen.get_rect().centerx, 350), "LOAD GAME")

        self.main_menu_btn = Button(pygame.Vector2(self.screen.get_rect().centerx, 450), "MAIN MENU")

    def update(self, event_info: EventInfo) -> None:
        self.main_menu_btn.update(event_info)
        self.newgame_btn.update(event_info)
        self.loadgame_btn.update(event_info)
    
        if self.main_menu_btn.clicked \
            or self.newgame_btn.clicked \
            or self.loadgame_btn.clicked:
                self.is_over = True


    

    def next_game_state(self) -> Any:
        
        if self.newgame_btn.clicked:

            return GamePrologScreen
        
        elif self.main_menu_btn.clicked:
            return MainMenu

    def draw(self) -> None:
        
        self.screen.blit(self.load_BG_size,(0,0))

        self.screen.blit(self.text, (self.text_rect.x, 100))

        self.newgame_btn.draw(self.screen)



        self.loadgame_btn.draw(self.screen)

        self.main_menu_btn.draw(self.screen)




class MainMenu(GameState):
    """
    Main Menu for game.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

        self.mixer_init = mixer.init()
        self.main_menu_music_load = mixer.music.load("assets/music/VEREDEN.mp3")
        self.main_menu_music_play = mixer.music.play()

        self.main_menu_BG = pygame.image.load("assets/images/Vereden.jpg")
        self.main_menu_BG_size = pygame.transform.scale(self.main_menu_BG,(pygame.display.get_window_size()))

        self.text = self.FONT.render("MAIN MENU", False, "white")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.screen.get_rect().center

        self.start_btn = Button(pygame.Vector2(self.screen.get_rect().centerx, 200), "START")

        self.quit_btn = Button(pygame.Vector2(self.screen.get_rect().centerx, 400), "Quit")

    def update(self, event_info: EventInfo) -> None:
        self.start_btn.update(event_info)
        self.quit_btn.update(event_info)
        
        if self.start_btn.clicked or self.quit_btn.clicked:
            self.is_over = True
        

    def next_game_state(self):
        if self.start_btn.clicked:
            return GameLoadScreen
        
        elif self.quit_btn.clicked:
            self.exit = pygame.QUIT
            raise SystemExit

    def draw(self) -> None:
        self.screen.blit(self.main_menu_BG_size,(0,0))

        self.screen.blit(self.text, (self.text_rect.x, 100))


        self.start_btn.draw(self.screen)

        self.quit_btn.draw(self.screen)




