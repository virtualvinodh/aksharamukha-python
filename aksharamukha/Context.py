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
