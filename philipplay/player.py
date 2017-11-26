import logging
import time

import pygame
from pygame import mixer

logger = logging.getLogger(__name__)


NEXT_SONG = pygame.USEREVENT + 1
STOP = pygame.USEREVENT + 2


class Player(object):

    def __init__(self, **kwargs):
        self._fadeout = int(kwargs.get('fadeout', 1) * 1000)

    @property
    def volume(self):
        return mixer.music.get_volume()

    @volume.setter
    def volume(self, value):
        value = min(1, max(0, value))
        logger.info('set volume %s', value)
        mixer.music.set_volume(value)

    def __enter__(self):
        mixer.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        mixer.quit()

    def play(self, filename):
        self.stop()
        logger.info('play song %s', filename)
        mixer.music.set_endevent(NEXT_SONG)
        mixer.music.load(filename)
        mixer.music.play()

    def stop(self):
        if not mixer.music.get_busy():
            return

        mixer.music.set_endevent(STOP)
        logger.debug('fade out song in %s [ms]', self._fadeout)
        mixer.music.fadeout(self._fadeout)
        while mixer.music.get_busy():
            time.sleep(.1)

        mixer.music.stop()
        logger.info('song stopped')

