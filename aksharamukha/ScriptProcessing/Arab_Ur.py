# -*- coding: utf-8 -*-

# Arab_Ur's own Fix logic, consolidated out of ConvertFix.py (batch
# migration - see ScriptProcessing/Tamil.py for the pattern this
# follows). No pre/post options exist for this script. Its bare calls
# to FixArab are qualified as CF.FixArab, since FixArab now lives in
# ScriptProcessing/Arab.py.


def _FixArab_UrEncode(Strng, Source):
    from .. import ConvertFix as CF
    Strng = CF.FixArab(Strng, Source, False)

    if Source != 'Type':
        ## introduce hamza
        pass

    return Strng

def _FixArab_UrDecode(Strng, Source):
    from .. import ConvertFix as CF
    Strng = CF.FixArab(Strng, Source, True)

    pass

    return Strng

def FixArab_Ur(Strng, Source, reverse=False):
    return _FixArab_UrDecode(Strng, Source) if reverse else _FixArab_UrEncode(Strng, Source)
