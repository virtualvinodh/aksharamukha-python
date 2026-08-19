# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass
class ConversionContext:
    # Typed channel for flags passed between convert() pipeline stages, in
    # place of smuggling them as marker characters into the transliterated
    # text (see MARKERS.md for the marker inventory this is meant to
    # replace piece by piece, one marker at a time - not all at once).
    # Created fresh once per convert() call, including recursive pivot
    # calls inside convert() itself - never shared across calls, matching
    # how preoptions/postoptions/nativize are already independently
    # recomputed for each. Mutated in place by whichever stage produces a
    # value and read by whichever stage consumes it; unlike src/tgt/txt/
    # preoptions/postoptions/nativize, it is not threaded through the
    # stage functions' return tuples, since it's passed by identity, not
    # by value.
    is_khuen_target: bool = False
    # Thai/Lao "short vowels not shown" transcription mode - previously a
    # parameter threaded separately alongside ctx through convertScript and
    # gated by hardcoded `Source/Target in ('Thai', 'LaoPali')` checks at
    # every dispatch site. Folded in here so consumers (FixThai, FixLaoPali,
    # FixIndicOutput) just declare ctx and read ctx.transcription_mode -
    # the existing ctx-aware dispatch (GM.resolve, GM.accepts_ctx) already
    # only hands ctx to functions that ask for it, making the hardcoded
    # script-name lists unnecessary.
    transcription_mode: bool = False
