import logging
import os

logger = logging.getLogger(__name__)


class Library(object):
    def __init__(self, base_path):
        self._base_path = os.path.expanduser(base_path)
        self._libraries = list()
        self._current_library = 0
        self._current_song = -1

    def __enter__(self):
        self._scan_library()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def library(self):
        return self._current_library

    @library.setter
    def library(self, value):
        self._current_library = value % len(self._libraries)
        self._current_song = -1

    @property
    def song(self):
        return self._libraries[self._current_library][self._current_song]

    def next(self):
        self._current_song = (self._current_song + 1) % len(self._libraries[self._current_library])

    def _scan_library(self):
        self._libraries.clear()

        logger.info('loading audio library %s', self._base_path)
        for directory in sorted(os.listdir(self._base_path)):
            directory = os.path.join(self._base_path, directory)
            if not os.path.isdir(directory):
                continue

            logger.info('adding songs from directory %s', directory)
            self._libraries.append(list(os.path.join(directory, file) for file in sorted(os.listdir(directory))
                                        if os.path.isfile(os.path.join(directory, file))
                                        and file.lower().endswith('.ogg')))

    def __str__(self):
        return '%s' % self._libraries
