# -*- coding: utf-8 -*-
r"""
                         _   _____       
    /\                  | | |  __ \      
   /  \__   ____ _ _ __ | |_| |__) |   _ 
  / /\ \ \ / / _` | '_ \| __|  ___/ | | |
 / ____ \ V / (_| | | | | |_| |   | |_| |
/_/    \_\_/ \__,_|_| |_|\__|_|    \__, |
                                    __/ |
                                   |___/ 
"""

from . import utils
from . import download
from . import upload
from .Transfer import *

import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())
logging.basicConfig(level=logging.DEBUG)