# -*- coding: utf-8 -*-

# Thai's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).
#
# ThaiSajjhayaOrthography/ThaiSajjhayawithA each independently define the
# SAME option name in both PreProcess.py and PostProcess.py as different
# functions - suffixed _pre/_post here. Each side's own bare call to its
# ThaiSajjhayaOrthography sibling was renamed to the matching suffix.
#
# ThaiReverseVowelSigns/ThaiDigraphConjuncts (ConvertFix.py privates) are
# absorbed here - their only callers anywhere are FixThai and the (now
# co-located) post ThaiSajjhayaOrthography/ThaiTranscription, confirmed
# via a full-codebase reference scan. CF.-qualified call sites
# de-qualified to bare accordingly.
#
# ThaiLaoTranscription stays behind in PostProcess.py - it's genuinely
# shared (also used by LaoPali.py via pp.ThaiLaoTranscription), so
# ThaiTranscription's own bare call to it was re-qualified to
# PostProcess.ThaiLaoTranscription instead.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.EastIndic import Thai

# ---- Fix (encode/decode conversion logic) ----

# internal
def FixThai(Strng,reverse=False,ctx=None):
    """Dispatches Thai fix logic: reverses vowel sign order, resolves digraph conjuncts, and optionally applies phonetic transcription."""
    from .. import PostProcess
    Strng = ThaiReverseVowelSigns(Strng,reverse)
    Strng = ThaiDigraphConjuncts(Strng,reverse)

    transcription_mode = ctx.transcription_mode if ctx is not None else False
    if transcription_mode:
        Strng = PostProcess.ThaiLaoTranscription(Strng,"Thai", '\u0E30', '\u0E31', True)

        Strng = Strng.replace("หฺ์","ห์")

    return Strng

# internal
def ThaiReverseVowelSigns(Strng,reverse=False):
    """Reorders leading Thai vowel signs to/from consonant-first internal order and forms the AM/IM ligatures (◌ํ, ◌ึ)."""
    from .. import ConvertFix as CF
#    EAIO = "".join(Thai.VowelSignMap[9:12])
#    cons = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai"))
#    a = Thai.VowelMap[0]
#    Strng = re.sub("("+cons+")(["+EAIO+"])(?!["+EAIO+"]"+a+")",r"\2\1",Strng)

    Strng = CF.ReverseVowelSigns(Strng,"Thai",reverse)
    if not reverse:
        # VS AA + Anusvara -> VS AM (Ligature)
        # VS I + Anusvara -> VS IM (Ligature)
        Strng = Strng.replace("\u0E32\u0E4D","\u0E33").replace("\u0E34\u0E4D","\u0E36")
    else:
        # Reverse above
        Strng = Strng.replace("\u0E33","\u0E32\u0E4D").replace("\u0E36","\u0E34\u0E4D")

    return Strng

# internal
def ThaiDigraphConjuncts(Strng,reverse=False):
    """Reorders vowel-consonant-virama-consonant sequences to form Thai digraph conjunct clusters, or reverses them."""
    EAIO = "".join(Thai.VowelSignMap[9:12])
    cons = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai"))
    yrlvh = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai")[25:29] + GM.CrunchSymbols(GM.Consonants, "Thai")[32:33])
    sh = "|".join(Thai.ConsonantMap[31:33])
    vir = Thai.ViramaMap[0]

    #Replace \s with all punctuations
    if not reverse:
        # Comments
        Strng = re.sub("(?<=\s)("+cons+")"+"("+vir+")"+"(["+EAIO+"])"+"("+cons+")",r"\3\1\2\4",Strng)
        Strng = re.sub("("+cons+")"+"("+vir+")"+"(["+EAIO+"])"+"("+yrlvh+")",r"\3\1\2\4",Strng)
        Strng = re.sub("("+sh+")"+"("+vir+")"+"(["+EAIO+"])"+"("+cons+")",r"\3\1\2\4",Strng)
    else:
        ## Reverse the above.
        Strng = re.sub("(["+EAIO+"])"+"("+vir+")"+"("+cons+")",r"\2\3\1",Strng)

    return Strng

# ---- Pre-processing options ----

# frontend
def ThaiOrthography(Strng):

    """Marks text as standard Thai orthography - e.g. พุทธะ."""
    return Strng

# frontend
def ThaiPhonetic(Strng):
    """Converts to Thai phonetic transcription: ด→ท, บ→พ, marks aspirated ก/จ with a dot-below, and strips nikkhahit/tone marks - e.g. ตะต͜ระ ราจ̥ะ."""
    Strng = Strng.replace('ด', 'ท')
    Strng = Strng.replace('บ', 'พ')
    Strng = Strng.replace('ก\u0325', 'ค')
    Strng = Strng.replace('จ\u0325', 'ช')
    Strng = Strng.replace('งํ', 'ง')

    Strng = Strng.replace('\u035C', '')

    Strng = Strng.replace('\u0E47', '')

    return Strng

# frontend
def ThaiSajjhayaOrthography_pre(Strng):
    """Pre-processes text for Thai Sajjhāya orthography by converting anusvara/tone marks to the subscript virama sign and dropping the short-a conjunct."""
    Script = "Thai"

    #cons = "|".join(GM.CrunchSymbols(GM.Consonants, Script)+GM.CrunchList('VowelMap',Script)[0:1])
    #EAIO = "".join(GM.CrunchList('VowelSignMap',Script)[9:12]+GM.CrunchList('SinhalaVowelSignMap',Script)[:])
    ## Reorder dve
    #Strng = re.sub('([' + EAIO + '])' + '(' + cons  + ')' + '(๎)' + '(' + cons + ')', r'\2\3\1\4', Strng)

    Strng = Strng.replace('ัง', 'ังฺ')
    Strng = Strng.replace('์', 'ฺ')
    Strng = Strng.replace('๎', 'ฺ')
    Strng = Strng.replace('ั', '')

    return Strng

# frontend
def ThaiSajjhayawithA_pre(Strng):
    """Strips the short-a sign then applies the Thai Sajjhāya orthography pre-processing."""
    Strng = Strng.replace('ะ', '')
    Strng = ThaiSajjhayaOrthography_pre(Strng)

    return Strng

# ---- Post-processing options ----

# frontend
def ThaiNativeConsonants(Strng):
    """Converts to native Thai phonetic consonant forms - พุทฺธตฺว → บุดธะต͜วะ."""
    Strng = Strng.replace('ท', 'ด')
    Strng = Strng.replace('พ', 'บ')
    Strng = Strng.replace("\u0E36","\u0E34\u0E4D")
    Strng = Strng.replace('ํ', 'งฺ')

    Strng = re.sub('(\u0E3A)([ยรลวห])', '\u035C'+ r'\2', Strng)
    Strng = Strng.replace('ห\u0E3A', 'ห\u035C')

    Strng = re.sub('([ยรลวห])' + '\u035C' + r'\1', r'\1' + '\u0E3A' + r'\1', Strng)

    Strng = re.sub('(า)(.)(ฺ)', '็' + r'\1\2\3', Strng)
    Strng = re.sub('([เโ])(.)(.)(ฺ)',  r'\1\2' + '็' +  r'\3\4', Strng)

    Strng = ThaiTranscription(Strng, False)

    Strng = Strng.replace('ะ͜', '\u035C')
    Strng = Strng.replace('ะ็', '็')
    Strng = re.sub('([เโไ])(.)(\u035C)(.)([ะ\u0E31])', r'\1\2\3\4', Strng)

    Strng = Strng.replace('ค', 'ก\u0325')
    Strng = Strng.replace('ช', 'จ\u0325')

    Strng = Strng.replace('ํ', 'ง')
    Strng = Strng.replace('ง', 'งํ')

    Strng = Strng.replace('ะงํ\u035C', '\u0E31งํ')

    Strng = re.sub('([เโไ])(งํ)([าัะ])', r'\1' + 'ง' + r'\2', Strng)
    Strng = re.sub('([เโไ])(งํ)', r'\1' + 'ง', Strng)
    Strng = re.sub('(งํ)([าัะ])', 'ง' + r'\2', Strng)

    return Strng

# frontend
def ThaiSajjhayaOrthography_post(Strng, Script = "Thai"):
    ## reverse digraphs
    """Post-processes Thai (or Lao Pali) text into Sajjhāya orthography, inserting joiners between consonant clusters and reordering digraphs."""
    Strng = ThaiReverseVowelSigns(Strng, True)
    Strng = ThaiDigraphConjuncts(Strng, True)
    Strng = ThaiReverseVowelSigns(Strng)

    if Script == "Thai":
        Strng = Strng.replace('ฺ', '์')
    if Script == "LaoPali":
        Strng = Strng.replace('຺', '์')

    cons = "|".join(GM.CrunchSymbols(GM.Consonants, Script)+GM.CrunchList('VowelMap',Script)[0:1])
    EAIO = "".join(GM.CrunchList('VowelSignMap',Script)[9:12]+GM.CrunchList('SinhalaVowelSignMap',Script)[:])

    # short a for conjuncts : t(a)ssa
    Strng = re.sub('(?<![' + EAIO + '])' + '(' + cons + ')' + '(' + cons + ')' + '(์)', r'\1' + 'ั' + r'\2\3', Strng)

    if Script == "Thai":
        cons_others  = '([ยรลวศษสหฬ])' # avarga
    if Script == "LaoPali":
        cons_others = '([ຍຣລວຨຩສຫຬ])' # avarga

    Strng = re.sub('(?<![' + EAIO + '])' + '(' + cons + ')' + '(' + cons + ')' + '(์)', r'\1' + 'ั' + r'\2\3', Strng)

    # varga + avaraga or avarga + varga add joiner
    # hma, mha etc.
    Strng = re.sub('(' + cons + ')' + '(์)' + '([' + EAIO + ']?)' + cons_others , r'\1' + '๎' + r'\3\4', Strng)
    Strng = re.sub(cons_others + '(์)' + '([' + EAIO + ']?)' + '(' + cons + ')', r'\1' + '๎' + r'\3\4', Strng)

    ## ssa, lla, nna do no add joiner
    Strng = re.sub(cons_others + '(๎)' + '([' + EAIO + ']?)' + r'\1' , r'\1' + '์' + r'\3\1', Strng)

    #reorder dve sme
    Strng = re.sub('(' + cons  + ')' + '(๎)' + '([' + EAIO + '])' + '(' + cons + ')', r'\3\1\2\4', Strng)

    if Script == "Thai":
        Strng = Strng.replace('ง์', 'ง')
        Strng = re.sub('(\u0E31)(.)(\u0E4E)', r'\2\3', Strng)

    if Script == "LaoPali":
        Strng = Strng.replace('ั', 'ັ')
        Strng = Strng.replace("ງ์", "ງ")
        Strng = Strng.replace("์", "໌")
        Strng = re.sub('(\u0EB1)(.)(\u0E4E)', r'\2\3', Strng)

        Strng = Strng.replace('\u0E4E', '\u0ECE')

    #Strng = re.sub('([ยรลวศษสหฬ])(์)', r'\1' + '๎', Strng)

    return Strng

# frontend
def ThaiSajjhayawithA_post(Strng):
    """Post-processes text into nativized Sajjhāya-with-a orthography by applying transcription with anusvara restoration."""
    Strng = ThaiSajjhayaOrthography_post(Strng)
    Strng = Strng.replace('ัง','ังฺ')
    Strng = ThaiTranscription(Strng, anusvaraChange = True)

    Strng = Strng.replace('ะํ', 'ํ')
    Strng = Strng.replace('ะั', 'ั')
    Strng = Strng.replace('ะ๎', '๎')

    Strng = re.sub('([เโไ])(.๎)([ยรลวศษสหฬ])ะ', r'\1\2\3', Strng)

    Strng = Strng.replace("\u0E32\u0E4D", "\u0E33").replace("\u0E34\u0E4D", "\u0E36") # reverse AM, iM

    return Strng

# frontend
def ThaiTranscription(Strng, anusvaraChange = True):
    """Converts Thai script to phonetic transcription orthography by reversing digraphs and applying short-a insertion rules - พุทฺธ → พุทธะ."""
    from .. import PostProcess

    ## reverse digraphs
    Strng = ThaiReverseVowelSigns(Strng, True)
    Strng = ThaiDigraphConjuncts(Strng, True)
    Strng = ThaiReverseVowelSigns(Strng)

    Strng = PostProcess.ThaiLaoTranscription(Strng,"Thai", '\u0E30', '\u0E31', anusvaraChange = anusvaraChange)

    Strng = Strng.replace('ะ์','์')

    Strng = Strng.replace('ะงัง', '\u0E31งํ')

    #print(Strng)

#    shortA = u'\u0E30'
#    shortAconj = u'\u0E31'
#    cons = "|".join(GM.CrunchSymbols(GM.Consonants, "Thai")+Thai.VowelMap[0:1])
#    vir = Thai.ViramaMap[0]
#    AIUVir = "".join(Thai.VowelSignMap[0:5]+[vir])
#    EAIO = "".join(Thai.VowelSignMap[9:12])
#    Anu = Thai.AyogavahaMap[1]
#    ng = Thai.ConsonantMap[4]
#
#    Strng = AnusvaraToNasal(Strng,"Thai")
#
#    Strng = re.sub("(["+EAIO+"])"+"("+cons+")"+"("+vir+")",r'\2\3\1',Strng) #Reverse bre, bro etc
#    Strng = Strng.replace(u"\u0E33",u"\u0E32\u0E4D").replace(u"\u0E36",u"\u0E34\u0E4D") # reverse AM, iM
#    Strng = re.sub("(?<!["+EAIO+"])"+"("+cons+")"+"(?!["+AIUVir+"])",r'\1'+shortA,Strng)
#    Strng = Strng.replace(Anu,ng)
#    Strng = Strng.replace(vir,"")
#    Strng = re.sub("("+shortA+")"+"(?=("+cons+")"+"("+cons+"|"+"["+EAIO+"]))",shortAconj,Strng)

    return Strng

# frontend
def ThaiVisargaSaraA(Strng):
    """Converts the visarga-style ห์ marker back into the short-a sign ะ - นมัห์ → นมะ."""
    Strng = Strng.replace('ห์','ะ')

    return Strng
