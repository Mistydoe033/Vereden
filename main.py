import asyncio

import pygame

from _types import EventInfo
from states import MainMenu, GameLoadScreen





class Game:
    """
    Handle flow in pygame application
    """
    
    FPS_CAP = 60
    CLOCK = pygame.time.Clock()

    def __init__(self):
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.current_game_state = MainMenu(self.screen)
        self.caption = pygame.display.set_caption("Vereden")

    def get_events(self) -> EventInfo:
        """
        Returns necessary events for application. Packed in a dictionary.
        """

        events = pygame.event.get()
        mouse_press = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        raw_dt = self.CLOCK.get_time()
        dt = raw_dt * self.FPS_CAP

        return {
            "events": events,
            "mouse press": mouse_press,
            "keys": keys,
            "mouse pos": mouse_pos,
            "raw dt": raw_dt,
            "dt": dt,
            "screen": self.screen
        }

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        while True:
            event_info = self.get_events()
            for event in event_info["events"]:
                if event.type == pygame.QUIT:
                    raise SystemExit

            self.current_game_state.update(event_info)
            if self.current_game_state.is_over:
                self.current_game_state = self.current_game_state.next_game_state()(
                    self.screen
                )

            self.screen.fill("black")
            self.current_game_state.draw()

            self.CLOCK.tick(self.FPS_CAP)
            pygame.display.flip()
            await asyncio.sleep(0)


if __name__ == "__main__":
    game = Game()
    game.run()
