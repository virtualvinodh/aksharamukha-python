# -*- coding: utf-8 -*-

# Hebr's own Fix logic, consolidated out of ConvertFix.py (batch
# migration - see ScriptProcessing/Tamil.py for the pattern this
# follows). No pre/post options exist for this script. Distinct from
# the already-migrated Hebrew script - reuses Hebrew's character
# tables (GM.CrunchSymbols(GM.VowelSigns, 'Hebrew')) but is its own
# separate dispatchable script.

import re
from .. import GeneralMap as GM

def _FixHebrEncode(Strng, Source):
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')'
    vowelsigns2 = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')?'

    #print('here fixing')
    #print('reverse is ', str(reverse), 'vinodh')
    Strng = re.sub('(׳)' + vowelsigns + vowelsigns2, r'\3\2\1', Strng)
    Strng = re.sub('(וֹ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(וּ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\1', Strng)

    return Strng

def _FixHebrDecode(Strng, Source):
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')'
    vowelsigns2 = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['\u05BC']) + ')?'

    #print('here fixing')
    #print('reverse is ', str(reverse), 'vinodh')
    # swap garesh and short vowels
    vowels = ['ְ','ֱ','ֲ','ֳ','ִ','ֵ','ֶ','ַ','ָ','ֹ','ֺ','ֻ','ׇ','\u05BC']
    vowelsR = '(' + '|'.join(vowels + ['וֹ', 'וּ']) + ')'
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)

    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)

    return Strng

def FixHebr(Strng, Source, reverse = False):
    return _FixHebrDecode(Strng, Source) if reverse else _FixHebrEncode(Strng, Source)
