#!/usr/bin/env python3
import argparse
import logging
import logging.config
import signal
import threading

import os
import pygame
import yaml

from philipplay.controller import Controller
from philipplay.library import Library
from philipplay.player import Player

logger = logging.getLogger('philipplay')
shutdown = threading.Event()


# noinspection PyUnusedLocal
def signal_handler(signal_number, frame):
    """Signal handler to intercept SIGINT"""
    shutdown.set()


def setup_parser():
    """Setup the command line argument parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Path to the configuration file')
    return parser


def setup_environment():
    """Setup the pygame environment"""
    logging.debug('setup pygame environment')
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    signal.signal(signal.SIGINT, signal_handler)


def parse_main():
    """The application main entry point"""
    parser = setup_parser()
    args = parser.parse_args().__dict__
    config_path = args.get('config', None) or '/etc/philipplay.yaml'
    with open(config_path, 'r') as config_file:
        config, log_config = yaml.load_all(config_file)
    logging.config.dictConfig(log_config)

    setup_environment()
    with Player(**config) as player, Library(**config) as library, Controller(player, library, event=shutdown):
        logger.info('Press Q to shutdown')
        shutdown.wait()
        logger.info('Shutting down audio player')


if __name__ == '__main__':
    parse_main()
