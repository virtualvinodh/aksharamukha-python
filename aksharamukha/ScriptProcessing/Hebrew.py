# -*- coding: utf-8 -*-

# Hebrew's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixHebrewEncode(Strng):
    """Builds surface Hebrew script from the internal representation: inserts default patah, fixes nasal assimilation before certain consonants, reorders dagesh/vowel diacritics, marks gemination with dagesh, and applies final letter forms."""
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew')+['צּ','גּ']) + ')'

    vowelsignsA = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ']) + ')'
    vowelsignsAD = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ']) + ')'

    vowelsignsADShin = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ']) + ')'
    vowelsignsADShinG = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ', '׳']) + ')'


    finalCons = ['כ', 'מ', 'נ', 'פ', 'צ', 'פּ', 'כּ']
    finals = ['ך', 'ם', 'ן', 'ף', 'ץ', 'ףּ', 'ךּ']

    otherCons = 'ב,ח,ע,צ,ש,ת'.split(',')
    consonantsAll = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew') + finals  + otherCons + ['׳']) + ')'

    Strng = Strng.replace('\u02BD', '')
    Strng = Strng.replace('\u02BE', '')

    ## geminate cc/jj
    Strng = Strng.replace('ג׳ְג׳', 'גּ׳').replace('צ׳ְצ׳', 'צּ׳')

    # Fix Anusvara

    # mK, mG, mp, mC, md, mt
    Strng = re.sub('מְ' + '\u02BC' + '([גדזטכצקת])', 'נְ' + r'\1', Strng)
    Strng = re.sub('מְ' + '\u02BC', 'מְ', Strng)

    # insert a_sign
    Strng = re.sub(consonants + '(?!' + vowelsigns + ')', r'\1' + '\u05B7' + r'\2', Strng)

    # reverse dagesh patah
    Strng = Strng.replace('\u05b7\u05Bc', '\u05Bc\u05b7')

    # fix double a to single a
    Strng = Strng.replace('\u05b7\u05b7', '\u05B7')

    # Fix a appear with Dagesh and Shva.. k -> kaph + patau + dagesh + shva -> kaph + dagesh + shva
    Strng = Strng.replace('\u05b7\u05bc\u05B0', '\u05bc\u05B0')


    # fix order of vowel signs and vowels sign with ch/j
    Strng = re.sub('(׳)' + vowelsigns, r'\2\1', Strng)
    Strng = re.sub('(וֹ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(וּ)(׳)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\2\1', Strng)
    Strng = re.sub('(׳)(\u05b7)', r'\1', Strng)

    # Fix Pateh appearing with vowel signs
    Strng = re.sub('(\u05b7)' + vowelsigns, r'\2', Strng)
    Strng = re.sub('(\u05b7)' + '(\u05BC)' + vowelsigns, r'\2\3', Strng)

    #Do gemination
    ## consonant doubling with Dagesh
    ## gemination with dagesh as well
    Strng = re.sub('([' + 'ושרקסנמליזטײ' + 'הגדת' + '])(ְ)' + r'\1', r'\1' + 'ּ', Strng)
    Strng = re.sub('(שׁ)(ְ)' + r'\1', r'\1' + 'ּ', Strng)
    ## for geminate ka use qa
    ## bba -> ba, ppa -> pa ; cannot use dagesh for gemination too ambigous
    Strng = Strng.replace('כְּכּ', 'קּ').replace('פְּפּ','פּ').replace('בְּבּ','בּ')

    # Fix Finals
    shortVowels = '(' + '|'.join(['\u05B7', '\u05B8', '\u05B4', '\u05BB', '\u05B5', '\u05B6', '\u05B9', '\u05B0']) + ')'

    vowelsAll = '(' + '|'.join(['\u05B7', '\u05B8', '\u05B4', '\u05BB', '\u05B5', '\u05B6', '\u05B9', '\u05B0', 'י', 'וֹ', 'וּ'] + ['׳']) + ')'

    for c, f in zip(finalCons, finals):
        Strng = re.sub(vowelsAll + '(' + c + ')' + shortVowels + '(׳?)' + '(?!' + consonantsAll + '|י|ו)', r'\1' + f +  r'\3' + r'\4', Strng)

    # remove final schwa
    Strng = re.sub('(?<!ה)(ְ)(׳?)' + '(?!' + consonantsAll + '|י|ו)', r'\2\3', Strng)

    # Fix Va + O
    Strng = Strng.replace('װ' + '\u05B9', '\u05D5\u05BA')

    Strng = Strng.replace('װ' , '\u05D5')
    Strng = Strng.replace('ײ' , 'י')

    Strng = Strng.replace('\u02BC', '')


    Strng = Strng.replace('௞', '')

    return Strng

# internal
def _FixHebrewDecode(Strng):
    """Reconstructs the internal representation from surface Hebrew script: restores final letters to medial forms, reorders diacritics, approximates missing consonant/vowel distinctions, expands dagesh gemination, and resolves shva na versus shva nach."""
    vowelsigns = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew')) + ')'
    consonants = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew')+['צּ','גּ']) + ')'

    vowelsignsA = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ']) + ')'
    vowelsignsAD = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ']) + ')'

    vowelsignsADShin = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ']) + ')'
    vowelsignsADShinG = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ', '׳']) + ')'


    finalCons = ['כ', 'מ', 'נ', 'פ', 'צ', 'פּ', 'כּ']
    finals = ['ך', 'ם', 'ן', 'ף', 'ץ', 'ףּ', 'ךּ']

    otherCons = 'ב,ח,ע,צ,ש,ת'.split(',')
    consonantsAll = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew') + finals  + otherCons + ['׳']) + ')'

    vowels = ['ְ','ֱ','ֲ','ֳ','ִ','ֵ','ֶ','ַ','ָ','ֹ','ֺ','ֻ','ׇ']
    vowelsR = '(' + '|'.join(vowels + ['וֹ', 'וּ']) + ')'

    for f,c in zip(finals, finalCons):
        Strng = Strng.replace(f, c)

    # Swap the order of diacritics
    Strng = re.sub(vowelsR + '([ּׁׂ])', r'\2\1', Strng)

    ## gimme, teh and other consonants  with Dagesh just replace themselves
    #Strng = re.sub('([דתצ])(ּ)', r'\1', Strng)

    ## approx vowels

    # Short vowels with Schwa
    Strng = Strng.replace('אֲ', 'אַ')
    Strng = Strng.replace('עֲ', 'אַ')

    Strng = Strng.replace('\u05B1', '\u05B6').replace('\u05B3', '\u05B9').replace('\u05B2','\u05b7')

    # replace malei forms
    Strng = re.sub('(?<=[ֵֶַָֹ])([א])'+'(?!' + vowelsignsA + ')', '', Strng)
    Strng = re.sub('(?<=[ִֵֶַָֹֻ])([ה])'+'(?!' + vowelsignsAD + ')', '', Strng)

    Strng = re.sub('(?<=[ֵֶ])([י])'+'(?!' + vowelsR + vowelsigns + ')', '', Strng)

    # ha + dagesh to normal ha
    Strng = Strng.replace('הּ', 'ה')

    ## consonant doubling with Dagesh

    Strng = re.sub('([' + 'שרקסנמליזט' + '])(ּ)', r'\1' + 'ְ' + 'ְ' + r'\1', Strng) ## twice to mark it specifically
    Strng = re.sub('([דתצה])(ּ)', r'\1'+ 'ְ' + 'ְ' + r'\1', Strng)


    ## approx Cons
    Strng = Strng.replace('ת', 'ט').replace('ח', 'כ').replace('ע', 'א').replace('שׂ', 'ס')
    Strng = re.sub('ש(?![ׂׄ])', 'שׁ', Strng)

    Strng = Strng.replace('ׁׁ','ׁ')

    ## replace vet with double vav if not followed by dagesh
    Strng = re.sub('ב(?!ּ)', 'װ', Strng)

    # swap garesh and short vowels
    Strng = re.sub(vowelsR + "(׳)", r'\2\1', Strng)

    ## reverse dagesh of cca jja
    Strng = Strng.replace('גּ׳', 'ג׳ְג׳').replace('צּ׳', 'צ׳ְצ׳')

    # tsa when not followed by gatresh with t+sa (including vowel signs)
    Strng = re.sub('צ' + '(?!׳)', 'טְְס', Strng)

    ## reinsert uo2dbc of vau based vowels
    Strng = re.sub('(\s|^|\.|,|א)' + '(וֹ|וּ)', 'א' + r'\1\2' , Strng)
    Strng = re.sub('(וּ)' + vowelsignsA, 'װְװ' + r'\2', Strng)

    ## vav, yod to double vav/yod if followed by short vowels or long vowels
    Strng = re.sub('י' + '(?=' + vowelsigns + '|ַ)', 'ײ', Strng)
    Strng = re.sub('ו' + '(?=' + '[ְִֵֶַָׇֺֻ]' +  '|ַ)', 'װ', Strng)

    ## replace vay ad yod in other cases when no preceded or succeeded by the vowels
    Strng  = re.sub('(?<!ִ)(י)', 'ײ' , Strng)
    Strng = re.sub('(ו)(?![ֹֺּ])', 'װ', Strng)

    ## Intrdouce Schva nach

    # Replva holem for vav with holem
    Strng = Strng.replace('ֺ','ֹ')

    # remove stray alephs
    Strng = re.sub('[א](?!' + vowelsR + ')', '', Strng)

    ## remove schwa at the end of vwords
    Strng = re.sub(consonantsAll + "(?!" + vowelsignsADShinG + ')', r'\1' + 'ְ' + r'\2', Strng)

    ## Aleph + Svha = a
    Strng = Strng.replace('אְ','')

    ## Hard Svha nakh
    if '௞' in Strng:
        # added in preoptions
        Strng = Strng.replace('௞', '')
        Strng = Strng.replace('ְ' + 'ְ','ְ')
    else:
        ## Schva nach
        # https://judaism.stackexchange.com/questions/92599/what-are-the-rules-for-shva-na
        # http://www.shailamorah.com/kriah-roundtable/teaching-shva-rules
        Strng = re.sub('(\s|\.|,|^)' + consonantsAll + '(ְ)', r'\1\2' + 'ֶ', Strng)
        Strng = re.sub('(ּ)' + '(ְ)', r'\1' + 'ֶ' , Strng)
        Strng = re.sub(consonantsAll + '(' 'ְ' + 'ְ' + ')' + '(' + r'\1' + ')(' + 'ְ' + ')', r'\1\2\3' +  'ֶ', Strng)
        Strng = re.sub(consonantsAll + '(ְ)' + '(' + r'\1' + ')'+ '(?!(\s|\.|\n|,|$))', r'\1' + 'ֶ' + r'\3', Strng)
        Strng = re.sub(consonantsAll + '(ְ)' + consonantsAll + '(ְ)' + '(?!(\s|\.|\n|,|$))', r'\1\2' + r'\3' + 'ֶ' , Strng)

        Strng = Strng.replace('ְ' + 'ְ','ְ') #two schva to one
        Strng = Strng.replace('ֶ' + 'ְ','ְ') #two schva to one

    ## remove patesh
    Strng = re.sub('(?<![אע])\u05B7', '', Strng)

    Strng = Strng.replace('௞', '')

    return Strng

# internal
def FixHebrew(Strng, reverse = False):
    """Dispatches to the Hebrew encode or decode fix routine based on the reverse flag."""
    return _FixHebrewDecode(Strng) if reverse else _FixHebrewEncode(Strng)

# ---- Pre-processing options ----

# frontend
def holamlong(Strng):
    """Writes holam as vav+holam to denote a long /o/ rather than a bare holam."""
    Strng = Strng.replace('ֹּ','ֹּ')
    Strng = re.sub('(?<!ו)ֹ', 'וֹ', Strng)

    return Strng

# frontend
def novowelshebrewIndic(Strng):
    """Produces unpointed (vowel-less) Hebrew text for Indic-sourced input, defaulting consonants without an explicit vowel sign to a bare patah."""
    Strng = novowelshebrewSemitic(Strng)

    finals = ['ך', 'ם', 'ן', 'ף', 'ץ', 'ףּ', 'ךּ']
    otherCons = 'ב,ח,ע,צ,ש,ת'.split(',')
    consonantsAll = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew') + finals  + otherCons + ['׳', 'י', 'ו' ,'א']) + ')'
    vowelsignsADShinG = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Hebrew') + ['ַ', 'ּ', 'ׁ', '׳']) + ')'

    Strng = re.sub(consonantsAll + "(?!" + vowelsignsADShinG + ')', r'\1' + 'ַ' + r'\2', Strng)

    return Strng

# frontend
def novowelshebrewSemitic(Strng):
    """Adds a dagesh to the ambiguous begadkefat letters (ב פ כ) so they read as plosives rather than fricatives when niqqud is absent, e.g. ב פ כ → k p b not v f ḵ."""
    Strng = Strng.replace('כ', 'כּ').replace('פ', 'פּ').replace( 'ב', 'בּ')
    Strng = Strng.replace('ך', 'ךּ').replace('ף','ףּ')

    return Strng

# frontend
def shvanakhall(Strng):
    """Appends a marker that forces every shva in the text to be treated as shva nach (silent) rather than shva na."""
    Strng = Strng + ' \u0BDE'

    return Strng

# ---- Post-processing options ----

# frontend
def removeNikkud(Strng):
    """Strips all niqqud (vowel-point) diacritics such as patach, kamatz, hiriq, and dagesh from the text."""
    nikkuds = ["\u05B7","\u05B8","\u05B4","\u05B4י","\u05BB", "\u05C2", "\u05C1",\
    "\u05B6","\u05B5","\u05B9","וֹ","\u05B1","\u05B2","\u05B3","\u05BC","\u05B0", "\u05C7"]

    for nikkud in nikkuds:
        Strng = Strng.replace(nikkud, '')

    return Strng

# internal
def HebrewVetVav(Strng):
    """Converts vav to vet after short vowels when not followed by a dagesh, and normalizes bet+holam sequences."""
    shortVowels = '(' + '|'.join(['\u05B7', '\u05B8', '\u05B4', '\u05BB', '\u05B5', '\u05B6', '\u05B9', '\u05B0']) + ')'

    Strng = re.sub(shortVowels + '(' + 'ו' + ')' + '(?!\u05BC)', r'\1' + 'ב', Strng)

    # Bet with Holam for Vav with beth with holam

    Strng = Strng.replace('בֺ', 'בֹ')

    return Strng

# frontend
def HeberewQoph(Strng):
    """Represents geminated/emphatic kaf using qof instead, e.g. כּ ← ק."""
    Strng = Strng.replace('כּ', 'ק').replace('ךּ', 'ק')

    return Strng

# frontend
def HebewShortO(Strng):
    """Marks short /o/ with kamatz katan instead of holam when the holam is not preceded by vav, e.g. לֹ ← לׇ."""
    Strng = re.sub('(?<!ו)\u05B9', '\u05C7', Strng)

    return Strng

# internal
def HebrewnonFinalShort(Strng):
    """Marks a short vowel on a word-final letter by temporarily inserting a helper heh, then restores the corresponding final (sofit) consonant form once resolved."""
    finals = ['ך', 'ם', 'ן', 'ף', 'ץ', 'ףּ', 'ךּ']
    finalCons = ['כ', 'מ', 'נ', 'פ', 'צ', 'פּ', 'כּ']

    otherCons = 'ב,ח,ע,צ,ש,ת'.split(',')
    consonantsAll = '(' + '|'.join(GM.CrunchSymbols(GM.Consonants, 'Hebrew') + finals  + ['׳', 'י', 'ו'] + otherCons) + ')'

    shortVowels = ['\u05B7', '\u05B8', '\u05B4', '\u05BB', '\u05B5', '\u05B6', '\u05B9', '\u05C7']
    shortVowelsR = '(' + '|'.join(['\u05B7', '\u05B8', '\u05B4', '\u05BB', '\u05B5', '\u05B6', '\u05B9', '\u05C7'] + ['׳']) + ')'

    for s in shortVowels:
        Strng = re.sub('(' + s + ')' + '(׳?)' + '(?!' + consonantsAll + ')', r'\1\2' + 'ה' + '\u02BE', Strng )

    for f, c in zip(finals, finalCons):
        Strng = re.sub('(' + f + ')' + shortVowelsR + '(׳?)' + 'ה' + '\u02BE', c + r'\2\3' + 'ה', Strng)

    for f in finals:
        Strng = Strng.replace(f + '\u05B0', f)

    Strng = Strng.replace('\u05B0' + '׳' + 'ה' + '\u02BE', '\u05B0' + '׳' )
    Strng = Strng.replace('וֹה' + '\u02BE', 'וֹ' )

    Strng = Strng.replace('\u02BE', '')

    uVowels = ['וֹ', 'וּ']

    #for s in uVowels:
        #Strng = re.sub('(' + s + ')' + '(׳?)' + '(?!' + consonantsAll + ')', r'\1\2' + 'א', Strng )

    return Strng

# unreferenced
def HebrewKatevMalei(Strng):
    """Replaces Hebrew qamats and patach vowel points with aleph, producing ktiv male (full/plene) spelling."""
    Strng = Strng.replace('ָ', 'א') # long aa
    Strng = Strng.replace('ַ', 'א') # short a

    return Strng

