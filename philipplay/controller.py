import logging

from pynput import keyboard
from pynput.keyboard import Key

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, player, library, event):
        self._player = player
        self._library = library
        self._event = event

    def __enter__(self):
        logger.debug('Attach keyboard listener')
        self._keyboard = keyboard.Listener(on_press=self._on_press)
        self._keyboard.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug('Detach keyboard listener')
        self._keyboard.__exit__(None, None, None)

    def _on_press(self, key):
        try:
            if key == Key.up:
                self._player.volume += .1
            elif key == Key.down:
                self._player.volume -= .1

            if hasattr(key, 'char'):
                if key.char == '0':
                    self._player.stop()
                elif '1' <= key.char <= '9':
                    self._select_song(ord(key.char) - ord('0') - 1)

                elif key.char.lower() == 'q':
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

