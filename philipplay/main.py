#!/usr/bin/env python3
import argparse
import logging
import logging.config
import signal
import threading

import pygame
import yaml

from philipplay.controller import Controller
from philipplay.library import Library
from philipplay.player import Player

logger = logging.getLogger('philipplay')
shutdown = threading.Event()


def signal_handler(signal, frame):
    shutdown.set()


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Path to the configuration file')
    return parser


def parse_main():
    parser = setup_parser()
    args = parser.parse_args().__dict__
    config_path = args.get('config', None) or '/etc/philipplay.yaml'
    with open(config_path, 'r') as config_file:
        config, log_config = yaml.load_all(config_file)
    logging.config.dictConfig(log_config)

    logging.debug('create hidden window for input')
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((1,1))
    signal.signal(signal.SIGINT, signal_handler)

    base_path = config.get('base_path', '~/Music/')
    with Player(fadeout=.5) as player, Library(base_path) as library, Controller(player, library, event=shutdown) as controller:
        logger.info('Press Q to shutdown')
        shutdown.wait()
        logger.info('Shutting down audio player')


if __name__ == '__main__':
    # TODO: Add autostart for raspian
    # http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/auto-running-programs-gui
    parse_main()
