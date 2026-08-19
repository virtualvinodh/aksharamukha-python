# -*- coding: utf-8 -*-

# Tamil's own Fix/pre-option/post-option logic, consolidated into one file
# instead of being split across ConvertFix.py/PreProcess.py/PostProcess.py.
# ConvertFix.py/PreProcess.py/PostProcess.py re-export these names (see the
# `from .ScriptProcessing.Tamil import ...` lines in each) so every existing
# dispatch mechanism - Options.py's getmembers()-based pre/post-option
# discovery, Convert.py's GM.resolve(CF, "Fix"+Source, ...) - keeps working
# unchanged; only where the code actually LIVES has moved.
#
# PostProcess/ConvertFix (needed for RetainDandasIndic/RetainIndicNumerals/
# CorrectRuLu/ShiftDiacritics) are deliberately NOT imported at module level
# here - this file sits in a three-way import cycle with ConvertFix.py and
# PostProcess.py (each re-exports names from here, and the functions below
# call back into both). A module-level `from .. import PostProcess` works
# fine when THIS module is reached via ConvertFix.py or PostProcess.py
# already loading (the module object exists in sys.modules early, even
# partially initialized, and attribute access is deferred to call time) -
# but breaks if this module is ever imported first/standalone, since the
# `from .ScriptProcessing.Tamil import FixTamil, ...` re-export lines in
# ConvertFix.py/PostProcess.py need the name to already exist, not just the
# module object. Importing PostProcess/ConvertFix locally, inside each
# function that needs them, sidesteps this entirely - matches how the
# original (pre-move) TamilAddFirstVarga already did a local `from . import
# ConvertFix` for the same reason, just applied consistently here.

import re
from .. import GeneralMap as GM
from aksharamukha.ScriptMap.MainIndic import Tamil

def FixTamil(Strng,reverse=False):
    """Dispatches to the Tamil encode or decode fix-up routine based on the reverse flag."""
    return _FixTamilDecode(Strng) if reverse else _FixTamilEncode(Strng)

def _FixTamilEncode(Strng):
    """Corrects Tamil vocalic ru/lu forms, retains dandas and native numerals, and reorders superscript diacritics before Vedic accent marks."""
    from .. import ConvertFix as CF
    from .. import PostProcess
    Strng = CF.CorrectRuLu(Strng,"Tamil",False)

    ava = Tamil.SignMap[0]
    avaA = '\u0028\u0B86\u0029'

    VedicSign = ['॑', '॒', '᳚']
    TamilDiacritic = ['ʼ', 'ˮ', '꞉']#, '²', '³', '⁴', '₂', '₃', '₄']

    Strng = Strng.replace(ava+ava,avaA)
    Strng = PostProcess.RetainDandasIndic(Strng, 'Tamil', True)
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Tamil', True)

    for x in TamilDiacritic:
        for y in VedicSign:
            Strng = Strng.replace(x + y, y + x)

    return Strng

def _FixTamilDecode(Strng):
    """Reverses Tamil vocalic ru/lu correction, danda/numeral retention, and diacritic ordering, and restores grantha visarga and the ஷ² ligature."""
    from .. import ConvertFix as CF
    from .. import PostProcess
    Strng = CF.CorrectRuLu(Strng,"Tamil",True)

    ava = Tamil.SignMap[0]
    avaA = '\u0028\u0B86\u0029'

    VedicSign = ['॑', '॒', '᳚']
    TamilDiacritic = ['ʼ', 'ˮ', '꞉']#, '²', '³', '⁴', '₂', '₃', '₄']

    Strng = PostProcess.RetainDandasIndic(Strng, 'Tamil')
    Strng = PostProcess.RetainIndicNumerals(Strng, 'Tamil')
    Strng = Strng.replace(avaA,ava+ava)
    Strng = Strng.replace('ஷ²', 'ஶ')

    Strng = Strng.replace('𑌃', '꞉')

    for x in TamilDiacritic:
        for y in VedicSign:
            Strng = Strng.replace(y + x, x + y)

    return Strng


def TamilNumeralSub(Strng):
    """Converts diacritic digit suffixes into Tamil superscript numerals used to mark Grantha consonants, e.g. க2 க3 க4 → க² க³ க⁴."""
    ListC = '(' + '[கசடதபஜஸ]' + ')'
    ListV = '(' + '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Tamil')) + ')'

    Strng = re.sub(ListC + ListV + '2', r'\1\2' + '²', Strng)
    Strng = re.sub(ListC + ListV + '3', r'\1\2' + '³', Strng)
    Strng = re.sub(ListC + ListV + '4', r'\1\2' + '⁴', Strng)

    Strng = re.sub(ListC + '2', r'\1' + '²', Strng)
    Strng = re.sub(ListC + '3', r'\1' + '³', Strng)
    Strng = re.sub(ListC + '4', r'\1' + '⁴', Strng)

    Strng = Strng.replace('ரு\'', 'ருʼ')
    Strng = Strng.replace('ரு’', 'ருʼ')

    Strng = Strng.replace('ம்\'', 'ம்ʼ')
    Strng = Strng.replace('ம்’', 'ம்ʼ')

    return Strng

def TamilTranscribeCommon(Strng, c = 31):
    """Implements shared Tamil phonetic transcription rules: intervocalic/post-nasal consonant voicing, sandhi assimilations, and letter simplifications."""
    script = "Tamil"

    ListC = GM.CrunchList('ConsonantMap',script)
    ListSC = GM.CrunchList('SouthConsonantMap',script)
    vir = GM.CrunchSymbols(GM.VowelSigns, script)[0]

    ConUnVoiced = [ListC[x] for x in [0,5,10,15,20]]
    ConVoicedJ =  [ListC[x] for x in [2,7,12,17,22]]
    ConVoicedS =  [ListC[x] for x in [2,31,12,17,22]]

    ConNasalsAll = '|'.join([ListC[x] for x in [4, 9, 14, 19, 24]])
    conNasalCa = '|'.join([ListC[x] for x in [9]])
    ConNasalsGroup = [ConNasalsAll, conNasalCa, ConNasalsAll, ConNasalsAll, ConNasalsAll]

    ConMedials = '|'.join(ListC[25:28]+ListSC[0:2]+ListSC[3:4])
    Vowels = '|'.join(GM.CrunchSymbols(GM.Vowels+GM.VowelSignsNV, script))
    Aytham = GM.CrunchList('Aytham',script)[0]
    Consonants = '|'.join(GM.CrunchSymbols(GM.Consonants,script))
    NRA =ListSC[3] + vir + ListSC[2]
    NDRA = ListC[14] + vir + ListC[12] + vir + ListC[26]

    ### Check Siva Siva Mails
    ### Do something about Eyelash ra in Transliterated text

    for i in range(len(ConUnVoiced)):
        pass
        #Strng = re.sub('('+Vowels+Consonants+')'+ConUnVoiced[i]+'('+Vowels+Consonants+')',r'\1'+ConVoicedS[i]+r'\2',Strng)
        Strng = re.sub('('+Vowels+'|'+Consonants+'|'+Aytham+')'+ConUnVoiced[i]+'(?!'+vir+')',r'\1'+ConVoicedS[i],Strng)
        Strng = re.sub('([³])'+ConUnVoiced[i]+'(?!'+vir+')',r'\1'+ConVoicedS[i],Strng)
        Strng = re.sub('³+', '³', Strng)

        # Nasals + Unvoiced -> voiced
        # Rule applied even if spaced -> ulakaJ cuRRu -> ulakaJ juRRu; cenJu -> senju
        # Strng = re.sub('('+ConNasalsSpace+')'+'('+vir+')'+'( ?)'+ConUnVoiced[i],r'\1\2\3'+ConVoicedJ[i],Strng)

        # Only without space : vampu -> vambu;  varim panam -> varim panam
        Strng = re.sub('('+ConNasalsGroup[i]+')'+'('+vir+')'+ConUnVoiced[i],r'\1\2'+ConVoicedJ[i],Strng)

        # Medials + Unvoiced -> Voiced
        Strng = re.sub('('+ConMedials+')'+'('+vir+')'+ConUnVoiced[i]+'(?!'+vir+')',r'\1\2'+ConVoicedS[i],Strng)

    Strng = Strng.replace(NRA,NDRA)

    # Intervocalic S
    Strng = re.sub('(?<!'+'('+ListC[5]+'|'+ListSC[2] +'|' + 'ட' + ')'+vir+')'+ListC[5]+'(?!'+vir+')',ListC[c],Strng)

    import string

    punct = "|".join(['\\'+x for x in list(string.punctuation.replace(".","").replace("?",""))])+"|\s"

    # CA + Spac | Punct + SA -> CCA
    Strng = re.sub('('+ListC[5]+vir+')'+'(('+punct+')+)'+'('+ListC[c]+')',r'\1\2'+ListC[5],Strng)

    # JA + Spac | Punct + SA -> JCA
    Strng = re.sub('('+ListC[9]+vir+')'+'(('+punct+')+)'+'('+ListC[c]+')',r'\1\2'+ListC[7],Strng)

    # GA + Spac | Punct + KA ->
    Strng = re.sub('('+ListC[4]+vir+')'+'(('+punct+')+)'+'('+ListC[0]+')',r'\1\2'+ListC[2],Strng)

    # NA + Spac | Punct + TTA ->
    Strng = re.sub('('+ListC[14]+vir+')'+'(('+punct+')+)'+'('+ListC[10]+')',r'\1\2'+ListC[12],Strng)

    # NA + Spac | Punct + TA ->
    Strng = re.sub('('+ListC[19]+vir+')'+'(('+punct+')+)'+'('+ListC[15]+')',r'\1\2'+ListC[17],Strng)

    # K + k -> hh
    Strng = Strng.replace(Tamil.Aytham[0]+ListC[0],ListC[32]+vir+ListC[32])

    # K -> H
    Strng = Strng.replace(Tamil.Aytham[0],ListC[32]+vir)

    # RR + RRA -> TT+RA
    Strng = re.sub(ListSC[2]+vir+ListSC[2],ListC[10]+vir+ListC[26],Strng)

    # RR | TT + /s + SA -> RR + /s + CA
    Strng = re.sub("("+'['+ListC[10]+ListSC[2]+']'+vir+')'+'(\s)'+'('+ListC[c]+')',r'\1\2'+ListC[5],Strng)

    ## NNN to N, RR to R

    Strng = Strng.replace(ListSC[3],ListC[19])
    #Strng = Strng.replace(ListSC[2],ListC[26])

    return Strng

def TamilTranscribe(Strng):
    """Transcribes Tamil script into its standard spoken pronunciation, e.g. மதம், பேசு → madam, pēsu."""
    Strng = TamilTranscribeCommon(Strng)

    return Strng

def TamilTranscribeDialect(Strng):
    """Transcribes Tamil script into its dialectal spoken pronunciation, e.g. மதம், பேசு → madam, pēśu."""
    Strng = TamilTranscribeCommon(Strng, c=29)

    return Strng


def TamilNaToNNa(Strng):
    """Converts dental na (ந) to alveolar ன after vowels, except when followed by த், per Tamil orthographic convention."""
    na = Tamil.ConsonantMap[19]
    nna = Tamil.SouthConsonantMap[3]
    vir = Tamil.ViramaMap[0]
    ta = Tamil.ConsonantMap[15]

    ListV = '|'.join(GM.CrunchSymbols(GM.Vowels+GM.VowelSigns+GM.Consonants,'Tamil')+[Tamil.SignMap[0].replace('(','\(').replace(')','\)')])

    Strng = re.sub('('+ListV+')'+ GM.VedicSvaras + '('+na+')' + '(?!' + vir + ta + ')',r'\1\2'+nna,Strng)
    Strng = re.sub('('+ListV+')'+ GM.VedicSvaras + '('+na+')' + '(?!' + vir + ta + ')',r'\1\2'+nna,Strng)

    Strng = re.sub('(²|³|⁴)'+ GM.VedicSvaras + '('+na+')' + '(?!' + vir + ta + ')',r'\1\2'+nna,Strng)
    Strng = re.sub('(²|³|⁴)'+ GM.VedicSvaras + '('+na+')' + '(?!' + vir + ta + ')',r'\1\2'+nna,Strng)

    #Strng = re.sub('(²|³|⁴)'+'('+na+')',r'\1'+nna,Strng)

    #Strng = re.sub('(\s)(ன)', r'\1' + 'ந', Strng)
    #Strng = re.sub('(\.)(ன)', r'\1' + 'ந', Strng)
    #Strng = re.sub('^ன', 'ந', Strng)

    Strng = re.sub("(?<=ஶ்ரீ)(ன)(?!" + vir + ")", "ந", Strng)

    return Strng

def TamilpredictDentaNa(Strng):
    """Restores dental na (ந) in place of ன for a hardcoded list of Sanskrit-derived words that conventionally take dental na."""
    listDentalNa = '''னக²
னக³ர
னகுல
னக்³ன
னக்ஷத்ர
னடராஜ
னடீ
னதீ³
னந்த³ன
னபும்ʼஸக
னப⁴**
னம**
னமஶ்
னமஸ்
னமாம
னமாமி
னமாமோ
னமுசி
னமோ
னமோநம
னமோநமோ
னமோஸ்து
னமோஸ்துதே
னம꞉
னயன
னர**
னரக
னர்தக
னர்தன
னர்மத³
னல**
னலின
னவ**
னவீன
னவ்ய
னஶ்**
னஷ்ட
னாராயண
னாக³
னாடக
னாடீ³
னாட்ய
னாட்³ய
னாத²
னாத³
னாரத
னானா***
னான்ய**
னான்ருʼத
னாப⁴
னாம
னாயக
னாயிகா
னாரத³
னாரஸிம்ʼஹ
னாரி
னாரீ
னாவ***
னாஶ
னாஸிக
னிக³ம
னிகட
னிகர
னிகாம
னிகாய
னிகி²ல
னிகுஞ்ஜ
னிகூ⁴ன
னிகேத
னிக்³ரஹ
னிக்³ருʼஹ
னிக்ருʼந்த
னிக்³ரந்த
னிக்ஷிப
னிக்ஷேப
னிக்⁴ன
னிஜ
னித³ர்ஶ
னிதம்ப³
னிதர
னிதா³க⁴
னிதா³ன
னிதாந்த
னிதா⁴ன
னிதா⁴ய
னித⁴
னிதே⁴ஹி
னித்³ர
னித்ய
னிந்தா³
னிப³த்³த⁴
னிப³த்⁴
னிப³ந்த⁴ன
னிபட
னிபதித
னிபத்ய
னிபபாத
னிபாதித
னிபாத்ய
னிபுண
னிபோ³த⁴
னிப்⁴ருʼத
னிமக்³ன
னிமித்த
னிமிஷ
னியத
னியந்த
னியந்த்ர
னியம
னியுக்த
னியுஜ்ய
னியோ
னிர
னிர்
னிலய
னிவர்
னிவஸ
னிவார
னிவாஸ
னிவிஷ்ட
னிவேத³
னிவேஶ
னிவ்ருʼ
னிஶ
னிஶ்
னிஷ
னிஷ்
னிஸ
னிஸ்
னிஹித
னி꞉ஶ
னி꞉ஷ
னி꞉ஸ
னீச
னீதி
னீர
னீல
னூதன
னூபுர
னேத்ர
னேய**
னைமித்த
னைமிஷ
னைராஶ்ய
னைர்ருʼத
னைவேத்³ய
னைஷ்
ன்யாய
ன்யாஸ
ன்யூன
ன்ருʼ'''.split('\n')

    vir = Tamil.ViramaMap[0]

    Tamillist = '²³⁴ஃஅஆஇஈஉஊஎஏஐஒஓஔகஙசஜஞடணதநனபமயரறலளழவஷஸஹாிீுூெேைொோௌ்ௗ'

    for wordNna in listDentalNa:
        wordNa = re.sub('^ன', 'ந', wordNna)
        if '²' in wordNna[-1] or '³' in wordNna[-1] or '⁴' in wordNna[-1]:
            number = wordNna[-1]

            wordNnaN = wordNna[:-1]
            wordNaN = wordNa[:-1]
            for vow in GM.CrunchSymbols(GM.VowelSigns, 'Tamil'):
                Strng = Strng.replace(wordNnaN + vow + number, wordNaN + vow + number)

        Strng = Strng.replace(wordNna, wordNa)

        for wordNna in ['னாம','னர']:
            wordNa = re.sub('^ன', 'ந', wordNna)
            Strng = re.sub('([' + Tamillist +'])('+wordNa + vir +')', r'\1' + wordNna + vir, Strng)

        Strng = Strng.replace('ன்ந', 'ந்ந')

        Strng = Strng.replace('னாம்ன', 'நாம்ன')

    return Strng

def ContextualLLa(Strng):
    """Contextually converts ல to retroflex ள after specific consonant clusters and in a list of known words, e.g. ப்ரலய → ப்ரளய."""
    ListVS = '|'.join(GM.CrunchSymbols(GM.VowelSigns, 'Tamil'))
    ListC = '|'.join(GM.CrunchSymbols(GM.Consonants, 'Tamil'))

    Strng = re.sub('(ஆவ|ாவ)'+ 'ல', r'\1' +  'ள', Strng)
    Strng = re.sub('(்ரவா|்ரவ|ர|பவ|வி|ரா|ஷ்க|த⁴வ)'+ 'ல', r'\1' +  'ள', Strng)
    Strng = re.sub('(யா|யாம|கோம)'+ 'ல', r'\1' +  'ள', Strng)
    Strng = re.sub('(மௌ)'+ 'ல', r'\1' +  'ள', Strng)
    Strng = re.sub('([\s^])(ந)'+ 'ல', r'\1' +  'ள', Strng)
    Strng = Strng.replace('கலத்ர', 'களத்ர')
    Strng = Strng.replace('ஶீதல', 'ஶீதள')
    Strng = Strng.replace('ஸுதல', 'ஸுதள')
    Strng = Strng.replace('காலி', 'காளி')
    Strng = Strng.replace('காலீ', 'காளீ')
    Strng = Strng.replace('கலேவர', 'களேவர')
    Strng = Strng.replace('கலேவர', 'களேவர')
    Strng = Strng.replace('ப³ஹுல', 'ப³ஹுள')
    Strng = Strng.replace('கஶ்மல', 'கஶ்மள')

    Strng = re.sub('([கத])' + '(' + ListVS + ')?' + '([³⁴])'+ 'ல', r'\1\2\3' +  'ள', Strng)
    Strng = re.sub('(ஜு)'+ 'ல', r'\1' +  'ள', Strng)
    Strng = re.sub('(து)'+ 'லசி', r'\1' +  'ளசி', Strng)
    Strng = re.sub('(ரிம)'+ 'ல', r'\1' +  'ள', Strng)

    Strng = Strng.replace('ள்ய', 'ல்ய')

    return Strng

def FinalNNa(Strng):
    """Restricts alveolar ன to word-final position, converting it to dental ந elsewhere, e.g. ஆனனன் → ஆநநன்."""
    Strng = re.sub('ன', 'ந', Strng)

    Strng = re.sub('ந்' + '([\.।॥,!-])', 'ன்' + r'\1', Strng)
    Strng = re.sub('ந்' + '(\s)', 'ன்' + r'\1', Strng)
    Strng = re.sub('ந்$', 'ன்', Strng)

    return Strng

def TamilAddFirstVarga(Strng):
    """Marks unvoiced first-varga consonants with a superscript ¹ to distinguish them from voiced/aspirated variants, e.g. தீ³பம் → தீ³ப¹ம்."""
    CM = GM.CrunchList('ConsonantMap','Tamil')
    ConUnVoiced = '|'.join([CM[x] for x in [0,5,10,15,20]])
    SuperSubScript = '|'.join(['\u00B2', '\u00B3','\u2074', '₂', '₃', '₄'])

    Strng = re.sub('('+ConUnVoiced+')'+'(?!'+SuperSubScript+')',r'\1'+'\u00B9',Strng)

    from .. import ConvertFix as CF
    Strng = CF.ShiftDiacritics(Strng,'Tamil')
    #remove spurios one
    Strng = re.sub('\u00B9'+'(?='+SuperSubScript+')', '', Strng)

    return Strng

def TamilDisableSHA(Strng):
    """Disables the Tamil letter ஶ, replacing it with ஷ² except within ஶ்ரீ, e.g. ஶ → ஷ²."""
    Strng = Strng.replace('ஶ', 'ஷ²')
    from .. import ConvertFix as CF
    Strng = CF.ShiftDiacritics(Strng,'Tamil')

    Strng = Strng.replace( 'ஷ்²ரீ', 'ஶ்ரீ')

    return Strng

def TamilGranthaVisarga(Strng):
    """Replaces the Tamil pluta-visarga symbol (꞉) with the Grantha visarga character, e.g. நம꞉ → நம𑌃."""
    Strng = Strng.replace('꞉', '𑌃')

    return Strng

def TamilOmDisable(Strng):
    """Disables the Tamil Om symbol, expanding it to ஓம், e.g. ௐ → ஓம்."""
    return Strng.replace("ௐ", "ஓம்")

def TamilRemoveApostrophe(Strng):
    """Removes apostrophe diacritics used for aytham/visarga notation, e.g. ருʼம்ʼ → ரும்."""
    Strng = Strng.replace('ʼ', '').replace('ˮ', '')

    return Strng

def TamilRemoveNumbers(Strng):
    """Strips diacritic superscript/subscript numerals used to mark Grantha consonants, e.g. க²க³க⁴ → ககக."""
    numerals = ['²', '³', '⁴', '₂', '₃', '₄', '¹', '₁']

    for num in numerals:
        Strng = Strng.replace(num, '')

    return Strng

def TamilSubScript(Strng):

    """Converts superscript diacritic numerals to subscript form, e.g. க²க³க⁴ → க₂க₃க₄."""
    SuperScript = ['\u00B9', '\u00B2', '\u00B3','\u2074']
    SubScript = ['\u2081','\u2082','\u2083','\u2084']

    for x,y in zip(SuperScript,SubScript):
        Strng = Strng.replace(x,y)

    return Strng

def oldtamilortho(Strng):
    """Selects old Tamil orthography style (currently a no-op placeholder)."""
    return Strng

