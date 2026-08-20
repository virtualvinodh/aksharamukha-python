# -*- coding: utf-8 -*-

# Aliased: this module's ApplyPreProcessing already uses the local name
# "Options" for its own resolved-option-name list (mirrors PostOptions.py's
# same aliasing, for the same reason).
from . import Options as OptionsModule

# Target -> default preoptions applied unconditionally when converting to
# that target. Inverse counterpart to PostOptions.py's
# _TARGET_DEFAULT_OPTIONS/ApplyScriptDefaults - same shape, pre-conversion
# side - see ApplyPreProcessing below.
#
# Empty for now. This used to have one entry, Target == 'PhagsPa' ->
# ['PhagsPaArrange'] - but ApplyPreProcessing itself was never actually
# called from anywhere in the pipeline (found while auditing for
# duplicate/dead normalization logic), so PhagsPaArrange has been dead
# since some earlier refactor, and separately crashed if a caller tried
# to select it manually via pre_options=['PhagsPaArrange'] (it needs a
# Source argument the single-arg preoptions path never supplied).
#
# Removed rather than silently re-enabled: ScriptProcessing/PhagsPa.py's
# _FixPhagsPaEncode already does its own, independent syllable-spacing on
# the target side (regex-based, using PhagsPa's own consonant/vowel maps),
# and it doesn't produce the same output PhagsPaArrange would add on the
# source side. Reconciling the two - or confirming PhagsPaArrange's extra
# marks are still wanted on top - needs a closer look, ideally from
# someone who actually knows 'Phags-pa orthography, before this fires
# again.
_TARGET_DEFAULT_PREOPTIONS = {
}

def ApplyPreProcessing(Strng, Source, Target, PreOptions=[], ctx=None):
    Options = _TARGET_DEFAULT_PREOPTIONS.get(Target, [])

    for Option in Options:
        if Option.find(Source) != -1:
            Strng = OptionsModule.call_pre_option(Option, Strng, ctx=ctx)
        else:
            Strng = OptionsModule.call_pre_option(Option, Strng, Source, ctx=ctx)

    return Strng
