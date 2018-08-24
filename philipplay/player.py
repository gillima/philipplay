import logging
import time

import pygame
from pygame import mixer

logger = logging.getLogger(__name__)


NEXT_SONG = pygame.USEREVENT + 1
STOP = pygame.USEREVENT + 2


# noinspection PyArgumentList
class Player(object):
    """
    Simple audio player which used `pygame.mixer` to play audio files.
    """
    def __init__(self, **kwargs):
        """
        Initializes a new instance of the :class:`Player` class.

        :param float fadeout: Fadeout time in seconds when switch to next song
        """
        self._fadeout = int(kwargs.get('fadeout', .5) * 1000)

    @property
    def volume(self):
        """Gets the current volume of the audio player"""
        return mixer.music.get_volume()

    @volume.setter
    def volume(self, value):
        """Sets the volume of the audio player"""
        value = min(1, max(0, value))
        logger.info('set volume %s', value)
        mixer.music.set_volume(value)

    def __enter__(self):
        """Setup the system to allow playing of audio files"""
        mixer.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops the audio player, and terminates all related threads"""
        self.stop()
        mixer.quit()

    def play(self, filename):
        """
        Plays the given file. If another file is currently played,
        the song will be faded out before the new song is started

        :param str filename: Absolute path to the audio file to be played
        """
        self.stop()
        if not filename:
            return

        logger.info('play song %s', filename)
        mixer.music.set_endevent(NEXT_SONG)
        mixer.music.load(filename)
        mixer.music.play()

    def stop(self):
        """Stops any file which is currently played by the audio player"""
        if not mixer.music.get_busy():
            return

        mixer.music.set_endevent(STOP)
        logger.debug('fade out song in %s [ms]', self._fadeout)
        mixer.music.fadeout(self._fadeout)
        while mixer.music.get_busy():
            time.sleep(.1)

        mixer.music.stop()
        logger.info('song stopped')

