# A base index of None means don't use internal mapping - just use the
# replacement character. NUKTA as a suffix (in position 1, never as the base
# index) means combine the base character with that script's own nukta sign
# instead of a literal suffix string.
#
## OthersRev/OthersNonRev/Others: [base, suffix] - synthesizes a fallback
## character for any script with no explicit mapping of its own, by
## combining the character already at position `base` in THAT SCRIPT's own
## canonical letter order with `suffix`. `base` is named using HK's own
## spelling for that letter (e.g. 'u', 'k', 'kh') rather than a raw index -
## see VOWEL_NAMES/VOWEL_SIGN_NAMES/CONSONANT_NAMES/AYOGAVAHA_NAMES in
## GeneralMap.py, which HK.py's own base lists are the source of truth for.
## `Others` gives ONE spec used for both reversible and non-reversible
## scripts - use this by default. Only fall back to writing OthersRev and
## OthersNonRev separately when the two genuinely need different suffixes
## (rare - e.g. a strictly-reversible script needing an apostrophe-based
## marker where a non-reversible one can just take the generic placeholder).
#
## Example - adding a new fallback vowel:
##   'myvowel': {
##       'independent': {
##           'Devanagari': '\u1234',       # scripts with a real glyph get one
##           'Others': ['u', 'x'],        # everyone else: base script's own
##       },                                # "u" vowel + suffix "x"
##       'dependent': {
##           'Devanagari': '\u1235',
##           'Others': ['u', 'x'],        # note: dependent form's own name
##       },                                # table is offset from independent's
##   },
#
## When several scripts share one glyph, key the entry with a tuple of their
## names instead of repeating the same value once per script. ThamFamily/
## ShanPair/IsoIast below are the three combinations that recur often enough
## to be worth naming; an ad hoc tuple works fine for anything else that
## happens to apply to more than one script.

ThamFamily = ('ThamLoC', 'LaoTham', 'LueTham', 'TaiTham', 'KhuenTham')
ShanPair = ('ShanLoC', 'Shan')
IsoIast = ('IAST', 'ISO')
NUKTA = object()  # sentinel for the suffix position; see comment above

# VowelPairs holds each vowel's independent form (used when the vowel
# starts a syllable) paired with its dependent/sign form (used after a
# consonant), keyed by one shared id. The two forms MUST stay keyed and
# ordered identically to each other - Latin->Indic conversion builds the
# internal 'Inter' pivot representation of a vowel using only the
# independent-form mapping, then disambiguates syllable-medial occurrences
# by matching a DepV marker against the dependent form's placeholder for
# that SAME vowel (see GeneralMap.InterAdd and Convert._convert_latin_to_indic).
# Authoring both forms under one key makes that pairing structural instead
# of a convention two separately-authored dicts have to maintain by hand -
# VowelMap/VowelSignMap below are derived from this, not hand-authored.
VowelPairs = {
    'halfu': {
        'independent': {
            'Malayalam': 'ഉ്',
            'Devanagari': 'ॶ',
            'Sharada': '𑆃𑇋𑆶',
            'Tamil': 'உ்',
            IsoIast: 'ŭ',
            'IPA': 'ʉ',
            'OthersRev': ['u', 'ʼ'],
            'OthersNonRev': ['u', '˂'],
        },
        'dependent': {
            'Malayalam': 'ു്',
            'Devanagari': 'ॖ',
            'Sharada': '𑇋𑆶',
            'Tamil': 'ு்',
            IsoIast: 'ŭ',
            'IPA': 'ʉː',
            'OthersRev': ['u', 'ʼ'],
            'OthersNonRev': ['u', '˂'],
        },
    },
    'halfuu': {
        'independent': {
            'Malayalam': 'ഊ്',
            'Devanagari': 'ॷ',
            'Sharada': '𑆃𑇋𑆷',
            'Tamil': 'ஊ்',
            IsoIast: 'ŭ̄',
            'IPA': 'ʉː',
            'OthersRev': ['U', 'ʼ'],
            'OthersNonRev': ['U', '˂'],
        },
        'dependent': {
            'Malayalam': 'ൂ്',
            'Devanagari': 'ॗ',
            'Sharada': '𑇋𑆷',
            'Tamil': 'ூ்',
            IsoIast: 'ŭ̄',
            'IPA': 'ʉ',
            'OthersRev': ['U', 'ʼ'],
            'OthersNonRev': ['U', '˂'],
        },
    },
    'oe': {
        'independent': {
            'Devanagari': 'ॳ',
            'Sharada': '𑆃𑇋',
            IsoIast: 'ö',
            'IPA': 'ʉː',
            'OthersRev': ['A', 'ʼʼ'],
            'OthersNonRev': ['A', '˂'],
        },
        'dependent': {
            'Devanagari': 'ऺ',
            'Sharada': '𑇋',
            IsoIast: 'ö',
            'IPA': 'ʉː',
            'OthersRev': ['A', 'ʼʼ'],
            'OthersNonRev': ['A', '˂'],
        },
    },
    'oee': {
        'independent': {
            'Devanagari': 'ॴ',
            'Sharada': '𑆃𑇋𑆳',
            IsoIast: 'ȫ',
            'IPA': 'ʉː',
            'OthersRev': ['A', 'ʼʼʼ'],
            'OthersNonRev': ['A', '˂'],
        },
        'dependent': {
            'Devanagari': 'ऻ',
            'Sharada': '𑇋𑆳',
            IsoIast: 'ȫ',
            'IPA': 'ʉː',
            'OthersRev': ['A', 'ʼʼʼ'],
            'OthersNonRev': ['A', '˂'],
        },
    },
    'ShanLoCesup': {
        'independent': {
            ShanPair: 'ဢဵ',
            'ShanLoCRomanLoC': 'eʽ',
            'Others': ['e', '˂'],
        },
        'dependent': {
            ShanPair: 'ဵ',
            'ShanLoCRomanLoC': 'eʽ',
            'Others': ['e', '˂'],
        },
    },
    'ShanLoCui': {
        'independent': {
            ShanPair: 'ဢို',
            'ShanLoCRomanLoC': 'ui',
            'Others': ['u', '˂'],
        },
        'dependent': {
            ShanPair: 'ို',
            'ShanLoCRomanLoC': 'ui',
            'Others': ['u', '˂'],
        },
    },
    'ShanLoCuui': {
        'independent': {
            ShanPair: 'ဢိူ',
            'ShanLoCRomanLoC': 'ūi',
            'Others': ['U', '˂'],
        },
        'dependent': {
            ShanPair: 'ိူ',
            'ShanLoCRomanLoC': 'ūi',
            'Others': ['U', '˂'],
        },
    },
    'ShanLoCuuiv': {
        'independent': {
            ShanPair: 'ဢိူဝ်',
            'ShanLoCRomanLoC': 'ūiv',
            'Others': ['U', '˂'],
        },
        'dependent': {
            ShanPair: 'ိူဝ်',
            'ShanLoCRomanLoC': 'ūiv',
            'Others': ['U', '˂'],
        },
    },
    'ShanLoCaai': {
        'independent': {
            ShanPair: 'ဢၢႆ',
            'ShanLoCRomanLoC': 'āi',
            'Others': ['ai', '˂'],
        },
        'dependent': {
            ShanPair: 'ၢႆ',
            'ShanLoCRomanLoC': 'āi',
            'Others': ['ai', '˂'],
        },
    },
    'ShanLoCaoi': {
        'independent': {
            ShanPair: 'ဢွႆ',
            'ThamLoC': 'ᩋ᩿ᩅᩭ',
            ('ShanLoCRomanLoC', 'ThamLoCRomanLoC'): 'oi',
            'Others': ['ai', '˂'],
        },
        'dependent': {
            ShanPair: 'ွႆ',
            'ThamLoC': '᩿ᩅᩭ',
            ('ShanLoCRomanLoC', 'ThamLoCRomanLoC'): 'oi',
            'Others': ['ai', '˂'],
        },
    },
    'ShanLoCoalt1': {
        'independent': {
            ShanPair: 'ဢေႃ်',
            'ShanLoCRomanLoC': 'ò',
            'Others': ['o', '˂'],
        },
        'dependent': {
            ShanPair: 'ေႃ်',
            'ShanLoCRomanLoC': 'ò',
            'Others': ['o', '˂'],
        },
    },
    'ShanLoCoalt': {
        'independent': {
            ShanPair: 'ဢူဝ်',
            'ShanLoCRomanLoC': 'ō',
            'Others': ['o', '˂'],
        },
        'dependent': {
            ShanPair: 'ူဝ်',
            'ShanLoCRomanLoC': 'ō',
            'Others': ['o', '˂'],
        },
    },
    'ShanLoCaialt': {
        'independent': {
            ShanPair: 'ဢͮ',
            'ShanLoCRomanLoC': 'ái',
            'Others': ['ai', '˂'],
        },
        'dependent': {
            ShanPair: 'ͮ',
            'ShanLoCRomanLoC': 'ái',
            'Others': ['ai', '˂'],
        },
    },
    'Khmery2': {
        'independent': {
            'KhmerLoC': 'ឪ',
            'KhmerLoCRomanLoC': 'ýu',
            'Others': ['u', '˂'],
        },
        'dependent': {
            'KhmerLoC': '្ឪ',
            'KhmerLoCRomanLoC': 'ýu',
            'Others': ['U', '˂'],
        },
    },
    'Khmery': {
        'independent': {
            'KhmerLoC': 'អិំʲ',
            'KhmerLoCRomanLoC': 'ẏ',
            'Others': ['i', '˂'],
        },
        'dependent': {
            'KhmerLoC': 'ិំʽ',
            'KhmerLoCRomanLoC': 'ẏ',
            'Others': ['i', '˂'],
        },
    },
    'Khmeryy': {
        'independent': {
            'KhmerLoC': 'អឺʲ',
            'KhmerLoCRomanLoC': 'ȳ',
            'Others': ['I', '˂'],
        },
        'dependent': {
            'KhmerLoC': 'ឺ',
            'KhmerLoCRomanLoC': 'ȳ',
            'Others': ['I', '˂'],
        },
    },
    'Khmerua': {
        'independent': {
            'KhmerLoC': 'អួʲ',
            'KhmerLoCRomanLoC': 'ua',
            'Others': ['u', '˂'],
        },
        'dependent': {
            'KhmerLoC': 'ួ',
            'KhmerLoCRomanLoC': 'ua',
            'Others': ['u', '˂'],
        },
    },
    'Khmeroe': {
        'independent': {
            'KhmerLoC': 'អើʲ',
            'KhmerLoCRomanLoC': 'oe',
            'Others': ['o', '˂'],
        },
        'dependent': {
            'KhmerLoC': 'ើ',
            'KhmerLoCRomanLoC': 'oe',
            'Others': ['o', '˂'],
        },
    },
    'Khmeryye': {
        'independent': {
            'KhmerLoC': 'អឿʲ',
            'KhmerLoCRomanLoC': 'ẏa',
            'Others': ['a', '˂'],
        },
        'dependent': {
            'KhmerLoC': 'ឿ',
            'KhmerLoCRomanLoC': 'ẏa',
            'Others': [None, '˂'],
        },
    },
    'Khmeria': {
        'independent': {
            'KhmerLoC': 'អៀʲ',
            'KhmerLoCRomanLoC': 'ia',
            'Others': ['a', '˂'],
        },
        'dependent': {
            'KhmerLoC': 'ៀ',
            'KhmerLoCRomanLoC': 'ia',
            'Others': [None, '˂'],
        },
    },
    'Khmershortaa': {
        'independent': {
            'KhmerLoC': 'អា់ʲ',
            'KhmerLoCRomanLoC': 'â',
            'Others': ['A', '˂'],
        },
        'dependent': {
            'KhmerLoC': 'ា់',
            'KhmerLoCRomanLoC': 'â',
            'Others': ['A', '˂'],
        },
    },
    'Thamcloseda': {
        'independent': {
            ThamFamily: 'ᩋᩢ',
            'ThamLoCRomanLoC': 'aʽ',
            'Others': ['a', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩢ',
            'ThamLoCRomanLoC': 'aʽ',
            'Others': [None, '˂'],
        },
    },
    'Thamclosede': {
        'independent': {
            ThamFamily: 'ᩋ᩿ᨿ',
            'ThamLoCRomanLoC': 'è',
            'Others': ['a', '˂'],
        },
        'dependent': {
            ThamFamily: '᩿ᨿ',
            'ThamLoCRomanLoC': 'è',
            'Others': ['e', '˂'],
        },
    },
    'Thamclosedau': {
        'independent': {
            ThamFamily: 'ᩋ᩿ᩅ',
            'ThamLoCRomanLoC': 'òʽ',
            'Others': ['au', '˂'],
        },
        'dependent': {
            ThamFamily: '᩿ᩅ',
            'ThamLoCRomanLoC': 'òʽ',
            'Others': [13, '˂'],
        },
    },
    'Thamopeno2h': {
        'independent': {
            ThamFamily: 'ᩋᩰᩬᩡ',
            'ThamLoCRomanLoC': 'ǫḥ',
            'Others': ['o', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩰᩬᩡ',
            'ThamLoCRomanLoC': 'ǫḥ',
            'Others': ['o', '˂'],
        },
    },
    'Thamclosedo2h': {
        'independent': {
            ThamFamily: 'ᩋᩫ',
            'ThamLoCRomanLoC': 'ǫḥʽ',
            'Others': ['o', '˂'],
        },
        'dependent': {
            'ThamLoC': 'ᩫ',
            ('TaiTham', 'LaoTham', 'KhuenTham', 'LueTham'): 'ᩳ',
            'ThamLoCRomanLoC': 'ǫḥʽ',
            'Others': ['o', '˂'],
        },
    },
    'Thamohook': {
        'independent': {
            ThamFamily: 'ᩋᩳ',
            'ThamLoCRomanLoC': 'ǫ',
            'Others': ['o', '˂'],
        },
        'dependent': {
            'ThamLoC': 'ᩳ',
            'ThamLoCRomanLoC': 'ǫ',
            'Others': ['o', '˂'],
        },
    },
    'Thamohookclosed': {
        'independent': {
            ThamFamily: 'ᩋᩬ',
            'ThamLoCRomanLoC': 'ǫʽ',
            'Others': ['I', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩬ',
            'ThamLoCRomanLoC': 'ǫʽ',
            'Others': ['o', '˂'],
        },
    },
    'Thamouhookk': {
        'independent': {
            ThamFamily: 'ᩋᩧ',
            'ThamLoCRomanLoC': 'ư',
            'Others': ['u', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩧ',
            'ThamLoCRomanLoC': 'ư',
            'Others': ['u', '˂'],
        },
    },
    'Thamuuhook': {
        'independent': {
            ThamFamily: 'ᩋᩨ',
            'ThamLoCRomanLoC': 'ư̄',
            'Others': ['U', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩨ',
            'ThamLoCRomanLoC': 'ư̄',
            'Others': ['U', '˂'],
        },
    },
    'Thamaiy': {
        'independent': {
            ThamFamily: 'ᩋᩱ᩿ᨿ',
            'ThamLoCRomanLoC': 'aiy᩺',
            'Others': ['ai', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩱ᩿ᨿ',
            'ThamLoCRomanLoC': 'aiy᩺',
            'Others': ['ai', '˂'],
        },
    },
    'Thamohohooki': {
        'independent': {
            ThamFamily: 'ᩋᩭ',
            'ThamLoCRomanLoC': 'ǫi',
            'Others': ['ai', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩭ',
            'ThamLoCRomanLoC': 'ǫi',
            'Others': ['ai', '˂'],
        },
    },
    'Thameo2': {
        'independent': {
            ThamFamily: 'ᩋᩴ᩿ᨿ',
            'ThamLoCRomanLoC': 'eo',
            'Others': ['o', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩴ᩿ᨿ',
            'ThamLoCRomanLoC': 'eo',
            'Others': ['o', '˂'],
        },
    },
    'Thamohao': {
        'independent': {
            ThamFamily: 'ᩋᩮᩢᩣ',
            'ThamLoCRomanLoC': 'ao',
            'Others': ['au', '˂'],
        },
        'dependent': {
            ('ThamLoC', 'Tham'): 'ᩮᩢᩣ',
            'ThamLoCRomanLoC': 'ao',
            'Others': ['au', '˂'],
        },
    },
}

VowelMap = {k: v['independent'] for k, v in VowelPairs.items()}
VowelSignMap = {k: v['dependent'] for k, v in VowelPairs.items()}

# See VowelPairs above - same independent/dependent pairing, for the
# smaller set of "modern" vowel additions.
ModernVowelPairs = {
    'ShanLoCeaeup': {
        'independent': {
            ShanPair: 'ဢႅ',
            'ShanLoCRomanLoC': 'è',
            'Others': ['aE', '˂'],
        },
        'dependent': {
            ShanPair: 'ႅ',
            'ShanLoCRomanLoC': 'èʽ',
            'Others': ['aE', '˂'],
        },
    },
    'ShanLoCeae2': {
        'independent': {
            ShanPair: 'ဢေေ',
            'ShanLoCRomanLoC': 'è',
            'Others': ['aE', '˂'],
        },
        'dependent': {
            ShanPair: 'ေေ',
            'ShanLoCRomanLoC': 'èʽ',
            'Others': ['aE', '˂'],
        },
    },
    'Thamhoe': {
        'independent': {
            ThamFamily: 'ᩋᩮᩨᩬ',
            'ThamLoCRomanLoC': 'œ',
            'Others': ['aO', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩮᩨᩬ',
            'ThamLoCRomanLoC': 'œ',
            'Others': ['aO', '˂'],
        },
    },
    'Thamoeclosed': {
        'independent': {
            ThamFamily: 'ᩋᩮᩨ',
            'ThamLoCRomanLoC': 'œʽ',
            'Others': ['aO', '˂'],
        },
        'dependent': {
            ThamFamily: 'ᩮᩨ',
            'ThamLoCRomanLoC': 'œʽ',
            'Others': ['aO', '˂'],
        },
    },
}

ModernVowelMap = {k: v['independent'] for k, v in ModernVowelPairs.items()}
ModernVowelSignMap = {k: v['dependent'] for k, v in ModernVowelPairs.items()}

ConsonantMap = {
    'khuenba': {
        ThamFamily: 'ᨷ',
        'ThamLoCRomanLoC': 'b̤',
        'Others': ['b', '˂'],
    },
    'khuenkxa': {
        ThamFamily: 'ᨤ',
        'ThamLoCRomanLoC': 'k̤',
        'Others': ['k', '˂'],
    },
    'khuenhfa': {
        ThamFamily: 'ᨺ',
        'ThamLoCRomanLoC': 'f̈',
        'Others': ['ph', '˂'],
    },
    'khuenlfa': {
        ThamFamily: 'ᨼ',
        'ThamLoCRomanLoC': 'f̤',
        'Others': ['ph', '˂'],
    },
    'khuensa': {
        ThamFamily: 'ᨪ',
        'ThamLoCRomanLoC': 's̤',
        'Others': ['s', '˂'],
    },
    'khuenha': {
        ThamFamily: 'ᩌ',
        'ThamLoCRomanLoC': 'h̤',
        'Others': ['h', '˂'],
    },
    'khuenya': {
        ThamFamily: 'ᩀ',
        'ThamLoCRomanLoC': 'ÿ',
        'Others': ['y', '˂'],
    },
    'theta': {
        ShanPair: 'ႀ',
        'ShanLoCRomanLoC': 'x',
        'Others': ['t', NUKTA],
    },
    'khmernga': {
        'KhmerLoC': 'ង៉',
        'KhmerLoCRomanLoC': 'ṅ″',
        'Others': ['G', '˂'],
    },
    'khmernja': {
        'KhmerLoC': 'ញ៉',
        'KhmerLoCRomanLoC': 'ñ″',
        'Others': ['J', '˂'],
    },
    'khmerma': {
        'KhmerLoC': 'ម៉',
        'KhmerLoCRomanLoC': 'm″',
        'Others': ['m', '˂'],
    },
    'khmerpa': {
        'KhmerLoC': 'ប៉',
        'KhmerLoCRomanLoC': 'p″',
        'Others': ['p', '˂'],
    },
    'khmerya': {
        'KhmerLoC': 'យ៉',
        'KhmerLoCRomanLoC': 'y″',
        'Others': ['y', '˂'],
    },
    'khmerra': {
        'KhmerLoC': 'រ៉',
        'KhmerLoCRomanLoC': 'r″',
        'Others': ['r', '˂'],
    },
    'khmerva': {
        'KhmerLoC': 'វ៉',
        'KhmerLoCRomanLoC': 'v″',
        'Others': ['v', '˂'],
    },
    'khmerpa2': {
        'KhmerLoC': 'ប៊',
        'KhmerLoCRomanLoC': 'p′',
        'Others': ['p', '˂'],
    },
    'khmersa': {
        'KhmerLoC': 'ស៊',
        'KhmerLoCRomanLoC': 's′',
        'Others': ['s', '˂'],
    },
    'khmerha': {
        ('Khmer', 'KhmerLoC'): 'ហ៊',
        'KhmerLoCRomanLoC': 'h′',
        'Others': ['h', '˂'],
    },
    'khmeracons': {
        'KhmerLoC': 'អ',
        'KhmerLoCRomanLoC': '‛ʹ',
        'Others': ['k', '˂'],
    },
    'khmeraconsmod': {
        'KhmerLoC': 'អ៊',
        'KhmerLoCRomanLoC': '‛ʹ′',
        'Others': ['k', '˂'],
    },
    'ThamDoubleNJNJ': {
        'ThamLoC': 'ᨬᩚ',
        'ThamLoCRomanLoC': 'ññ',
        'Others': ['J', '˂'],
    },
}

SignMap = {
    'shanexcl': {
        ShanPair: '႟',
        'ShanLoCRomanLoC': 'u*',
        'OthersRev': [None, '!˂˂˂˂˂'],
        'OthersNonRev': [None, '!˂˂˂˂'],
    },
    'shanone': {
        ShanPair: '႞',
        'ShanLoCRomanLoC': 'n*',
        'Others': [None, '!!˂'],
    },
    'Khmerdivider': {
        'KhmerLoC': '៖',
        'KhmerLoCRomanLoC': ':',
        'Others': [None, '!!!˂'],
    },
    'Thamlae': {
        'ThamLoC': 'ᩓ',
        'ThamLoCRomanLoC': 'læ',
        'Others': [None, '!!!˂'],
    },
}

AyogavahaMap = {
    'Jihvamuliya': {
        ('IAST', 'ISO', 'IASTPali', 'Titus'): 'ẖ',
        ('HK', 'Itrans'): 'X',
        ('Devanagari', 'Bengali', 'Assamese'): 'ᳵ',
        'Kannada': 'ೱ',
        'Tibetan': 'ྈ',
        'Brahmi': '𑀃',
        'Sharada': '𑇂',
        'Newa': '𑑠',
        'Soyombo': '𑪄',
        'Others': ['H', '˂'],
    },
    'Upadhmaniya': {
        ('IAST', 'ISO', 'IASTPali', 'Titus'): 'ḫ',
        ('HK', 'Itrans'): 'F',
        ('Devanagari', 'Bengali', 'Assamese'): 'ᳶ',
        'Kannada': 'ೲ',
        'Tibetan': 'ྉ',
        'Brahmi': '𑀄',
        'Sharada': '𑇃',
        'Newa': '𑑡',
        'Soyombo': '𑪅',
        'Others': ['H', '˂'],
    },
    'shantone2': {
        ShanPair: 'ႇ',
        'ShanLoCRomanLoC': '̢',
        'Others': [None, '˂'],
    },
    'shantone3': {
        ShanPair: 'ႈ',
        'ShanLoCRomanLoC': '̐',
        'Others': [None, '˂˂'],
    },
    'shantone5': {
        ShanPair: 'ႉ',
        'ShanLoCRomanLoC': 'ʹ',
        'Others': [None, '˂˂˂'],
    },
    'shantone6': {
        ShanPair: 'ႊ',
        'ShanLoCRomanLoC': '˝',
        'Others': [None, '˂˂˂˂'],
    },
    'KhmerTone3': {
        'KhmerLoC': '៍',
        'KhmerLoCRomanLoC': '˚',
        'Others': [None, '˂˂˂'],
    },
    'KhmerTone4': {
        'KhmerLoC': '៎',
        'KhmerLoCRomanLoC': '’',
        'Others': [None, '˂˂˂'],
    },
    'KhmerTone5': {
        'KhmerLoC': '៏',
        'KhmerLoCRomanLoC': 'ʻ',
        'Others': [None, '˂˂˂'],
    },
    'Khmerbreve': {
        'KhmerLoC': '័',
        'KhmerLoCRomanLoC': '̆',
        'Others': [None, '˂'],
    },
    'Khmervisarga2': {
        'KhmerLoC': 'ៈ',
        'KhmerLoCRomanLoC': '̀',
        'Others': [None, '˂'],
    },
    'Khmershortener': {
        'KhmerLoC': '់',
        'KhmerLoCRomanLoC': '́',
        'Others': [None, '˂'],
    },
    'ThamTone1': {
        ThamFamily: '᩵',
        'ThamLoCRomanLoC': '′',
        'Others': [None, '˂˂˂˂˂'],
    },
    'ThamTone2': {
        ThamFamily: '᩶',
        'ThamLoCRomanLoC': '″',
        'Others': [None, '˂˂˂˂˂'],
    },
    'ThamTone3': {
        ThamFamily: '᩷',
        'ThamLoCRomanLoC': 'ˆ',
        'Others': [None, '˂˂˂˂˂'],
    },
    'ThamTone4': {
        ThamFamily: '᩸',
        'ThamLoCRomanLoC': 'ᴶ',
        'Others': [None, '˂˂˂˂˂'],
    },
    'ThamTone5': {
        ThamFamily: '᩹',
        'ThamLoCRomanLoC': 'ʵ',
        'Others': [None, '˂˂˂˂˂'],
    },
}
