# -*- coding: utf-8 -*-

# Tibetan's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Tibetan

def _FixTibetanEncode(Strng, swapNative):

    from .. import PostProcess
    ListC = [Tibetan.ViramaMap[0]+chr(x) for x in range(0x0F40,0x0F68)] # Consonants
    ListSubC = [chr(x+80) for x in range(0x0F40,0x0F68)] # Subjoined Consonants

    SubC = ["ཝྭ","ཡྱ","རྱ","རྭ", "ྺྭ"]
    SubMinC = ["ཝྺ","ཡྻ","ཪྻ","ཪྺ", "ྺྺ"]

    #introduce virama for Jihva/Upadh
    Strng = re.sub('([ྈྉ])', r'\1' + '\u0f84',  Strng)

    for x,y in zip(ListC,ListSubC):
        Strng = Strng.replace(x,y)

    for x,y in zip(SubC,SubMinC):
        Strng = Strng.replace(x,y)

    Strng = Strng.replace(' ', '\u0F0B')

    Strng = Strng.replace("ཛྷ༹", "ཞ")

    Strng = Strng.replace("(", "༺")
    Strng = Strng.replace(")", "༻")

    Strng = Strng.replace("{", "༼")
    Strng = Strng.replace("}", "༽")



    return Strng

def _FixTibetanDecode(Strng, swapNative):

    from .. import PostProcess
    ListC = [Tibetan.ViramaMap[0]+chr(x) for x in range(0x0F40,0x0F68)] # Consonants
    ListSubC = [chr(x+80) for x in range(0x0F40,0x0F68)] # Subjoined Consonants

    SubC = ["ཝྭ","ཡྱ","རྱ","རྭ", "ྺྭ"]
    SubMinC = ["ཝྺ","ཡྻ","ཪྻ","ཪྺ", "ྺྺ"]



    AspirateDecom= ["གྷ", "ཌྷ", "དྷ", "བྷ", "ཛྷ", "ྒྷ", "ྜྷ", "ྡྷ", "ྦྷ", "ྫྷ"]
    AspirateAtomic = ["གྷ", "ཌྷ", "དྷ", "བྷ", "ཛྷ", "ྒྷ", "ྜྷ", "ྡྷ", "ྦྷ", "ྫྷ"]

    for x, y in zip(AspirateDecom, AspirateAtomic):
        Strng = Strng.replace(x, y)

    for x,y in zip(SubC,SubMinC):
        Strng = Strng.replace(y,x)

    for x,y in zip(ListC,ListSubC):
        Strng = Strng.replace(y,x)

    for x,y in zip(['྄རྀ','྄རཱྀ','྄ལྀ',"྄ལཱྀ"],['ྲྀ','ྲཱྀ', 'ླྀ','ླཱྀ']):
        Strng = Strng.replace(x,y)

    Strng = Strng.replace('་', ' ')
    Strng = Strng.replace("༔", "།")
    Strng = Strng.replace("༈", "།")

    Strng = Strng.replace("༺", "(")
    Strng = Strng.replace("༻", ")")

    Strng = Strng.replace("༼", "{")
    Strng = Strng.replace("༽", "}")

    #remove virama from Jihva/Upadh
    Strng = re.sub('([ྈྉ])(\u0f84)', r'\1',  Strng)

    if swapNative:
        Strng = Strng.replace('ཇྷ', 'ཛྷ') ## JHA -> DZHA
        Strng = Strng.replace("ཇ", "ཛ")
        Strng = Strng.replace('ཅ', 'ཙ')
        Strng = Strng.replace('ཆ', 'ཚ')
        Strng = Strng.replace("ཞ", "ཛྷ༹")
        Strng = Strng.replace("འ", "ཨ")

    return Strng

def FixTibetan(Strng,reverse=False, swapNative = True):

    from .. import PostProcess
    return _FixTibetanDecode(Strng, swapNative) if reverse else _FixTibetanEncode(Strng, swapNative)

def TibetanSyllabize(Strng):

    from .. import PostProcess
    vowels = '(' + '|'.join(GM.CrunchSymbols(GM.Vowels, 'Tibetan')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Tibetan')+['ཨ','ཅ','ཆ','ཇ','ཇྷ']) + ')'
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Tibetan')+['\u0F80']) + ')'
    combiningSigns = '(' + '|'.join(GM.CrunchSymbols(GM.CombiningSigns, 'Tibetan')+['\u0F82']) + ')'
    ListSubC = '(' + '|'.join([chr(x+80) for x in range(0x0F40,0x0F68)] + ['ྻ','ྺ','ྼ']) + ')' # Subjoined Consonants

    Strng = re.sub(vowelsigns + combiningSigns + '?', r'\1\2་', Strng)
    Strng = re.sub(consonants , r'\1་', Strng)
    Strng = re.sub(ListSubC, r'\1་', Strng)
    Strng = re.sub('་' + vowelsigns, r'\1', Strng)
    Strng = re.sub('་' + ListSubC, r'\1', Strng)
    Strng = re.sub('་' + combiningSigns, r'\1', Strng)
    Strng = re.sub(combiningSigns, r'\1་', Strng)

    Strng = Strng.replace('་་', '་')

    return Strng

def TibetanSanskritPalatals(Strng):

    from .. import PostProcess
    caSeries = ['ཅ','ཆ','ཇ','ཇྷ']
    tsaSeries = ['ཙ','ཚ','ཛ','ཛྷ']

    for x, y in zip(tsaSeries,caSeries):
        Strng = Strng.replace(x, y)

    return Strng

def tibetandbumed(Strng):

    from .. import PostProcess
    return Strng

def TibetanNada(Strng):

    from .. import PostProcess
    Strng = Strng.replace('\u0F83','\u0F82')

    return Strng

def TibetanTsheg(Strng):

    from .. import PostProcess
    Strng = Strng.replace('\u0F0B', ' ')

    return Strng

def TibetanRemoveVirama(Strng):

    from .. import PostProcess
    Strng = Strng.replace(Tibetan.ViramaMap[0],'')

    return Strng

def TibetanRemoveBa(Strng):

    from .. import PostProcess
    Strng = PostProcess.VaToBa(Strng,'Tibetan')

    Strng = Strng.replace('ཪྺ', 'རྦ')
    Strng = Strng.replace('བྺ', 'བྦ')
    Strng = Strng.replace('ྦྺ', 'ྦྦ')

    return Strng
