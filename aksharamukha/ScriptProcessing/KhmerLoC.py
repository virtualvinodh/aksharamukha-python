# -*- coding: utf-8 -*-

# KhmerLoC's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py. FixKhmerLoC delegates to
# the shared ConvertFix.FixKhmer; the pre/post options below are
# genuinely KhmerLoC's own.
#
# KhmerLoCRomanLoCTarget/KhmerLoCRomanLoCSource each independently
# define the SAME option name in both PreProcess.py and PostProcess.py
# as genuinely different functions - suffixed _pre/_post here, same
# convention used everywhere else in ScriptProcessing/.
#
# PreProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import. See ScriptProcessing/Tamil.py.


import re
import unicodedata
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Khmer


# ---- Fix (encode/decode conversion logic) ----

def FixKhmerLoC(Strng,reverse=False):

    """Applies the shared Khmer fix-up logic (via ConvertFix.FixKhmer) targeting the Library of Congress romanization scheme."""
    from .. import ConvertFix as CF
    return CF.FixKhmer(Strng, reverse, target="KhmerLoC")

# ---- Pre-processing options ----

def KhmerLoCRomanLoCTarget_pre(Strng):
    """Apply Khmer LoC target-side fixes: mark the im vowel, reposition the bantoc sign, tag subscript consonant modifiers, reorder tone marks, normalize oya to oy, and drop decorative punctuation."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Khmer'))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,'Khmer'))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Khmer'))

    vir = Khmer.ViramaMap[0]

    #Mark im
    Strng = Strng.replace('ឹ', 'ិំ\u02BD')

    #move bantoc around
    Strng = re.sub('(.)(.(\u17D2.)*)(\u17CB)', r'\1\4\2', Strng)

    #mark consonant modifiers with subbase form
    Strng = re.sub('([ងញមបយរវ])(ុ)([ិឹីឺ])', r'\1''៉'r'\3', Strng)
    Strng = re.sub('([សហអ])(ុ)([ិឹីឺ])', r'\1''៊'r'\3', Strng)

    #move tonemarks around
    Strng = re.sub('('+ListC+')'+'([៎៏])''('+ListV+')''('+ListA+')?',r'\1\3\4\2',Strng)
    Strng = re.sub('('+ListC+')'+'('+ListV+')''([៎៏៊៉])''('+ListA+')?',r'\1\2\4\3',Strng)

    #fix oya to oy
    Strng = Strng.replace('ឲ្យ', 'ឱ្យ').replace('ឱ្យ', 'ឱ្យ' + vir)

    #ignore the following
    Strng = re.sub('[៙៚]', '', Strng)

    return Strng

def KhmerLoCRomanLoCSource_pre(Strng):
    """Denormalize precomposed diacritic vowels to NFD and fix apostrophe/oaḥ sequences for Khmer LoC source text."""
    listdenormalize = ['å', 'ẙ', 'à', 'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'ă']

    for let in listdenormalize:
        Strng = Strng.replace(let, unicodedata.normalize('NFD', let))

    Strng = re.sub('‛(?!ʹ)', '‛ʹ', Strng)
    Strng = re.sub('oaḥ', 'oḥ', Strng)

    return Strng

# ---- Post-processing options ----

def KhmerLoCRomanLoCTarget_post(Strng):
    """Normalizes Khmer LoC romanization output: NFC-normalizes, repositions consonant-modifier marks before certain vowels, fixes the 'oh' sequence, collapses double spaces."""
    import unicodedata
    Strng = unicodedata.normalize('NFC', Strng)

    #move consonant modifiers
    #Strng = re.sub('(‛ʹ)(′?)(a)(?![ṃḥ])', r'\1\2', Strng)
    Strng = re.sub('(ʹ)(′?)(?=[aāiīuūẏȳeoăáâààáéíóúàèìòùă])', r'\2', Strng)
    #Strng = re.sub('(ʹ)(′?)(a)(?=[aāiīuūẏȳeoă])', r'\2', Strng)

    #fix Oh
    Strng = Strng.replace('oḥ', 'oaḥ')
    Strng = Strng.replace('  ', ' ')


    return Strng

def KhmerLoCRomanLoCSource_post(Strng):
    """Reorders Khmer LoC romanization diacritics (bantoc, tone marks) relative to base consonants/vowels, marks subbase-form consonant modifiers, and strips the virama."""
    ListC ='|'.join(GM.CrunchSymbols(GM.Consonants,'Khmer'))
    ListV ='|'.join(GM.CrunchSymbols(GM.VowelSigns,'Khmer'))
    ListA ='|'.join(GM.CrunchSymbols(GM.CombiningSigns,'Khmer'))

    vir = Khmer.ViramaMap[0]

    #move bantoc around
    Strng = re.sub('(\u17CB)(.)', r'\2\1', Strng)

    #move tonemarks around
    Strng = re.sub('('+ListC+')'+'('+ListV+')''('+ListA+')?''([៎៏])',r'\1\4\2\3',Strng)

    #subjoined a
    #Strng = Strng.replace(vir + '‛', '\u17D2')

    #mark consonant modifiers with subbase form
    Strng = re.sub('([ងញមបយរវ])(៉)([ិឹីឺ])', r'\1''ុ'r'\3', Strng)
    Strng = re.sub('([សហអ])(៊)([ិឹីឺ])', r'\1''ុ'r'\3', Strng)

    #remove virama
    Strng = Strng.replace(vir, '')

    return Strng
