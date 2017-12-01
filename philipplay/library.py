import logging
import os

from watchdog.events import PatternMatchingEventHandler, DirModifiedEvent, DirCreatedEvent
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


class Library(PatternMatchingEventHandler):
    def __init__(self, **kwargs):
        """
        Initializes a new instance of the :class:`Library` class.
        """
        super().__init__()
        self._supported = kwargs.get('supported', ['.mp3', '.ogg'])
        self._base_path = os.path.expanduser(kwargs.get('base_path', '~/Music'))
        self._libraries = list()
        self._current_library = 0
        self._current_song = -1

    def __enter__(self):
        """Starts the song library"""
        self._scan_library()
        self._observer = Observer()
        parent = os.path.abspath(os.path.join(self._base_path, os.pardir))
        self._observer.schedule(self, path=parent, recursive=True)
        self._observer.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops the song library"""
        self._observer.stop()
        self._observer.join()

    @property
    def library(self):
        """Gets the current selected song library"""
        return self._current_library

    @library.setter
    def library(self, value):
        """Selects a song library"""
        self._current_library = value % len(self._libraries)
        self._current_song = -1

    @property
    def song(self):
        """Gets the current selected song of the current song library"""
        if not self._libraries or not self._libraries[self._current_library]:
            return
        return self._libraries[self._current_library][self._current_song]

    def next(self):
        """Selects the next song in the current song library"""
        if not self._libraries:
            return
        self._current_song = (self._current_song + 1) % len(self._libraries[self._current_library])

    def _scan_library(self):
        """Scans the root directory for song libraries"""
        self._libraries.clear()

        logger.info('loading audio library %s', self._base_path)
        if not os.path.isdir(self._base_path):
            logger.info('audio library is empty')
            return

        for directory in sorted(os.listdir(self._base_path)):
            directory = os.path.join(self._base_path, directory)
            if not os.path.isdir(directory):
                continue

            logger.info('adding songs from directory %s', directory)
            self._libraries.append(list(os.path.join(directory, file) for file in sorted(os.listdir(directory))
                                        if os.path.isfile(os.path.join(directory, file))
                                        and os.path.splitext(file.lower())[1] in self._supported))

    def on_any_event(self, event):
        if not isinstance(event, (DirModifiedEvent, DirCreatedEvent)):
            return
        if str(event.src_path).startswith(self._base_path):
            self._scan_library()

    def __str__(self):
        return '%s' % self._libraries
