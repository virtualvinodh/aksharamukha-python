# -*- coding: utf-8 -*-

# Thaa's own Fix logic, consolidated out of ConvertFix.py (batch
# migration - see ScriptProcessing/Tamil.py for the pattern this
# follows). No pre/post options exist for this script. Distinct from
# the already-migrated Thaana script. Its bare calls to
# PersoArabicPuntuation are qualified as CF.PersoArabicPuntuation,
# since that helper is genuinely shared/generic and stays behind in
# ConvertFix.py.


def _FixThaaEncode(Strng, Source):
    from .. import ConvertFix as CF
    Strng = CF.PersoArabicPuntuation(Strng, False)
    pass
    #Strng = Strng.replace('â', 'ʾ')

    return Strng

def _FixThaaDecode(Strng, Source):
    from .. import ConvertFix as CF
    Strng = CF.PersoArabicPuntuation(Strng, True)
    pass

    return Strng

def FixThaa(Strng, Source, reverse=False):
    return _FixThaaDecode(Strng, Source) if reverse else _FixThaaEncode(Strng, Source)
