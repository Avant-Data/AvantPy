# -*- coding: utf-8 -*-
"""
                         _   _____        _        
    /\                  | | |  __ \      | |       
   /  \__   ____ _ _ __ | |_| |  | | __ _| |_ __ _ 
  / /\ \ \ / / _` | '_ \| __| |  | |/ _` | __/ _` |
 / ____ \ V / (_| | | | | |_| |__| | (_| | || (_| |
/_/    \_\_/ \__,_|_| |_|\__|_____/ \__,_|\__\__,_|
                                                   
"""

from .utils import Utils

import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())