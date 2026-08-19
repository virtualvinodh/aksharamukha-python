# -*- coding: utf-8 -*-

# Wancho's own Fix logic, consolidated out of ConvertFix.py (batch migration -
# see ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re

def _FixWanchoEncode(Strng):
    """Encode romanized input into native Wancho script: convert ASCII tone-mark escapes to tone codepoints, fuse nasalization/anusvara markers with their vowels, and merge digraph/WA ligatures into single codepoints."""
    tonemarks = ['\U0001E2EC', '\U0001E2ED', '\U0001E2EE', '\U0001E2EF']
    tonewri = ['\\_', '\\-', '\\!', '\\;']

    nasalization = ['\U0001E2E6', '\U0001E2E7', '\U0001E2E8', '\U0001E2EA'] # o, e, aa , u ; nasalization
    nasvowels = ['\U0001E2D5', '\U0001E2DB', '\U0001E2C0', '\U0001E2DE']

    Anusvaras = ['\U0001E2E2', '\U0001E2E3', '\U0001E2E4', '\U0001E2E5'] # o, aa, a, i
    AnusvaraVowels = ['\U0001E2D5', '\U0001E2C0', '\U0001E2C1', '\U0001E2DC']

    for x, y in zip(tonemarks, tonewri):
        Strng = Strng.replace(y, x)

    for x, y in zip(nasvowels, nasalization):
        Strng = Strng.replace(x + 'ʿ', y)

    Strng = Strng.replace('ʿ', '𞋉')

    for x, y in zip(AnusvaraVowels, Anusvaras):
        Strng = Strng.replace(x + 'ʾ', y)

    Strng = Strng.replace('ʾ', '𞋝')

    Strng = Strng.replace('𞋋𞋗', '\U0001E2E1')
    Strng = Strng.replace('𞋋𞋎', '\U0001E2E0')

    Strng = Strng.replace('𞋓Ø', '\U0001E2D2') ## WA
    Strng = Strng.replace('Ø', '')



    return Strng

def _FixWanchoDecode(Strng):
    """Decode native Wancho script back to its romanized representation: expand tone codepoints to ASCII escapes, split fused nasalization/anusvara vowels into vowel+marker sequences, and expand merged ligatures."""
    tonemarks = ['\U0001E2EC', '\U0001E2ED', '\U0001E2EE', '\U0001E2EF']
    tonewri = ['\\_', '\\-', '\\!', '\\;']

    nasalization = ['\U0001E2E6', '\U0001E2E7', '\U0001E2E8', '\U0001E2EA'] # o, e, aa , u ; nasalization
    nasvowels = ['\U0001E2D5', '\U0001E2DB', '\U0001E2C0', '\U0001E2DE']

    Anusvaras = ['\U0001E2E2', '\U0001E2E3', '\U0001E2E4', '\U0001E2E5'] # o, aa, a, i
    AnusvaraVowels = ['\U0001E2D5', '\U0001E2C0', '\U0001E2C1', '\U0001E2DC']

    for x, y in zip(tonemarks, tonewri):
        Strng = Strng.replace(x, y)

    for x, y in zip(nasvowels, nasalization):
        Strng = Strng.replace(y, x + 'ʿ')

    for x, y in zip(AnusvaraVowels, Anusvaras):
        Strng = Strng.replace(y, x + 'ʾ')

    Strng = Strng.replace('\U0001E2E1', '𞋋𞋗')
    Strng = Strng.replace('\U0001E2E0', '𞋋𞋎')

    Strng = Strng.replace('\U0001E2D2', '𞋓Ø') ## WA


    return Strng

def FixWancho(Strng, reverse=False):
    """Core Wancho encode/decode entry point: encode into Wancho script by default, or decode out of it back to internal representation when reverse=True."""
    return _FixWanchoDecode(Strng) if reverse else _FixWanchoEncode(Strng)
