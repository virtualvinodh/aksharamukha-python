# -*- coding: utf-8 -*-

# PhagsPa's own Fix/pre-option/post-option logic, consolidated out of
# ConvertFix.py/PreProcess.py/PostProcess.py (batch migration - see
# ScriptProcessing/Tamil.py for the full rationale/pattern this follows).

import re
from .. import GeneralMap as GM
from .. import ScriptRegistry as SR
from aksharamukha.ScriptMap.EastIndic import PhagsPa

# ---- Fix (encode/decode conversion logic) ----

# internal
def _FixPhagsPaEncode(Strng):
    """Reorders candrabindu and subjoined consonants, removes viramas, and inserts syllable-separating spaces for 'Phags-pa encoding."""
    candraBindu = PhagsPa.AyogavahaMap[0]
    ListC = "|".join(sorted(PhagsPa.ConsonantMap,key=len,reverse=True)) #Do this for all
    ListV = "|".join(sorted(PhagsPa.VowelMap,key=len,reverse=True))
    ListVS = "|".join(sorted(PhagsPa.VowelSignMap,key=len,reverse=True))

    vir  = PhagsPa.ViramaMap[0]
    Virrvy = [vir+x for x in [PhagsPa.ConsonantMap[c] for c in [25,26,28]]]
    Subrvy = ['\uA868','\uA871','\uA867']

    SubrvyE = ['ꡱꡨ'] + Subrvy


    # Removing Indep. Vowel Sign
    #ListV = ListV.replace("\u1E7F","")
    #Strng = Strng.replace("\u1E7F","")

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(x,y)

    Strng = re.sub("("+ListV+")"+"("+candraBindu+")",r'\2\1',Strng)

    # Move Chandrabindu - bhrUM
    Strng = re.sub("("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?)"+"("+candraBindu+")",r'\6\1\2\4',Strng)
    # Move Sigh Candrabindu

    # Move Vowel Sign AA for subjoining vowels ## Not moving
   #  Strng = re.sub("(["+"".join(Subrvy[1])+"])"+"("+PhagsPa.VowelSignMap[0]+")",r'\2\1',Strng)


    ## Fix rka - superfixed ra ; rka used only for Specific Tibetan context.
    Strng = Strng.replace(" ", "᠂")
    Strng = Strng.replace("\u02BD","")

    ## separate syllables

    #Strng = re.sub("(?<!ꡖ)" + "(" + "(" + ListV +")" + ")" + "(?!" + ListCVir + ")", r'\1' + ' ', Strng)
    #Strng = re.sub("(" + "(" + ListC +")" + "(" + "|".join(Subrvy) + ")?" + "(" + ListVS + ")" + ")" + "(?!" + ListCVir + ")", r'\1' + ' ', Strng)
    #Strng = Strng.replace("")
    #Strng = re.sub("(" + "(" + ListC +")" + "(" + "|".join(Subrvy) + ")?" + "(?!" + ListCVir + ")" + ")", r'\1' + ' ', Strng)

    ## sakv sakr not changing properly
    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \8', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \8', Strng)

    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \4', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" +
        "(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" + "(?!" + vir + ")", r'\1 \4', Strng)

    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \8', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?))" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \8', Strng)

    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \4', Strng)
    Strng = re.sub("(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")" +
        "(("+candraBindu+")?"+"("+ListV+"))" + "(?!" + vir + ")", r'\1 \4', Strng)

    Strng = Strng.replace("\n","\n")

    #Strng = "(" + "(" + ListC +")" + "(" + "|".join(Subrvy) + ")?" + "(" + ListVS + ")" + ")" + "(?!" + ListCVir + ")"

    Strng = '\u12BA᠂' + Strng

    ListCE = ListC + "|" + "|".join(SubrvyE)

    ## Probably add more punctuations
    Strng = re.sub('(?:(?<!\n)(?<!᠂)(?<![,\.\"\?\&\(\)]))' + "(?<!" + vir + ")" + '(' + ListC + ')' + vir + "((" + candraBindu +")?" + "("+ListC+"))",r"\1 \2", Strng) #\u02BF Virama
    Strng = re.sub('(?<!᠂)' + '(' + ListC + ')' + vir + "((" + candraBindu +")?" + "("+ListV+"))",r" \1", Strng) #\u02BF Virama

    Strng = Strng.replace(vir,"") #\u02BF Virama
    Strng = Strng.replace("\u1E7F","")
    Strng = Strng.replace("\u1E7E","")
    Strng = Strng.replace("\u12BA᠂","")

    Strng = Strng.replace("᠂", " ᠂ ")


    #print Strng



    return Strng

# internal
def _FixPhagsPaDecode(Strng):
    """Reconstructs viramas between 'Phags-pa syllables, expands aspirate letter markers, and reverses subjoined consonant and candrabindu placement when decoding."""
    candraBindu = PhagsPa.AyogavahaMap[0]
    ListC = "|".join(sorted(PhagsPa.ConsonantMap,key=len,reverse=True)) #Do this for all
    ListV = "|".join(sorted(PhagsPa.VowelMap,key=len,reverse=True))
    ListVS = "|".join(sorted(PhagsPa.VowelSignMap,key=len,reverse=True))

    vir  = PhagsPa.ViramaMap[0]
    Virrvy = [vir+x for x in [PhagsPa.ConsonantMap[c] for c in [25,26,28]]]
    Subrvy = ['\uA868','\uA871','\uA867']

    SubrvyE = ['ꡱꡨ'] + Subrvy


    ListV = ListV.replace("\u1E7F","")

    Strng = Strng.replace('ꡖꡘꡟ','ꡱꡖꡟ')

    Aspirate = [('\uA842\uA85C','\u1E7E\uA842\u1E7E\uA85C\u1E7E'), ('\uA852\uA85C','\u1E7E\uA852\u1E7E\uA85C\u1E7E'), ('\uA86B\uA85C','\u1E7E\uA86B\u1E7E\uA85C\u1E7E'),
        ('\uA84A\uA85C','\u1E7E\uA84A\u1E7E\uA85C\u1E7E'),('\uA84E\uA85C','\u1E7E\uA84E\u1E7E\uA85C\u1E7E')]

    for x,y in Aspirate:
        Strng = Strng.replace(x,y)

    Strng = re.sub("("+PhagsPa.VowelSignMap[0]+")"+"(["+"".join(Subrvy[1])+"])",r'\2\1',Strng)
    Strng = re.sub("("+candraBindu+')'+"("+ListC+')'+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+')?)',r'\2\3\5\1',Strng)
    Strng = re.sub("("+candraBindu+')'+'('+ListV+')',r'\2\1',Strng)

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(y,x)

    # Fixing  + Indepdendent vowels.
    Strng = re.sub("("+ListV+")","\u1E7F"r"\1",Strng)
    Strng = re.sub("("+ListC+"|ꡖ)"+"("+"\u1E7F"+")",r'\1',Strng)

    ## Fix rka - superfixed ra ; rka used only for Specific Tibetan context.
    Strng = Strng.replace("ꡆ","ꡒ")

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(x,y)

    #print(Strng)

    ## Fix splavya
    Strng = re.sub("((" + ListC + ")" + "(("+"|".join(SubrvyE)+")?)" + "(?!" + ListVS + "))"
        + "((("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+"))" + "("+candraBindu+")?))"  , r"\1" + vir + r"\6", Strng)


    Strng = re.sub("((("+ListC+")"+"(("+"|".join(SubrvyE)+")?)"+"(("+ListVS+")?)" + "("+candraBindu+")?)"
        + "((" + ListC + ")" + "(("+"|".join(SubrvyE)+")?)" + "(?!" + ListVS + ")))" , r"\1" + vir, Strng)

    Strng = re.sub("((("+ListV+")" + "("+candraBindu+")?)"
        + "((" + ListC + ")" + "(("+"|".join(SubrvyE)+")?)" + "(?!" + ListVS + ")))" , r"\1" + vir, Strng)

    for x,y in zip(Virrvy,Subrvy):
        Strng = Strng.replace(y,x)

    Strng = Strng.replace(" ", "")
    Strng = Strng.replace("᠂"," ")
    Strng = Strng.replace("᠃"," ")

    Strng = Strng.replace(vir + vir, vir)

    # ꡳꡊꡞꡚ ꡩꡖ ꡗ ---> diMSTAya
    # Fix Aspirated add the extra character
    # Fix saphA -> sphA ; sata -> sat ; suda -> sud
    # Add options to retain space
    #Strng = Strng.replace("(" + ListC + ")")


    return Strng

# internal
def FixPhagsPa(Strng,reverse=False):
    """Dispatches to the 'Phags-pa encode or decode fix-up routine based on the reverse flag."""
    return _FixPhagsPaDecode(Strng) if reverse else _FixPhagsPaEncode(Strng)

# ---- Pre-processing options ----

# internal (test fixture only)
def PhagsPaArrange(Strng,Source):
    """Inserts spaces between consonant-vowel syllable clusters when arranging 'Phags-pa output for Indic-derived source scripts."""
    if SR.get(Source).is_indic:
        ListC = "|".join(sorted(GM.CrunchSymbols(GM.Consonants, Source),key=len,reverse=True)) #Do this for all
        ListV = "|".join(sorted(GM.CrunchSymbols(GM.Vowels, Source),key=len,reverse=True))
        ListVS = "|".join(sorted(GM.CrunchSymbols(GM.VowelSignsNV, Source),key=len,reverse=True))
        ListCS = "|".join(sorted(GM.CrunchSymbols(GM.CombiningSigns, Source),key=len,reverse=True))

        vir = GM.CrunchSymbols(GM.VowelSigns,Source)[0]

        yrv = "|".join([GM.CrunchSymbols(GM.Consonants, Source)[i] for i in [25,26,28]])

        Strng = re.sub("("+ListC+")"+"("+vir+")"+"("+yrv+")"+"("+"("+ListVS+")?"+"("+ListCS+")?"+")",r' \1\2\3\4',Strng)
        Strng = re.sub("("+ListC+ListV+")"+"("+"("+ListVS+")?"+"("+ListCS+")?"+")"+"("+ListC+")"+"("+vir+")"+"(?!\s)",r"\1\2\5\6 ",Strng)
        Strng = re.sub("("+ListC+ListV+")"+"("+"("+ListVS+")?"+"("+ListCS+")?"+")"+"("+ListC+")"+'(?!'+vir+')',r"\1\2 \5",Strng)
        Strng = re.sub("("+ListC+ListV+")"+"("+"("+ListVS+")?"+"("+ListCS+")?"+")"+"("+ListC+")"+'(?!'+vir+')',r"\1\2 \5",Strng)

    elif SR.get(Source).is_latin:
        pass

    return Strng

# ---- Post-processing options ----

# frontend
def PhagsPaTib(Strng):

    """Selects Tibetan-style 'Phags-pa rendering (currently a no-op placeholder)."""
    return Strng

# frontend
def PhagsPaSeal(Strng):

    """Selects seal-script-style 'Phags-pa rendering (currently a no-op placeholder)."""
    return Strng

# internal (test fixture only)
def PhagsPaRearrange(Strng,Target):
    """Inserts virama before word-final 'Phags-pa consonants (marked by trailing spaces), then converts remaining spaces and Mongolian-style punctuation into 'Phags-pa segment markers."""
    vir = GM.CrunchList('ViramaMap', Target)[0]
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants,Target))
    ListV = '|'.join(GM.CrunchSymbols(GM.Vowels,Target))
    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSignsNV,Target))

    Strng = re.sub("(?<!( |"+vir+"))"+"("+ListC+")"+"(?= )",r'\2'+vir,Strng)
    #print Strng

    Strng = Strng.replace(" ","").replace("᠂"," ").replace("᠃"," ")
    return Strng

