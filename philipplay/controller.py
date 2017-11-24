import logging
import threading

import pygame

from philipplay.player import NEXT_SONG

logger = logging.getLogger(__name__)


class Controller(threading.Thread):
    def __init__(self, player, library, event):
        threading.Thread.__init__(self, target=self._run, name='philipplay-player')
        self._player = player
        self._library = library
        self._event = event

    def __enter__(self):
        logger.debug('Attach keyboard listener')
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug('Detach keyboard listener')
        self._event.set()
        self.join()

    def _on_press(self, key, mods):
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
        logger.debug('Select song %s', index)
        if self._library.library != index:
            self._library.library = index

        self._library.next()
        self._player.play(self._library.song)

    def _run(self):
        while not self._event.is_set():
            for event in  pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self._on_press(event.key, event.mod)

                if event.type == NEXT_SONG:
                    self._library.next()
                    self._player.play(self._library.song)

            pygame.time.wait(0)

