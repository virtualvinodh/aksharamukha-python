# -*- coding: utf-8 -*-

# Itrans's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# swapEeItrans independently defines the SAME option name in both
# PreProcess.py and PostProcess.py as two different functions - suffixed
# _pre/_post here, aliased back on re-export (see ScriptProcessing/
# DevanagariLimbu.py for the first script this pattern was used on).

import re

def swapEeItrans_pre(Strng):
    Strng = Strng.replace('^e', 'X@X@')
    Strng = Strng.replace('e', '^e')
    Strng = Strng.replace('X@X@','e')

    Strng = Strng.replace('^o', 'X@X@')
    Strng = Strng.replace('o', '^o')
    Strng = Strng.replace('X@X@','o')

    return Strng

def swapEeItrans_post(Strng):
    Strng = Strng.replace('^e', 'X@X@')
    Strng = Strng.replace('e', 'E')
    Strng = Strng.replace('X@X@', 'e')

    Strng = Strng.replace('^o', 'X@X@')
    Strng = Strng.replace('o', 'O')
    Strng = Strng.replace('X@X@', 'o')

    return Strng

def readableItrans(Strng):
    pairsReadable = [('R^i','RRi'), ('R^I','RRii'), ('',''), ('',''), ('A', 'aa'), ('I', 'ii'), ('U', 'uu'), ('Ch', 'chh'), ('kSh','x'), ('M', '.m')]

    for x, y in pairsReadable:
        Strng = Strng.replace(x,y)

    return Strng
