# -*- coding: utf-8 -*-

# Bengali's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# ConvertFix/PreProcess/PostProcess are imported LOCALLY inside each
# function that needs them (not at module level) - required to avoid a
# load-order-dependent circular import, since these three modules
# re-export names from here. See ScriptProcessing/Tamil.py.

import re
from .. import GeneralMap as GM

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixBengaliEncode(Strng):

    """Inserts a ZWNJ before bare ba after a virama, fixes subjoined bva rendered as va-with-nukta, and applies the khanda-ta fix when encoding into Bengali."""
    from .. import PostProcess
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Bengali'))
    ba = 'ব'

    Strng = re.sub('(?<![রবম])' + Virama + ba,  Virama + '\u200C' + ba, Strng)
    #print(Strng)
    ## Fix স্ভ়ারা  -> স্বারা ; subjoined ba is by default pronounced as /va/ in Bengali
    Strng = re.sub('(?<![রবমভ়])' + '(\u09CD\u09AD\u09BC)', '\u09CD\u09AC', Strng)
    #print(Strng)

    Strng = PostProcess.KhandaTa(Strng, 'Bengali', False)
    #print(Strng)

    return Strng

# internal
def _FixBengaliDecode(Strng):

    """Reverses the khanda-ta fix when decoding out of Bengali."""
    from .. import PostProcess
    Virama = ''.join(GM.CrunchSymbols(['ViramaMap'], 'Bengali'))
    ba = 'ব'

    pass

    Strng = PostProcess.KhandaTa(Strng, 'Bengali', True)
    #print(Strng)

    return Strng

# internal
def FixBengali(Strng, reverse=False):

    """Dispatches to the Bengali encode or decode fix routine based on the reverse flag."""
    return _FixBengaliDecode(Strng) if reverse else _FixBengaliEncode(Strng)

# ---- Pre-processing options ----

# frontend
def BengaliSubojinedVa(Strng):

    """Renders subjoined /va/ using nukta-ba (ভ়) instead of plain ba, e.g. স্ব দ্ব → sva dva."""
    Strng = re.sub('(?<![মব])(্ব)', '্ভ়', Strng)

    return Strng

# frontend
def BengaliTargetVa(Strng):

    """Uses nukta-ba (ভ়) as the target letter for /va/, e.g. ব → va."""
    Strng = Strng.replace('ব', 'ভ়')

    return Strng

# frontend
def BengaliSwitchYaYYa_pre(Strng):
    """Swap Bengali ya (য) and yya (য়) so that ya maps to ẏa and yya maps to ya."""
    Strng = re.sub('(?<!\u09CD)য', '@#$', Strng)
    Strng = re.sub('য়', 'য', Strng)
    Strng = Strng.replace('@#$', 'য়')

    return Strng

# ---- Post-processing options ----

# frontend
def BengaliOldRA(Strng):

    """Uses the old Bengali ra form (ৰ) instead of the standard ra, e.g. র → ৰ."""
    Strng = Strng.replace('র', 'ৰ')

    return Strng

# internal
def BengaliConjunctVB(Strng):

    """Merges ZWNJ-separated virama+ba clusters into a normal conjunct (so kva/kba render alike) and converts khanda-ta+ba to ta+virama+ba."""
    ## kva / kba will be rendered the same
    Strng = Strng.replace('\u09CD\u200C\u09AC', '\u09CD\u09AC')
    Strng = khandatabatova(Strng)

    return Strng

# frontend
def khandatabatova(Strng):

    """Converts khanda-ta followed by ba (with or without an intervening ZWNJ) into full ta+virama+ba, e.g. ৎব → ত্ব."""
    Strng = Strng.replace('ৎব', 'ত্ব')
    Strng = Strng.replace('ৎ\u200Cব', 'ত্ব')

    return Strng

# frontend
def BengaliRaBa(Strng):

    """Treats ৰ as /b/ and ব as /v/, breaking ra conjuncts and inserting joiners to correctly render bra/bya/bru and rba clusters."""
    Strng = Strng.replace('ৰু', 'ৰ‌ু').replace('ৰূ', 'ৰ‌ূ')
    ## Avoid bba -> rra
    ## break all ba conjuncts
    Strng = Strng.replace('\u09CD\u09F0', '\u09CD\u200C\u09F0')

    ## bra/bya bru fix
    Strng = re.sub('(\u09F0)(\u09CD)([\u09B0\u09AF])', r'\1' + '\u200D' + r'\2\3', Strng)
    Strng = re.sub('(\u09F0)(\u09CD)', r'\1\2' + '\u200C', Strng)

    ## rba
    Strng = Strng.replace('র্‌ৰ', 'ৰ্ৰ')

    return Strng

# frontend
def BengaliIntervocalicDDA(Strng):

    """Converts ড/ঢ to their nukta forms ড়/ঢ় in intervocalic position, e.g. দৃঢ আষাঢ → দৃঢ় আষাঢ়."""
    Target = 'Bengali'

    ListC = '|'.join(GM.CrunchSymbols(GM.Characters, Target)+[GM.CrunchList('SignMap',Target)[0]] + ['ৰ'])

    replacements = [('ড', 'ড়'), ('ঢ', 'ঢ়')]

    for x, y in replacements:
        Strng = re.sub('('+ListC+')'+ GM.VedicSvaras + x,r'\1\2'+y,Strng)

    return Strng

# frontend
def BengaliSwitchYaYYa_post(Strng):
    """ya -> yya-with-nukta & yya-with-nukta -> ya (swaps the plain and nuktaed Bengali ya letters)."""
    Strng = re.sub('(?<!\u09CD)য', '@#$', Strng)
    Strng = re.sub('য়', 'য', Strng)
    Strng = Strng.replace('@#$', 'য়')

    return Strng

# frontend
def BengaliYYA(Strng):
    """ya everywhere - yayati yajna -> nukta-ya-yati nukta-yajna (replaces every plain ya with nuktaed yya in Bengali)."""
    from .. import PostProcess
    return PostProcess.YYAEverywhere(Strng, 'Bengali')

