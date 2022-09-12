# -*- coding: utf-8 -*-
import avantpy


def test_generateID():
    assert avantpy.utils.generateID(
        'Generate ID with MD5 hash text') == '3b3331b428cc68278b975d0d177b9948'

def test_removeEmpty():
    assert avantpy.utils.removeEmpty('') == None

def test_flatten():
    assert avantpy.utils.flatten([[],[],[],[]]) == []