import logging
import os

from watchdog.events import FileCreatedEvent, RegexMatchingEventHandler, FileMovedEvent, DirCreatedEvent, DirMovedEvent
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


class SongList(object):
    def __init__(self, directory, songs):
        self.directory = directory
        self.songs = songs


class Library(RegexMatchingEventHandler):
    def __init__(self, **kwargs):
        """
        Initializes a new instance of the :class:`Library` class.
        """
        self._supported = kwargs.get('supported', ['.mp3', '.ogg'])
        self._base_path = os.path.join(os.path.expanduser(kwargs.get('base_path', '~/Music')), '')
        self._libraries = list()
        self._current_library = 0
        self._current_song = -1
        self.on_changed = lambda *a, **kw: None

        regex = r'{root_dir}.*?\/.*?\.({extensions})'.format(
            root_dir=self._base_path.replace('/', '\/'),
            extensions='|'.join(self._supported))
        super(Library, self).__init__(regexes=[regex])

    def __enter__(self):
        """Starts the song library"""
        self._rescan_library()
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
        if self._current_library >= len(self._libraries):
            return
        if self._current_song >= len(self._libraries[self._current_library]):
            return
        return self._libraries[self._current_library][self._current_song]

    def next(self):
        """Selects the next song in the current song library"""
        if not self._libraries:
            return
        self._current_song = (self._current_song + 1) % len(self._libraries[self._current_library])

    def _rescan_library(self):
        """Scans the root directory for song libraries"""
        self._libraries.clear()

        logger.info('loading audio library %s', self._base_path)
        if not os.path.isdir(self._base_path):
            logger.info('audio library is empty')
            self.on_changed()
            return

        for index, directory in enumerate(sorted(os.listdir(self._base_path))):
            directory = os.path.join(self._base_path, directory)
            if not os.path.isdir(directory):
                continue

            logger.info('adding songs from directory %s', directory)
            self._libraries.append(sorted(
                [os.path.join(directory, file)
                 for file in os.listdir(directory)
                 if os.path.isfile(os.path.join(directory, file))
                 and os.path.splitext(file.lower())[1] in self._supported]
            ))

        self.library = self._current_library
        self.on_changed()

    def on_any_event(self, event):
        if isinstance(event, (DirCreatedEvent, DirMovedEvent)):
            if os.path.join(event.src_path, '') == self._base_path:
                self._rescan_library()

        elif isinstance(event, FileCreatedEvent):
            self._on_file_created(str(event.src_path))

        elif isinstance(event, FileMovedEvent):
            self._on_file_removed(str(event.src_path))
            self._on_file_created(str(event.dest_path))

    def _on_file_removed(self, file_path):
        changed = False
        for index, library in enumerate(self._libraries[:]):
            if file_path in library:
                logger.info('remove song from directory %s', file_path)
                library.remove(file_path)
                changed = True
                if not library:
                    self._libraries.remove(library)

        self.on_changed()

    def _on_file_created(self, file_path):
        dir_name, file_name = os.path.split(file_path)
        if not dir_name.startswith(self._base_path):
            return

        library = [i for i, x in enumerate(self._libraries) if x[0].startswith(dir_name)]
        if len(library) > 1:
            logging.warning('can\'t add song, multiple libraries matches: %s', file_path)
            return

        if len(library) == 0:
            logging.info('add new library: %s', dir_name)
            self._libraries.append([file_path])
            self._libraries = sorted(self._libraries)
            self.on_changed()
            return

        index = library[0]
        if file_path not in self._libraries[index]:
            logging.info('add song to library: %s', file_path)
            library = self._libraries[index]
            library.append(file_path)
            self._libraries[index] = sorted(library)
            self.on_changed()

    def __str__(self):
        return '%s' % self._libraries
