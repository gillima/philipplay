import logging
import time

from pygame import mixer

logger = logging.getLogger(__name__)


class Player(object):
    def __init__(self, **kwargs):
        self._fadeout = int(kwargs.get('fadeout', 1) * 1000)

    @property
    def volume(self):
        return mixer.music.get_volume()

    @volume.setter
    def volume(self, value):
        value = min(1, max(0, value))
        logger.debug('set volume %s', value)
        mixer.music.set_volume(value)

    def __enter__(self):
        mixer.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        mixer.quit()

    def play(self, filename):
        self.stop()
        logger.debug('play song %s', filename)
        mixer.music.load(filename)
        mixer.music.play()

    def stop(self):
        if not mixer.music.get_busy():
            return

        logger.debug('fade out song in %s [ms]', self._fadeout)
        mixer.music.fadeout(self._fadeout)
        while mixer.music.get_busy():
            time.sleep(.1)
        logger.debug('song stopped')

