# -*- coding: utf-8 -*-

# Burmese's LoC (Library of Congress) romanization logic. See
# ScriptProcessing/HOW_TO_ADD_LOC.md for the naming convention this
# follows (BurmeseToRomanLocPre/Post run native->LoC-Roman;
# RomanLocToBurmesePre/Post run LoC-Roman->native) and how to add a new
# script. Burmese has no separate LoC character-map pivot (unlike
# Gurmukhi/Tibetan/etc.) - it converts directly from plain Burmese.


import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Burmese

# ---- Pre-processing options ----

def BurmeseToRomanLocPre(Strng):
    # asat + virma to just virama
    """Apply Burmese LoC target-side normalization: merge asat+virama, reorder subjoined consonants, mark glottal-stop a and pure viramas, and convert dependent vowel+diacritic sequences to independent vowels."""
    Strng = Strng.replace('\u103A\u1039', '\u1039')

    # swap iu -> ui
    Strng = Strng.replace('\u102D\u102F', '\u102F\u102D')

    # mark Independent au -> o'
    Strng = Strng.replace('ဪ','ဩʻ')

    ## sort subjoined consonants
    yrvh = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29] + Burmese.ConsonantMap[32:33]
    yrvhsub = ['\u103B','\u103C','\u103D','\u103E']
    vir = Burmese.ViramaMap[0]

    for x,y in zip(yrvh,yrvhsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(y, vir + vir + x)

    # swap tone + virama to proper order
    Strng = Strng.replace("့်", "့်")

    # mark pure viramas
    aThat = r'်'
    Strng = Strng.replace(aThat, aThat + 'ʻ')

    # mark a as glottalstop
    Strng = Strng.replace('အ','’အ')

    # replace vowel + diac with vowels
    vowDep = 'အော် အော အိ အီ အု အူ အေ'.split(' ')
    vowIndep = 'ဪ ဩ ဣ ဤ ဥ ဦ ဧ'.split(' ')

    for x, y in zip(vowDep, vowIndep):
        Strng = Strng.replace(x, y)

    # danda to comma and double danda to full stop
    Strng = Strng.replace('၊', ',').replace('။', '.')

    #print(Strng)

    return Strng

def RomanLocToBurmesePre(Strng):
    # adhoc chars
    """Normalize LoC Burmese romanization source text: expand ad hoc letter codes to Burmese punctuation, fix visarga/diacritic characters, convert comma/period to danda marks, and simplify o-quote sequences to au."""
    chars_misc = {
        "e*": "၏",
        'n*': "၌",
        'r*': '၍',
        'l*': '၎'
    }

    for lat, bur in chars_misc.items():
        Strng = Strng.replace(lat, bur)

    Strng = Strng.replace('ṁ', 'ṃ')

    # reverse danda to comma and double danda to full stop
    Strng = Strng.replace(',', '၊').replace('.', '။')

    # restore visarga and fix incorrect diacritic character
    Strng = Strng.replace('˝', 'ʺ').replace('ʺ', 'ḥ')

    # restore visarga and fix incorrect diacritic character
    Strng = Strng.replace('´','ʹ').replace('ʹ', '˳')

    # replace modifier letter with quotation mark
    vowelSigns = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV, 'IAST'))
    Strng = re.sub('(ʼ)(a|' + vowelSigns + ')', '’' + r'\2', Strng)

    # left quotation mark -> modifier letter comma
    consonants = '|'.join(GM.CrunchSymbols(GM.Consonants, 'IAST'))
    Strng = re.sub('(' + consonants + ')(‘)', r'\1' + 'ʻ', Strng)

    Strng = Strng.replace('o‘', 'oʻ')

    # reverse o' to au
    Strng = Strng.replace('oʻ', 'au')

    return Strng

# ---- Post-processing options ----

def BurmeseToRomanLocPost(Strng):
    #print(Strng)
    # mark tone
    """Applies Library of Congress Burmese romanization target conventions: marks tone, folds 'au+glottal' to 'o+glottal', renders visarga as a tone mark, and substitutes a few adhoc lexical characters."""
    Strng = Strng.replace('˳', 'ʹ')

    # mark depaend au -> o'
    Strng = Strng.replace('auʻ','oʻ')

    # mark visarga as tone
    Strng = Strng.replace('ḥ', 'ʺ')

    # sort subjoined consonants
    # Strng = Strng.replace('‘‘', '')

    # adhoc chars
    chars_misc = {
        "e*": "၏",
        'n*': "၌",
        'r*': '၍',
        'l*': '၎'
    }

    for lat, bur in chars_misc.items():
        Strng = Strng.replace(bur, lat)

    #Strng = Strng.replace('ṃ', 'ṁ')

    return Strng

def RomanLocToBurmesePost(Strng):
    # remove marking for pure virama
    """Reverses LoC Burmese romanization conventions back to native encoding: drops pure-virama marker, restores superscript-Ga to subjoined y/r/v/h, reassembles vowel+diacritic sequences, undoes glottal-stop marking."""
    Strng = Strng.replace('ʻ', '')

    # restore superscript Ga into normal subjoined y, r , v, h
    yrvh = Burmese.ConsonantMap[25:27] + Burmese.ConsonantMap[28:29] + Burmese.ConsonantMap[32:33]
    yrvhPat = ''.join(yrvh)
    Strng = re.sub(f'(\u103A)(\u1039)([{yrvhPat}])', r'\2\3', Strng)

    # restrore special yrvh
    virsub = '\u1039'
    yrvhsub = ['\u103B','\u103C','\u103D','\u103E']

    for x,y in zip(yrvh,yrvhsub):
        # Undo Replace subjoining forms: exp-virama + y/r/v/h <- subjoining y/r/v/h
        Strng = Strng.replace(virsub + x, y)

    # reverse replace vowel + diac with vowels
    vowDep = 'အော် အော အိ အီ အု အူ အေ'.split(' ')
    vowIndep = 'ဪ ဩ ဣ ဤ ဥ ဦ ဧ'.split(' ')

    ## Fix modifier letter apostrephe to normal quotation mark
    Strng = Strng.replace('ʼ', '’')

    for x, y in zip(vowDep, vowIndep):
        Strng = Strng.replace('’' + y, x)

    # u-Indep-i -> u-dep-i
    Strng = Strng.replace('\u102Fဣ', '\u102D\u102F')

    # reverse mark a as glottalstop
    Strng = Strng.replace('’အ', 'အ')

    # swap tone + virama to proper order
    Strng = Strng.replace("့်", "့်")

    return Strng
