# -*- coding: utf-8 -*-

# Makasar's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
# PostProcess/ConvertFix are imported LOCALLY inside each function that
# needs them (not at module level) - required to avoid a load-order-
# dependent circular import, since ConvertFix.py re-exports names from
# here. See ScriptProcessing/Tamil.py for the full explanation.

import re
from aksharamukha.ScriptMap.EastIndic import Makasar

def _FixMakasarEncode(Strng):

    """Inserts the gemination sign and collapses a doubled Makasar consonant into a single consonant plus the killer sign (Anka)."""
    from .. import PostProcess
    ListC = "|".join(Makasar.ConsonantMap)
    #ListV = "|".join(Makasar.VowelSignMap)
    #print(ListV)
    ListV = "|".join(['\U00011EF3', '\U00011EF4', '\U00011EF5', '\U00011EF6'])
    Anka = '\U00011EF2'
    #print(Makasar.VowelSignMap)

    Strng = PostProcess.InsertGeminationSign(Strng, 'Makasar')
    Strng = Strng.replace('\u02BE', '').replace('\u02BD', '')
    Strng = re.sub('(' + ListC + ')' + '(' + ListV + ')?' + r'\1', r'\1' + r'\2' + Anka, Strng)

    return Strng

def _FixMakasarDecode(Strng):

    """Expands the Makasar killer sign (Anka) marking a doubled consonant back into the repeated consonant sequence."""
    from .. import PostProcess
    ListC = "|".join(Makasar.ConsonantMap)
    #ListV = "|".join(Makasar.VowelSignMap)
    #print(ListV)
    ListV = "|".join(['\U00011EF3', '\U00011EF4', '\U00011EF5', '\U00011EF6'])
    Anka = '\U00011EF2'
    #print(Makasar.VowelSignMap)

    Strng = re.sub('(' + ListC + ')' + '(' + ListV + ')?' + Anka, r'\1' + r'\2' + r'\1', Strng)

    return Strng

def FixMakasar(Strng, reverse=False):

    """Dispatches to the Makasar encode or decode fix-up routine based on the reverse flag."""
    from .. import PostProcess
    return _FixMakasarDecode(Strng) if reverse else _FixMakasarEncode(Strng)
