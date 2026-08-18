# -*- coding: utf-8 -*-

## Include AnusvaraToNasal for Santali, TolongSikhi, Limbu, Lepcha

## Generate without Short Vowels - Only include for preserver "Source"

from . import ScriptRegistry as SR
# Aliased: this module's ApplyScriptDefaults already uses the local name
# "Options" for its own resolved-option-name list.
from . import Options as OptionsModule

# Target -> default postoptions applied unconditionally for that target.
# Targets with conditional logic (Bengali: depends on PostOptions; Latn:
# depends on Source) are handled separately in ApplyScriptDefaults, not here.
_TARGET_DEFAULT_OPTIONS = {
    'Telugu': ['NasalToAnusvara', 'MToAnusvara', 'TeluguRemoveNukta', 'TeluguRemoveAeAo'],
    'Kannada': ['NasalToAnusvara', 'MToAnusvara'],
    'Sinhala': ['SinhalaChandrbinduAnusvara'],
    'Khojki': ['KhojkiRRI'],
    'Nandinagari': ['NasalToAnusvara'],
    'Hebrew': ['HebrewVetVav', 'HebrewnonFinalShort'],
    'Malayalam': ['MalayalamAnusvaraNasal', 'MToAnusvara', 'MalayalamremoveHistorical'],
    'Tamil': ['TamilNaToNNa', 'AnusvaraToNasal', 'TamilpredictDentaNa'],
    'MeeteiMayek': ['MeeteiMayekremoveHistorical'],
    'Limbu': ['LimburemoveHistorical'],
    'Assamese': ['YaToYYa', 'AnusvaraToNasal'],
    'Oriya': ['AnusvaraToNasal', 'OriyaVa', 'YaToYYa'],
    'Chakma': ['YaToYYa'],
    'Gurmukhi': ['GurmukhiCandrabindu', 'GurmukhiTippiBindu', 'GurmukhiTippiGemination'],
    'Saurashtra': ['SaurashtraHaru'],
    'Ahom': ['AhomClosed'],
    'Tibetan': ['TibetanRemoveVirama', 'TibetanRemoveBa'],
    'Thaana': ['ThaanaRemoveHistorical'],
    'Avestan': ['AvestanConventions'],
    'Sundanese': ['SundaneseRemoveHistoric'],
    'Multani': ['MultaniAbjad'],
    'Modi': ['ModiRemoveLong'],
    'WarangCiti': ['WarangCitiModernOrthogaphy'],
    'Arab': ['ArabRemoveAdditions'],
}

# Latn's defaults depend on Source, not Target.
## Also make changes in FixSemiticPreProcess
_LATN_SOURCE_DEFAULT_OPTIONS = {
    'Arab': ['arabizeLatn'],
    'Arab-Ur': ['urduizeLatn'],
    'Arab-Pa': ['urduizeLatn'],
    'Arab-Fa': ['urduizeLatn'],
    'Syrn': ['syricizeLatn'],
    'Syrj': ['hebraizeLatn'],
    'Hebr': ['hebraizeLatn'],
}

def ApplyScriptDefaults(Strng,Source,Target, PostOptions=[], ctx=None):
    Options = []

    #print('Target is ' + Target)

    if SR.get(Target).is_indic:
        Options += []#['RemoveDiacritics'] #Sometimes you may wanna keep it. Adjust options

    if Target == 'Bengali':
        if 'BengaliRaBa' in PostOptions:
            Options += ['YaToYYa','AnusvaraToNasal', 'BengaliConjunctVB']
        else:
            Options += ['AnusvaraToNasal', 'VaToBa','YaToYYa', 'BengaliConjunctVB']

    elif Target == 'Latn':
        Options += _LATN_SOURCE_DEFAULT_OPTIONS.get(Source, [])

    else:
        Options += _TARGET_DEFAULT_OPTIONS.get(Target, [])

    for Option in Options:
        if Option.find(Target) != -1:
            Strng = OptionsModule.call_post_option(Option,Strng,ctx=ctx)
        else:
            Strng = OptionsModule.call_post_option(Option,Strng,Target,ctx=ctx)

    return Strng