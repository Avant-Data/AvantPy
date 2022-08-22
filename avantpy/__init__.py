# -*- coding: utf-8 -*-
r"""
                         _   _____        _        
    /\                  | | |  __ \      | |       
   /  \__   ____ _ _ __ | |_| |  | | __ _| |_ __ _ 
  / /\ \ \ / / _` | '_ \| __| |  | |/ _` | __/ _` |
 / ____ \ V / (_| | | | | |_| |__| | (_| | || (_| |
/_/    \_\_/ \__,_|_| |_|\__|_____/ \__,_|\__\__,_|
                                                   
"""

from . import utils
from . import download

import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())
logging.basicConfig(level=logging.DEBUG)