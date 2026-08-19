# -*- coding: utf-8 -*-

# Soyombo's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

def _FixSoyomboEncode(Strng):
    finVir = ['\U00011A5E\U00011A99','\U00011A5C\U00011A99','\U00011A60\U00011A99','\U00011A6D\U00011A99','\U00011A6F\U00011A99','\U00011A72\U00011A99','\U00011A74\U00011A99','\U00011A7C\U00011A99','\U00011A7D\U00011A99','\U00011A7F\U00011A99','\U00011A81\U00011A99']
    fin = ['\U00011A8A','\U00011A8B','\U00011A8C','\U00011A8D','\U00011A8E','\U00011A8F','\U00011A90','\U00011A91','\U00011A92','\U00011A93','\U00011A94']
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Soyombo')) + ')'

    Strng = Strng.replace('𑩜𑪙𑪀', '\U00011A83')  #KSSA
    Strng = re.sub('\U00011A7F\U00011A99' + '(?=' + consList + ')' , '\U00011A88', Strng) # Fix shka

    ## Gemination ##
    Strng = re.sub('(?<!𑪙)(.)𑪙' + r'\1', r'\1' + '\U00011A98', Strng)
    # final consonats
    if '\u02BE' in Strng:
        for x, y in zip (finVir, fin):
            Strng = re.sub(x + '(?!' + consList + ')' , y, Strng)

        Strng = re.sub('𑪈(?!' + consList + ')' , '\U00011A93', Strng)

        Strng = Strng.replace('\u02BE', '')

    ## remove final virama when not followed by a consonant
    Strng = re.sub('\U00011A99(?!' + consList + ')' , '', Strng)

    return Strng

def _FixSoyomboDecode(Strng):
    finVir = ['\U00011A5E\U00011A99','\U00011A5C\U00011A99','\U00011A60\U00011A99','\U00011A6D\U00011A99','\U00011A6F\U00011A99','\U00011A72\U00011A99','\U00011A74\U00011A99','\U00011A7C\U00011A99','\U00011A7D\U00011A99','\U00011A7F\U00011A99','\U00011A81\U00011A99']
    fin = ['\U00011A8A','\U00011A8B','\U00011A8C','\U00011A8D','\U00011A8E','\U00011A8F','\U00011A90','\U00011A91','\U00011A92','\U00011A93','\U00011A94']
    consList = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Soyombo')) + ')'

    Strng = Strng.replace('\U00011A9A', ' ') ## Reverse Tsheg
    Strng = Strng.replace('\U00011A83', '𑩜𑪙𑪀')  #KSSA

    ## Gemination ##
    Strng = re.sub('(.)\U00011A98', r'\1' + '\U00011A99' + r'\1', Strng)

    viraCon = ['\U00011A7C\U00011A99', '\U00011A7D\U00011A99', '\U00011A81\U00011A99', '\U00011A7F\U00011A99']
    initial = ['\U00011A86', '\U00011A87', '\U00011A89', '\U00011A88']

    for x, y in zip(viraCon, initial):
        Strng = Strng.replace(y, x)

    tsaSeries = ['𑩵','𑩶','𑩷']
    caSeries = ['𑩡','𑩢','𑩣']

    for x, y in zip(tsaSeries,caSeries):
        Strng = Strng.replace(y, x)

    ## initial ##

    for x, y in zip(finVir, fin):
        Strng = Strng.replace(y, x)

    return Strng

def FixSoyombo(Strng, reverse=False):
    return _FixSoyomboDecode(Strng) if reverse else _FixSoyomboEncode(Strng)

def SoyomboSyllabize(Strng):
    vowels = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'Soyombo')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Soyombo')+['𑩐', '\U00011A83']) + ')'
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Soyombo')) + ')'
    combiningSigns = '(' + '|'.join(GM.CrunchSymbols(GM.CombiningSigns, 'Soyombo')) + ')'

    fin = '(' + '|'.join(['\U00011A8A','\U00011A8B','\U00011A8C','\U00011A8D','\U00011A8E','\U00011A8F','\U00011A90','\U00011A91','\U00011A92','\U00011A93','\U00011A94']) + ')'

    Strng = re.sub(vowelsigns + combiningSigns + '?', r'\1\2 ', Strng)
    Strng = re.sub(consonants , r'\1 ', Strng)
    Strng = re.sub(' ' + vowelsigns, r'\1', Strng)
    Strng = re.sub(' ' + combiningSigns, r'\1', Strng)
    Strng = re.sub('\U00011A99' + ' ', '\U00011A99', Strng)
    Strng = re.sub(combiningSigns, r'\1 ', Strng)
    Strng = re.sub(' 𑪘', '\U00011A98', Strng)
    Strng = re.sub(fin, r'\1 ', Strng)
    Strng = re.sub('( )' + fin, r'\2 ', Strng)
    #Strng = re.sub(combiningSigns, r'\1་', Strng)

    return Strng

def SoyomboSanskritPalatals(Strng):
    tsaSeries = ['𑩵','𑩶','𑩷']
    caSeries = ['𑩡','𑩢','𑩣']

    for x, y in zip(tsaSeries,caSeries):
        Strng = Strng.replace(x, y)

    return Strng

def SoyomboFinals(Strng):

    return Strng

def SoyomboInitials(Strng):
    viraCon = ['\U00011A7C\U00011A99', '\U00011A7D\U00011A99', '\U00011A81\U00011A99']
    initial = ['\U00011A86', '\U00011A87', '\U00011A89']

    for x, y in zip(viraCon, initial):
        Strng = Strng.replace(x, y)

    return Strng

def SoyomboSpaceTscheg(Strng):
    Strng = Strng.replace(' ', '\U00011A9A')

    return Strng
