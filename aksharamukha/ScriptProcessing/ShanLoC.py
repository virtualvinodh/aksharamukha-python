# -*- coding: utf-8 -*-

# ShanLoC's LoC (Library of Congress) romanization logic. See
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention this
# follows and how to add a new script. No dedicated FixShanLoC exists -
# the ShanLoC pivot script (ScriptMap/EastIndic/ShanLoC.py) relies
# purely on these pre/post functions plus the ordinary FixShan dispatch.
# References Burmese's ConsonantMap/ViramaMap directly (Shan's
# subjoined-consonant ordering is defined in terms of Burmese's).


import re
from aksharamukha.ScriptMap.EastIndic import Burmese

# ---- Pre-processing options ----

# internal
def ShanLoCToRomanLocPre(Strng):
    #preserve ႂ်
    """Apply Shan LoC target-side normalization: unify /aa/ vowel spellings, merge asat+virama, reorder subjoined consonants, and mark glottal-stop a and pure viramas."""
    Strng = Strng.replace('ႂ်', '\u036E')

    # Shan normalize /aa/
    Strng = Strng.replace('ၢ', 'ႃ')
    Strng = Strng.replace('ါ', 'ႃ')

    Strng = Strng.replace('ႃႆ', 'ၢႆ').replace('ႆၢ', 'ၢႆ').replace('ႆႃ', 'ၢႆ')

    # asat + virma to just virama
    Strng = Strng.replace('\u103A\u1039', '\u1039')

    ## sort subjoined consonants
    yrv = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29]
    yrvsub = ['\u103B','\u103C','\u1082']
    vir = Burmese.ViramaMap[0]

    for x,y in zip(yrv,yrvsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(y, vir + vir + x)

    # mark pure viramas
    aThat = r'်'
    Strng = re.sub('(?<!ႃ)'+aThat, aThat + 'ʻ', Strng)

    # mark a as glottalstop
    Strng = Strng.replace('ဢ','’ဢ')

    # changes for old shan
    Strng = Strng.replace('\u1039', '\u103A')

    # changes

    return Strng

# internal
def RomanLocToShanLoCPre(Strng):

    """Placeholder Shan LoC source-side hook (currently a no-op passthrough)."""
    return Strng

# ---- Post-processing options ----

# internal
def ShanLoCToRomanLocPost(Strng):
    """Reorders Shan LoC romanization glottal-stop and tone-mark combining diacritics relative to the preceding vowel/consonant."""
    Strng = re.sub('(ʻ)([\u0310\u0322])', r'\2\1', Strng)
    Strng = re.sub('(ō)([\u0310\u0322]?)(ʻ)', r'\1\2', Strng)

    return Strng

# internal
def RomanLocToShanLoCPost(Strng):
    # restrore special yrvh
    """Restores Shan LoC romanization conventions to native Shan script: undoes subjoined y/r/v marking, strips pure-vowel and glottal markers, reverses ai, and resolves open/closed vowel-consonant ambiguity."""
    yrv = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29]
    vir = '်'
    yrvsub = ['\u103B','\u103C','\u1082']

    for x,y in zip(yrv,yrvsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(vir + x, y)

    ## Fix modifier letter apostrephe to normal quotation mark
    Strng = Strng.replace('ʼ', '’')
    #remove purevowel marker
    Strng = Strng.replace('’', '')
    # remove marking for pure virama
    Strng = Strng.replace('ʻ', '')

    #ai reversal
    Strng = Strng.replace('\u036E', 'ႂ်')

    # closed vs open
    cons = "[ၵၶၷꧠငၸꧡꩡꧢၺꩦꩧꩨꩩꧣတထၻꩪၼပၽၿꧤမယရလဝသႁꩮၹၾႀဢ]"
    open = ['ႃ', 'ႄ', 'ေ']
    closed = ['ၢ', 'ႅ', 'ဵ']

    for o, c in zip(open, closed):
        pass
        Strng = re.sub('(' + cons + ')' + '(' + o + ')' + '(' + cons + ')', r'\1' + c + r'\3', Strng)

    return Strng
