# -1 means don't use internal mapping - just use there replacement character
# nuk means use nukta with replacement character
# [1, "x"] combine the index 1 of the list with x

## OthersRev will always two values:
 # base characters + 'an addition'
## OtherNonREv
 # Singlechar - \u02BC will be added automatically to make it not reversible

## if first is nukta
 # Nukta will be added

VowelMap = {
'halfu': {
    'Malayalam': 'ഉ\u0D4D',
    'Devanagari': 'ॶ',
    'Sharada': '𑆃𑇋𑆶',
    'Tamil': 'உ\u0BCD',
    'IAST': 'ŭ',
    'ISO': 'ŭ',
    'IPA': 'ʉ',
    'OthersRev': [4, 'ʼ'],
    'OthersNonRev': [4, '\u02C2']
    },
'halfuu': {
    'Malayalam': 'ഊ\u0D4D',
    'Devanagari': 'ॷ',
    'Sharada': '𑆃𑇋𑆷',
    'Tamil': 'ஊ\u0BCD',
    'IAST': 'ŭ\u0304',
    'ISO': 'ŭ\u0304',
    'IPA': 'ʉː',
    'OthersRev': [5, 'ʼ'],
    'OthersNonRev': [5, '\u02C2']
    },
'oe': {
    'Devanagari': 'ॳ',
    'Sharada': '𑆃𑇋',
    'IAST': 'ö',
    'ISO': 'ö',
    'IPA': 'ʉː',
    'OthersRev': [1, 'ʼʼ'],
    'OthersNonRev': [1, '\u02C2']
    },
'oee': {
    'Devanagari': 'ॴ',
    'Sharada': '𑆃𑇋𑆳',
    'IAST': 'ȫ',
    'ISO': 'ȫ',
    'IPA': 'ʉː',
    'OthersRev': [1, 'ʼʼʼ'],
    'OthersNonRev': [1, '\u02C2']
    }
}

VowelSignMap = {
'halfu': {
    'Malayalam': '\u0D41\u0D4D',
    'Devanagari': '\u0956',
    'Sharada': '\U000111CB\U000111B6',
    'Tamil': '\u0BC1\u0BCD',
    'IAST': 'ŭ',
    'ISO': 'ŭ',
    'IPA': 'ʉː',
    'OthersRev': [3, 'ʼ'],
    'OthersNonRev': [3, '\u02C2']
    },
'halfuu': {
    'Malayalam': '\u0D42\u0D4D',
    'Devanagari': '\u0957',
    'Sharada': '\U000111CB\U000111B7',
    'Tamil': '\u0BC2\u0BCD',
    'IAST': 'ŭ\u0304',
    'ISO': 'ŭ\u0304',
    'IPA': 'ʉ',
    'OthersRev': [4, 'ʼ'],
    'OthersNonRev': [4, '\u02C2']
    },
'oe': {
    'Devanagari': '\u093A',
    'Sharada': '\U000111CB',
    'IAST': 'ö',
    'ISO': 'ö',
    'IPA': 'ʉː',
    'OthersRev': [0, 'ʼʼ'],
    'OthersNonRev': [0, '\u02C2']
    },
'oee': {
    'Devanagari': '\u093B',
    'Sharada': '\U000111CB\U000111B3',
    'IAST': 'ȫ',
    'ISO': 'ȫ',
    'IPA': 'ʉː',
    'OthersRev': [0, 'ʼʼʼ'],
    'OthersNonRev': [0, '\u02C2']
    },
'ShanLoCesup': {
        'ShanLoC': 'ဵ',
        'ShanLoCRomanLoC': 'e',
        'OthersRev': [9, '\u02C2'],
        'OthersNonRev': [9, '\u02C2'],
    },
'ShanLoCui': {
       'ShanLoC': 'ို',
       'ShanLoCRomanLoC': 'ui',
       'OthersRev': [5, '\u02C2'],
       'OthersNonRev': [5, '\u02C2'],
    },
'ShanLoCuui': {
       'ShanLoC': 'ိူ',
       'ShanLoCRomanLoC': 'ūi',
       'OthersRev': [6, '\u02C2'],
       'OthersNonRev': [6, '\u02C2'],
    },
'ShanLoCaai': {
       'ShanLoC': 'ၢႆ',
       'ShanLoCRomanLoC': 'āi',
       'OthersRev': [10, '\u02C2'],
       'OthersNonRev': [10, '\u02C2'],
    },
'ShanLoCaoi': {
       'ShanLoC': 'ွႆ',
       'ShanLoCRomanLoC': 'oi',
       'OthersRev': [10, '\u02C2'],
       'OthersNonRev': [10, '\u02C2'],
    },
'ShanLoCoalt1': {
       'ShanLoC': 'ေႃ်',
       'ShanLoCRomanLoC': 'ò',
       'OthersRev': [11, '\u02C2'],
       'OthersNonRev': [11, '\u02C2'],
    },
 'ShanLoCoalt': {
     'ShanLoC': 'ူဝ်',
     'ShanLoCRomanLoC': 'ō',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
    },
 'ShanLoCaialt': {
     'ShanLoC': 'ႂ်',
     'ShanLoCRomanLoC': 'ài',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
    }
}

ModernVowelSignMap = {
'ShanLoCeaeup': {
        'ShanLoC': 'ႅ',
        'ShanLoCRomanLoC': 'è',
        'OthersRev': [0, '\u02C2'],
        'OthersNonRev': [0, '\u02C2'],
    },
'ShanLoCeae2': {
        'ShanLoC': 'ေေ',
        'ShanLoCRomanLoC': 'è',
        'OthersRev': [0, '\u02C2'],
        'OthersNonRev': [0, '\u02C2'],
    },
}

ModernVowelMap = {
}

ConsonantMap = {
'theta': {
        'ShanLoC': 'ႀ',
        'ShanLoCRomanLoC': 'x',
        'OthersRev': [15, 'nukta'],
        'OthersNonRev': [15, 'nukta'],
    }
}

SignMap = {
}

AyogavahaMap = {
'Jihvamuliya': {
    'IAST': 'ẖ',
    'ISO': 'ẖ',
    'IASTPali': 'ẖ',
    'Titus': 'ẖ',
    'HK': 'X',
    'Itrans': 'X',
    'Devanagari': '\u1CF5',
    'Bengali': '\u1CF5',
    'Assamese': '\u1CF5',
    'Kannada': '\u0CF1',
    'Tibetan': '\u0F88',
    'Brahmi': '\U00011003',
    'Sharada': '\U000111C2',
    'Newa': '\U00011460',
    'Soyombo': '\U00011A84',
    'OthersRev': [2, '\u02C2'],
    'OthersNonRev': [2, '\u02C2']
    },
'Upadhmaniya': {
    'IAST': 'ḫ',
    'ISO': 'ḫ',
    'IASTPali': 'ḫ',
    'Titus': 'ḫ',
    'HK': 'F',
    'Itrans': 'F',
    'Devanagari': '\u1CF6',
    'Bengali': '\u1CF6',
    'Assamese': '\u1CF6',
    'Kannada': '\u0CF2',
    'Tibetan': '\u0F89',
    'Brahmi': '\U00011004',
    'Sharada': '\U000111C3',
    'Newa': '\U00011461',
    'Soyombo': '\U00011A85',
    'OthersRev': [2, '\u02C2'],
    'OthersNonRev': [2, '\u02C2']
    }
}