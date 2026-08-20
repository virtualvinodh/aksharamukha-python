# -*- coding: utf-8 -*-

# TamilSaurashtra's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Tamil

# ---- Pre-processing options ----

# frontend
def SaurastraHaaruColonTamil(Strng):
    """Represents Saurashtra haaru with a colon in Tamil-script text - நீ: → ꢥꢴꢷ."""
    Strng = Strng.replace('ன', 'ந')

    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Tamil'))

    Strng = re.sub('(' + ListVS + ')' + '(:)' , r'\2\1', Strng)

    chars = '([நமரல])'

    Strng = re.sub(chars + ':', r'\1' + '\uA8B4', Strng)

    return Strng

# ---- Post-processing options ----

# frontend
def SaurastraHaaruColon(Strng):
    """Converts Saurashtra haaru into a colon representation - ꢥꢴꢷ → நீ:."""
    vir = Tamil.ViramaMap[0]
    ha = Tamil.ConsonantMap[-1]

    Strng = Strng.replace(vir + ha, ':')

    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Tamil'))

    Strng = re.sub('(:)' + '(' + ListVS + ')', r'\2\1', Strng)

    Strng = re.sub('(\s)(ன)', r'\1' + 'ந', Strng)
    Strng = re.sub('^ன', 'ந', Strng)

    return Strng
