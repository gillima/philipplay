import logging
import threading

import pygame

from philipplay.keyboard import Keyboard
from philipplay.player import NEXT_SONG

logger = logging.getLogger(__name__)


class Controller(threading.Thread):
    def __init__(self, player, library, event):
        """
        Initializes a new instance of the :class:`Controller` class.

        :param philipplay.player.Player player: Audio player
        :param philipplay.library.Library library: Audio library to play songs from
        :param threading.Event event: Event to shutdown the whole application
        """
        threading.Thread.__init__(self, target=self._run, name='philipplay-eventloop')
        self._player = player
        self._library = library
        self._event = event

    def __enter__(self):
        """Starts the controller and all needed subtasks"""
        logger.debug('Attach keyboard listener')
        self._keyboard = Keyboard()
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops the controller and cleanup all subtasks"""
        logger.debug('Detach keyboard listener')
        self._event.set()
        self.join()
        self._keyboard.set_normal_term()

    # noinspection PyUnusedLocal
    def _on_press(self, key, mods):
        """Handles key press events from pygame"""
        try:
            if key == pygame.K_UP:
                self._player.volume += .1
            elif key == pygame.K_DOWN:
                self._player.volume -= .1

            elif key == pygame.K_0:
                self._player.stop()
            elif pygame.K_1 <= key <= pygame.K_9:
                self._select_song(key - pygame.K_0 - 1)

            elif key == pygame.K_q:
                logger.debug('Shutdown')
                self._event.set()

        except Exception as ex:
            logger.error(ex)

    def _select_song(self, index):
        """Selects the song and used the player to play it"""
        logger.debug('Select song %s', index)
        if self._library.library != index:
            self._library.library = index

        self._library.next()
        self._player.play(self._library.song)

    def _run(self):
        """Main loop of the controller"""

        while not self._event.is_set():
            for event in pygame.event.get():
                if event.type == NEXT_SONG:
                    self._library.next()
                    self._player.play(self._library.song)
            else:
                if self._keyboard.key_pressed():
                    key = self._keyboard.get_char()
                    self._on_press(key, 0)

            pygame.time.wait(0)
