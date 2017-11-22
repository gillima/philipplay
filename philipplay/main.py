#!/usr/bin/env python3
import logging
import signal
import threading

from philipplay.controller import Controller
from philipplay.library import Library
from philipplay.player import Player

logger = logging.getLogger(__name__)
shutdown = threading.Event()


def signal_handler(signal, frame):
    logger.info('Shutting down audio player')
    shutdown.set()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGINT, signal_handler)
    with Player(fadeout=.5) as player, Library('~/Music/') as library, Controller(player, library, event=shutdown) as controller:
        logger.info('Press Q to shutdown')
        shutdown.wait()
