# -*- coding: utf-8 -*-

# MasaramGondi's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

def _FixMasaramGondiEncode(Strng):
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'MasaramGondi')) + ')'

    Strng = Strng.replace('𑴌𑵅𑴪','\U00011D2E') # KSSA
    Strng = Strng.replace('𑴓𑵅𑴕','\U00011D2F') # JNYA
    Strng = Strng.replace('𑴛𑵅𑴦','\U00011D30') # TRA

    Strng = re.sub(consList + '\U00011D45\U00011D26', r'\1' + '\U00011D47', Strng) # kra
    Strng = re.sub('\U00011D26\U00011D45' + consList, '\U00011D46' + r'\1', Strng) # rka

    ## remove final virama when not followed by a consonant
    Strng = re.sub('\U00011D45(?!' + consList + ')' , '\U00011D44', Strng)

    return Strng

def _FixMasaramGondiDecode(Strng):
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'MasaramGondi')) + ')'

    Strng = Strng.replace('\U00011D2E', '𑴌𑵅𑴪') # KSSA
    Strng = Strng.replace('\U00011D2F', '𑴓𑵅𑴕') # JNYA
    Strng = Strng.replace('\U00011D30', '𑴛𑵅𑴦') # TRA

    Strng = Strng.replace('\U00011D47', '\U00011D45\U00011D26',) # kra
    Strng = Strng.replace('\U00011D46', '\U00011D26\U00011D45') # rka

    Strng = Strng.replace('\U00011D44','\U00011D45')

    return Strng

def FixMasaramGondi(Strng, reverse=False):
    return _FixMasaramGondiDecode(Strng) if reverse else _FixMasaramGondiEncode(Strng)
