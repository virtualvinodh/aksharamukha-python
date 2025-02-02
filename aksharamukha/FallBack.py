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
    },
'ShanLoCesup': {
        'ShanLoC': 'ဢဵ',
        'Shan': 'ဢဵ',
        'ShanLoCRomanLoC': 'e\u02BD',
        'OthersRev': [10, '\u02C2'],
        'OthersNonRev': [10, '\u02C2'],
    },
'ShanLoCui': {
       'ShanLoC': 'ဢို',
       'Shan': 'ဢို',
       'ShanLoCRomanLoC': 'ui',
       'OthersRev': [4, '\u02C2'],
       'OthersNonRev': [4, '\u02C2'],
    },
'ShanLoCuui': {
       'ShanLoC': 'ဢိူ',
       'Shan': 'ဢိူ',
       'ShanLoCRomanLoC': 'ūi',
       'OthersRev': [5, '\u02C2'],
       'OthersNonRev': [5, '\u02C2'],
    },
'ShanLoCuuiv': {
       'ShanLoC': 'ဢိူဝ်',
       'Shan': 'ဢိူဝ်',
       'ShanLoCRomanLoC': 'ūiv',
       'OthersRev': [5, '\u02C2'],
       'OthersNonRev': [5, '\u02C2'],
    },
'ShanLoCaai': {
       'ShanLoC': 'ဢၢႆ',
       'Shan': 'ဢၢႆ',
       'ShanLoCRomanLoC': 'āi',
       'OthersRev': [11, '\u02C2'],
       'OthersNonRev': [11, '\u02C2'],
    },
'ShanLoCaoi': {
       'ShanLoC': 'ဢွႆ',
       'Shan': 'ဢွႆ',
       'ThamLoC': 'ᩋ\u1A7Fᩅᩭ',
       'ShanLoCRomanLoC': 'oi',
       'ThamLoCRomanLoC': 'oi',
       'OthersRev': [11, '\u02C2'],
       'OthersNonRev': [11, '\u02C2'],
    },
'ShanLoCoalt1': {
       'ShanLoC': 'ဢေႃ်',
       'Shan': 'ဢေႃ်',
       'ShanLoCRomanLoC': 'ò',
       'OthersRev': [12, '\u02C2'],
       'OthersNonRev': [12, '\u02C2'],
    },
 'ShanLoCoalt': {
     'ShanLoC': 'ဢူဝ်',
     'Shan': 'ဢူဝ်',
     'ShanLoCRomanLoC': 'ō',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
    },
 'ShanLoCaialt': {
     'ShanLoC': 'ဢ\u036E',
     'Shan': 'ဢ\u036E',
     'ShanLoCRomanLoC': 'ái',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
    },
  'Khmery2': {
      'KhmerLoC': 'ឪ',
      'KhmerLoCRomanLoC': 'ýu',
     'OthersRev': [4, '\u02C2'],
     'OthersNonRev': [4, '\u02C2'],
  },
  'Khmery': {
      'KhmerLoC': 'អ\u17B7\u17C6\u02B2',
      'KhmerLoCRomanLoC': 'ẏ',
     'OthersRev': [2, '\u02C2'],
     'OthersNonRev': [2, '\u02C2'],
  },
  'Khmeryy': {
      'KhmerLoC': 'អឺ\u02B2',
      'KhmerLoCRomanLoC': 'ȳ',
      'OthersRev': [3, '\u02C2'],
      'OthersNonRev': [3, '\u02C2'],
  },
  'Khmerua': {
      'KhmerLoC': 'អួ\u02B2',
      'KhmerLoCRomanLoC': 'ua',
      'OthersRev': [4, '\u02C2'],
      'OthersNonRev': [4, '\u02C2'],
  },
  'Khmeroe': {
      'KhmerLoC': 'អើ\u02B2',
      'KhmerLoCRomanLoC': 'oe',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
  },
  'Khmeryye': {
      'KhmerLoC': 'អឿ\u02B2',
      'KhmerLoCRomanLoC': 'ẏa',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
  },
  'Khmeria': {
      'KhmerLoC': 'អៀ\u02B2',
      'KhmerLoCRomanLoC': 'ia',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
  },
  'Khmershortaa': {
      'KhmerLoC': 'អា់\u02B2',
      'KhmerLoCRomanLoC': 'â',
     'OthersRev': [1, '\u02C2'],
     'OthersNonRev': [1, '\u02C2'],
  },
  'Thamcloseda': {
     'ThamLoC': 'ᩋᩢ',
     'TaiTham': 'ᩋᩢ',
     'LaoTham': 'ᩋᩢ',
     'LueTham': 'ᩋᩢ',
     'KhuenTham': 'ᩋᩢ',
     'ThamLoCRomanLoC': 'a\u02BD',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
  },
  'Thamclosede': {
   'ThamLoC': 'ᩋ\u1A7Fᨿ',
   'TaiTham': 'ᩋ\u1A7Fᨿ',
   'LueTham': 'ᩋ\u1A7Fᨿ',
   'KhuenTham': 'ᩋ\u1A7Fᨿ',
   'LaoTham': 'ᩋ\u1A7Fᨿ',
    'ThamLoCRomanLoC': 'è',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
  },
  'Thamclosedau': {
     'ThamLoC': 'ᩋ\u1A7Fᩅ',
     'TaiTham': 'ᩋ\u1A7Fᩅ',
     'LaoTham': 'ᩋ\u1A7Fᩅ',
     'LueTham': 'ᩋ\u1A7Fᩅ',
     'KhuenTham': 'ᩋ\u1A7Fᩅ',
     'ThamLoCRomanLoC': 'ò\u02BD',
     'OthersRev': [13, '\u02C2'],
     'OthersNonRev': [13, '\u02C2'],
  },
  'Thamopeno2h': {
     'ThamLoC': 'ᩋ\u1A70\u1A6C\u1A61',
     'TaiTham': 'ᩋ\u1A70\u1A6C\u1A61',
     'LueTham': 'ᩋ\u1A70\u1A6C\u1A61',
     'KhuenTham': 'ᩋ\u1A70\u1A6C\u1A61',
     'LaoTham': 'ᩋ\u1A70\u1A6C\u1A61',
      'ThamLoCRomanLoC': 'ǫḥ',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
  },
  'Thamclosedo2h': {
     'ThamLoC': 'ᩋᩫ',
     'TaiTham': 'ᩋᩫ',
     'LaoTham': 'ᩋᩫ',
     'LueTham': 'ᩋᩫ',
     'KhuenTham': 'ᩋᩫ',
      'ThamLoCRomanLoC': 'ǫḥ\u02BD',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
  },
  'Thamohook': {
     'ThamLoC': 'ᩋᩳ',
     'LaoTham': 'ᩋᩳ',
     'TaiTham': 'ᩋᩳ',
     'LueTham': 'ᩋᩳ',
     'KhuenTham': 'ᩋᩳ',
     'ThamLoCRomanLoC': 'ǫ',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
  },
  'Thamohookclosed': {
     'ThamLoC': 'ᩋᩬ',
     'LaoTham': 'ᩋᩬ',
     'TaiTham': 'ᩋᩬ',
     'LueTham': 'ᩋᩬ',
     'KhuenTham': 'ᩋᩬ',
     'ThamLoCRomanLoC': 'ǫ\u02BD',
     'OthersRev': [3, '\u02C2'],
     'OthersNonRev': [3, '\u02C2'],
  },
  'Thamouhookk': {
     'ThamLoC': 'ᩋᩧ',
     'TaiTham': 'ᩋᩧ',
     'LaoTham': 'ᩋᩧ',
     'LueTham': 'ᩋᩧ',
     'KhuenTham': 'ᩋᩧ',
     'ThamLoCRomanLoC': 'ư',
     'OthersRev': [4, '\u02C2'],
     'OthersNonRev': [4, '\u02C2'],
  },
  'Thamuuhook': {
     'ThamLoC': 'ᩋᩨ',
     'TaiTham': 'ᩋᩨ',
     'LaoTham': 'ᩋᩨ',
     'LueTham': 'ᩋᩨ',
     'KhuenTham': 'ᩋᩨ',
      'ThamLoCRomanLoC': 'ư̄',
     'OthersRev': [5, '\u02C2'],
     'OthersNonRev': [5, '\u02C2'],
  },
  'Thamaiy': {
     'ThamLoC': 'ᩋᩱ\u1A7Fᨿ',
     'TaiTham': 'ᩋᩱ\u1A7Fᨿ',
     'LueTham': 'ᩋᩱ\u1A7Fᨿ',
     'KhuenTham': 'ᩋᩱ\u1A7Fᨿ',
     'LaoTham': 'ᩋᩱ\u1A7Fᨿ',
      'ThamLoCRomanLoC': 'aiy\u1A7A',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Thamohohooki': {
     'ThamLoC': 'ᩋᩭ',
     'TaiTham': 'ᩋᩭ',
     'LaoTham': 'ᩋᩭ',
     'LueTham': 'ᩋᩭ',
     'KhuenTham': 'ᩋᩭ',
      'ThamLoCRomanLoC': 'ǫi',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Thameo2': {
     'ThamLoC': 'ᩋ\u1A74\u1A7Fᨿ',
     'TaiTham': 'ᩋ\u1A74\u1A7Fᨿ',
     'LaoTham': 'ᩋ\u1A74\u1A7Fᨿ',
     'LueTham': 'ᩋ\u1A74\u1A7Fᨿ',
     'KhuenTham': 'ᩋ\u1A74\u1A7Fᨿ',
      'ThamLoCRomanLoC': 'eo',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
  },
  'Thamohao': {
     'ThamLoC': 'ᩋᩮᩢᩣ',
     'TaiTham': 'ᩋᩮᩢᩣ',
     'LaoTham': 'ᩋᩮᩢᩣ',
     'KhuenTham': 'ᩋᩮᩢᩣ',
     'LueTham': 'ᩋᩮᩢᩣ',
      'ThamLoCRomanLoC': 'ao',
     'OthersRev': [13, '\u02C2'],
     'OthersNonRev': [13, '\u02C2'],
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
        'Shan': 'ဵ',
        'ShanLoCRomanLoC': 'e\u02BD',
        'OthersRev': [9, '\u02C2'],
        'OthersNonRev': [9, '\u02C2'],
    },
'ShanLoCui': {
       'ShanLoC': 'ို',
       'Shan': 'ို',
       'ShanLoCRomanLoC': 'ui',
       'OthersRev': [3, '\u02C2'],
       'OthersNonRev': [3, '\u02C2'],
    },
'ShanLoCuui': {
       'ShanLoC': 'ိူ',
       'Shan': 'ိူ',
       'ShanLoCRomanLoC': 'ūi',
       'OthersRev': [4, '\u02C2'],
       'OthersNonRev': [4, '\u02C2'],
    },
'ShanLoCuuiv': {
       'ShanLoC': 'ိူဝ်',
       'Shan': 'ိူဝ်',
       'ShanLoCRomanLoC': 'ūiv',
       'OthersRev': [4, '\u02C2'],
       'OthersNonRev': [4, '\u02C2'],
    },
'ShanLoCaai': {
       'ShanLoC': 'ၢႆ',
       'Shan': 'ၢႆ',
       'ShanLoCRomanLoC': 'āi',
       'OthersRev': [10, '\u02C2'],
       'OthersNonRev': [10, '\u02C2'],
    },
'ShanLoCaoi': {
       'ShanLoC': 'ွႆ',
       'Shan': 'ွႆ',
       'ThamLoC': '\u1A7Fᩅᩭ',
       'ShanLoCRomanLoC': 'oi',
       'ThamLoCRomanLoC': 'oi',
       'OthersRev': [10, '\u02C2'],
       'OthersNonRev': [10, '\u02C2'],
    },
'ShanLoCoalt1': {
       'ShanLoC': 'ေႃ်',
       'Shan': 'ေႃ်',
       'ShanLoCRomanLoC': 'ò',
       'OthersRev': [11, '\u02C2'],
       'OthersNonRev': [11, '\u02C2'],
    },
 'ShanLoCoalt': {
     'ShanLoC': 'ူဝ်',
     'Shan': 'ူဝ်',
     'ShanLoCRomanLoC': 'ō',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
    },
 'ShanLoCaialt': {
     'ShanLoC': '\u036E',
     'Shan': '\u036E',
     'ShanLoCRomanLoC': 'ái',
     'OthersRev': [10, '\u02C2'],
     'OthersNonRev': [10, '\u02C2'],
    },
  'Khmery2': {
      'KhmerLoC': '្ឪ',
      'KhmerLoCRomanLoC': 'ýu',
     'OthersRev': [4, '\u02C2'],
     'OthersNonRev': [4, '\u02C2'],
  },
  'Khmery': {
      'KhmerLoC': '\u17B7\u17C6\u02BD',
      'KhmerLoCRomanLoC': 'ẏ',
     'OthersRev': [1, '\u02C2'],
     'OthersNonRev': [1, '\u02C2'],
  },
  'Khmeryy': {
      'KhmerLoC': 'ឺ',
      'KhmerLoCRomanLoC': 'ȳ',
      'OthersRev': [2, '\u02C2'],
      'OthersNonRev': [2, '\u02C2'],
  },
  'Khmerua': {
      'KhmerLoC': 'ួ',
      'KhmerLoCRomanLoC': 'ua',
      'OthersRev': [3, '\u02C2'],
      'OthersNonRev': [3, '\u02C2'],
  },
  'Khmeroe': {
      'KhmerLoC': 'ើ',
      'KhmerLoCRomanLoC': 'oe',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Khmeryye': {
      'KhmerLoC': 'ឿ',
      'KhmerLoCRomanLoC': 'ẏa',
     'OthersRev': [-1, '\u02C2'],
     'OthersNonRev': [-1, '\u02C2'],
  },
  'Khmeria': {
      'KhmerLoC': 'ៀ',
      'KhmerLoCRomanLoC': 'ia',
     'OthersRev': [-1, '\u02C2'],
     'OthersNonRev': [-1, '\u02C2'],
  },
  'Khmershortaa': {
      'KhmerLoC': 'ា់',
      'KhmerLoCRomanLoC': 'â',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
  },
  'Thamcloseda': {
      'ThamLoC': 'ᩢ',
      'TaiTham': 'ᩢ',
      'LaoTham': 'ᩢ',
      'KhuenTham': 'ᩢ',
      'LueTham': 'ᩢ',
      'ThamLoCRomanLoC': 'a\u02BD',
     'OthersRev': [-1, '\u02C2'],
     'OthersNonRev': [-1, '\u02C2'],
  },
  'Thamclosede': {
    'ThamLoC': '\u1A7Fᨿ',
    'TaiTham': '\u1A7Fᨿ',
    'LaoTham': '\u1A7Fᨿ',
    'KhuenTham': '\u1A7Fᨿ',
    'LueTham': '\u1A7Fᨿ',
    'ThamLoCRomanLoC': 'è',
     'OthersRev': [9, '\u02C2'],
     'OthersNonRev': [9, '\u02C2'],
  },
  'Thamclosedau': {
      'ThamLoC': '\u1A7Fᩅ',
      'TaiTham': '\u1A7Fᩅ',
      'LaoTham': '\u1A7Fᩅ',
      'LueTham': '\u1A7Fᩅ',
      'KhuenTham': '\u1A7Fᩅ',
      'ThamLoCRomanLoC': 'ò\u02BD',
     'OthersRev': [13, '\u02C2'],
     'OthersNonRev': [13, '\u02C2'],
  },
  'Thamopeno2h': {
      'ThamLoC': '\u1A70\u1A6C\u1A61',
      'TaiTham': '\u1A70\u1A6C\u1A61',
      'LaoTham': '\u1A70\u1A6C\u1A61',
      'LueTham': '\u1A70\u1A6C\u1A61',
      'KhuenTham': '\u1A70\u1A6C\u1A61',
      'ThamLoCRomanLoC': 'ǫḥ',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Thamclosedo2h': {
      'ThamLoC': 'ᩫ',
      'TaiTham': 'ᩳ',
      'LaoTham': 'ᩳ',
      'KhuenTham': 'ᩳ',
      'LueTham': 'ᩳ',

      'ThamLoCRomanLoC': 'ǫḥ\u02BD',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Thamohook': {
      'ThamLoC': 'ᩳ',
      'ThamLoCRomanLoC': 'ǫ',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Thamohookclosed': {
      'ThamLoC': 'ᩬ',
      'TaiTham': 'ᩬ',
      'LaoTham': 'ᩬ',
      'KhuenTham': 'ᩬ',
      'LueTham': 'ᩬ',
      'ThamLoCRomanLoC': 'ǫ\u02BD',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Thamouhookk': {
      'ThamLoC': 'ᩧ',
      'TaiTham': 'ᩧ',
      'LaoTham': 'ᩧ',
      'KhuenTham': 'ᩧ',
      'LueTham': 'ᩧ',
      'ThamLoCRomanLoC': 'ư',
     'OthersRev': [3, '\u02C2'],
     'OthersNonRev': [3, '\u02C2'],
  },
  'Thamuuhook': {
      'ThamLoC': 'ᩨ',
      'TaiTham': 'ᩨ',
      'LaoTham': 'ᩨ',
      'KhuenTham': 'ᩨ',
      'LueTham': 'ᩨ',
      'ThamLoCRomanLoC': 'ư̄',
     'OthersRev': [4, '\u02C2'],
     'OthersNonRev': [4, '\u02C2'],
  },
  'Thamaiy': {
      'ThamLoC': 'ᩱ\u1A7Fᨿ',
      'TaiTham': 'ᩱ\u1A7Fᨿ',
      'LaoTham': 'ᩱ\u1A7Fᨿ',
      'KhuenTham': 'ᩱ\u1A7Fᨿ',
      'LueTham': 'ᩱ\u1A7Fᨿ',
      'ThamLoCRomanLoC': 'aiy\u1A7A',
     'OthersRev': [10, '\u02C2'],
     'OthersNonRev': [10, '\u02C2'],
  },
  'Thamohohooki': {
      'ThamLoC': 'ᩭ',
      'TaiTham': 'ᩭ',
      'LaoTham': 'ᩭ',
      'KhuenTham': 'ᩭ',
      'LueTham': 'ᩭ',
      'ThamLoCRomanLoC': 'ǫi',
     'OthersRev': [10, '\u02C2'],
     'OthersNonRev': [10, '\u02C2'],
  },
  'Thameo2': {
      'ThamLoC': '\u1A74\u1A7Fᨿ',
      'TaiTham': '\u1A74\u1A7Fᨿ',
      'LueTham': '\u1A74\u1A7Fᨿ',
      'KhuenTham': '\u1A74\u1A7Fᨿ',
      'LaoTham': '\u1A74\u1A7Fᨿ',
      'ThamLoCRomanLoC': 'eo',
     'OthersRev': [11, '\u02C2'],
     'OthersNonRev': [11, '\u02C2'],
  },
  'Thamohao': {
      'ThamLoC': 'ᩮᩢᩣ',
      'Tham': 'ᩮᩢᩣ',
      'ThamLoCRomanLoC': 'ao',
     'OthersRev': [12, '\u02C2'],
     'OthersNonRev': [12, '\u02C2'],
  }
}

ModernVowelSignMap = {
'ShanLoCeaeup': {
        'ShanLoC': 'ႅ',
        'Shan': 'ႅ',
        'ShanLoCRomanLoC': 'è\u02BD',
        'OthersRev': [0, '\u02C2'],
        'OthersNonRev': [0, '\u02C2'],
    },
'ShanLoCeae2': {
        'ShanLoC': 'ေေ',
        'Shan': 'ေေ',
        'ShanLoCRomanLoC': 'è\u02BD',
        'OthersRev': [0, '\u02C2'],
        'OthersNonRev': [0, '\u02C2'],
    },
  'Thamhoe': {
      'ThamLoC': 'ᩮᩨᩬ',
      'TaiTham': 'ᩮᩨᩬ',
      'LaoTham': 'ᩮᩨᩬ',
      'KhuenTham': 'ᩮᩨᩬ',
      'LueTham': 'ᩮᩨᩬ',
      'ThamLoCRomanLoC': 'œ',
     'OthersRev': [1, '\u02C2'],
     'OthersNonRev': [1, '\u02C2'],
  },
  'Thamoeclosed': {
      'ThamLoC': 'ᩮᩨ',
      'TaiTham': 'ᩮᩨ',
      'LaoTham': 'ᩮᩨ',
      'KhuenTham': 'ᩮᩨ',
      'LueTham': 'ᩮᩨ',
      'ThamLoCRomanLoC': 'œ\u02BD',
     'OthersRev': [1, '\u02C2'],
     'OthersNonRev': [1, '\u02C2'],
  }
}

ModernVowelMap = {
'ShanLoCeaeup': {
        'ShanLoC': 'ဢႅ',
        'Shan': 'ဢႅ',
        'ShanLoCRomanLoC': 'è',
        'OthersRev': [0, '\u02C2'],
        'OthersNonRev': [0, '\u02C2'],
    },
'ShanLoCeae2': {
        'ShanLoC': 'ဢေေ',
        'Shan': 'ဢေေ',
        'ShanLoCRomanLoC': 'è',
        'OthersRev': [0, '\u02C2'],
        'OthersNonRev': [0, '\u02C2'],
    },
  'Thamhoe': {
     'ThamLoC': 'ᩋᩮᩨᩬ',
     'TaiTham': 'ᩋᩮᩨᩬ',
     'LaoTham': 'ᩋᩮᩨᩬ',
     'LueTham': 'ᩋᩮᩨᩬ',
     'KhuenTham': 'ᩋᩮᩨᩬ',
      'ThamLoCRomanLoC': 'œ',
     'OthersRev': [1, '\u02C2'],
     'OthersNonRev': [1, '\u02C2'],
  },
  'Thamoeclosed': {
     'ThamLoC': 'ᩋᩮᩨ',
     'TaiTham': 'ᩋᩮᩨ',
     'LaoTham': 'ᩋᩮᩨ',
     'LueTham': 'ᩋᩮᩨ',
     'KhuenTham': 'ᩋᩮᩨ',
      'ThamLoCRomanLoC': 'œ\u02BD',
     'OthersRev': [1, '\u02C2'],
     'OthersNonRev': [1, '\u02C2'],
  }
}

ConsonantMap = {
'khuenba': {
    'ThamLoC': 'ᨷ',
    'LaoTham': 'ᨷ',
    'LueTham': 'ᨷ',
    'TaiTham': 'ᨷ',
    'KhuenTham': 'ᨷ',
    'ThamLoCRomanLoC': 'b\u0324',
     'OthersRev': [22, '\u02C2'],
     'OthersNonRev': [22, '\u02C2'],
},
'khuenkxa': {
    'ThamLoC': 'ᨤ',
    'LueTham': 'ᨤ',
    'TaiTham': 'ᨤ',
    'LaoTham': 'ᨤ',
    'KhuenTham': 'ᨤ',
    'ThamLoCRomanLoC': 'k\u0324',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
},
'khuenfa': {
    'ThamLoC': 'ᨺ',
    'TaiTham': 'ᨺ',
    'LueTham': 'ᨺ',
    'TaiTham': 'ᨺ',
    'LaoTham': 'ᨺ',
    'KhuenTham': 'ᨺ',
    'ThamLoCRomanLoC': 'f\u0308',
     'OthersRev': [21, '\u02C2'],
     'OthersNonRev': [21, '\u02C2'],
},
'khuensa': {
    'ThamLoC': 'ᨪ',
    'TaiTham': 'ᨪ',
    'LueTham': 'ᨪ',
    'LaoTham': 'ᨪ',
    'KhuenTham': 'ᨪ',
    'ThamLoCRomanLoC': 's\u0324',
     'OthersRev': [31, '\u02C2'],
     'OthersNonRev': [31, '\u02C2'],
},
'khuenha': {
    'ThamLoC': 'ᩌ',
    'TaiTham': 'ᩌ',
    'LueTham': 'ᩌ',
    'LaoTham': 'ᩌ',
    'KhuenTham': 'ᩌ',
    'ThamLoCRomanLoC': 'h\u0324',
     'OthersRev': [32, '\u02C2'],
     'OthersNonRev': [32, '\u02C2'],
},
'khuenya': {
    'ThamLoC': 'ᩀ',
    'LueTham': 'ᩀ',
    'LaoTham': 'ᩀ',
    'TaiTham': 'ᩀ',
    'KhuenTham': 'ᩀ',
    'ThamLoCRomanLoC': 'y\u0308',
     'OthersRev': [25, '\u02C2'],
     'OthersNonRev': [25, '\u02C2'],
},
'theta': {
        'ShanLoC': 'ႀ',
        'Shan': 'ႀ',
        'ShanLoCRomanLoC': 'x',
        'OthersRev': [15, 'nukta'],
        'OthersNonRev': [15, 'nukta'],
    },
 'khmernga': {
     'KhmerLoC' : 'ង៉',
     'KhmerLoCRomanLoC': 'ṅ″',
     'OthersRev': [4, '\u02C2'],
     'OthersNonRev': [4, '\u02C2'],
 },
 'khmernja': {
     'KhmerLoC' : 'ញ៉',
     'KhmerLoCRomanLoC': 'ñ″',
     'OthersRev': [9, '\u02C2'],
     'OthersNonRev': [9, '\u02C2'],
 },
 'khmerma': {
     'KhmerLoC' : 'ម៉',
     'KhmerLoCRomanLoC': 'm″',
     'OthersRev': [24, '\u02C2'],
     'OthersNonRev': [24, '\u02C2'],
 },
 'khmerpa': {
     'KhmerLoC' : 'ប៉',
     'KhmerLoCRomanLoC': 'p″',
     'OthersRev': [20, '\u02C2'],
     'OthersNonRev': [20, '\u02C2'],
 },
 'khmerya': {
     'KhmerLoC' : 'យ៉',
     'KhmerLoCRomanLoC': 'y″',
     'OthersRev': [25, '\u02C2'],
     'OthersNonRev': [25, '\u02C2'],
 },
 'khmerra': {
     'KhmerLoC' : 'រ៉',
     'KhmerLoCRomanLoC': 'r″',
     'OthersRev': [26, '\u02C2'],
     'OthersNonRev': [26, '\u02C2'],
 },
 'khmerva': {
     'KhmerLoC' : 'វ៉',
     'KhmerLoCRomanLoC': 'v″',
     'OthersRev': [28, '\u02C2'],
     'OthersNonRev': [28, '\u02C2'],
 },
 'khmerpa2': {
     'KhmerLoC' : 'ប៊',
     'KhmerLoCRomanLoC': 'p′',
     'OthersRev': [20, '\u02C2'],
     'OthersNonRev': [20, '\u02C2'],
 },
 'khmersa': {
     'KhmerLoC' : 'ស៊',
     'KhmerLoCRomanLoC': 's′',
     'OthersRev': [31, '\u02C2'],
     'OthersNonRev': [31, '\u02C2'],
 },
 'khmerha': {
     'Khmer' : 'ហ៊',
     'KhmerLoC' : 'ហ៊',
     'KhmerLoCRomanLoC': 'h′',
     'OthersRev': [32, '\u02C2'],
     'OthersNonRev': [32, '\u02C2'],
 },
 'khmeracons': {
     'KhmerLoC' : 'អ',
     'KhmerLoCRomanLoC': '‛ʹ',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
 },
 'khmeraconsmod': {
     'KhmerLoC' : 'អ៊',
     'KhmerLoCRomanLoC': '‛ʹ′',
     'OthersRev': [0, '\u02C2'],
     'OthersNonRev': [0, '\u02C2'],
 },
 'ThamDoubleNJNJ': {
     'ThamLoC' : 'ᨬᩚ',
     'ThamLoCRomanLoC': 'ññ',
     'OthersRev': [9, '\u02C2'],
     'OthersNonRev': [9, '\u02C2'],
 },

}

SignMap = {
    'shanexcl' : {
        'ShanLoC': '႟',
        'Shan': '႟',
        'ShanLoCRomanLoC': 'u*',
        'OthersRev': [-1, '!\u02C2\u02C2\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '!\u02C2\u02C2\u02C2\u02C2'],
    },
    'shanone' : {
        'ShanLoC': '႞',
        'Shan': '႞',
        'ShanLoCRomanLoC': 'n*',
        'OthersRev': [-1, '!!\u02C2'],
        'OthersNonRev': [-1, '!!\u02C2'],
    },
    'Khmerdivider' : {
      'KhmerLoC': '៖',
      'KhmerLoCRomanLoC': ':',
     'OthersRev': [-1, '!!!\u02C2'],
     'OthersNonRev': [-1, '!!!\u02C2'],
    },
    'Thamlae': {
        'ThamLoC': 'ᩓ',
        'ThamLoCRomanLoC': 'læ',
        'OthersRev': [-1, '!!!\u02C2'],
        'OthersNonRev': [-1, '!!!\u02C2'],
    },
    """'Danda1': {
        'Devanagari': '│',
        'OthersRev': [1, '\u02C2'],
        'OthersNonRev': [1, '\u02C2'],
    },
    'Danda2': {
        'Devanagari': '┃',
        'OthersRev': [2, '\u02C2'],
        'OthersNonRev': [2, '\u02C2'],
    },"""
    'Thamlae': {
        'ThamLoC': 'ᩓ',
        'ThamLoCRomanLoC': 'læ',
        'OthersRev': [-1, '!!!\u02C2'],
        'OthersNonRev': [-1, '!!!\u02C2'],
    }
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
    },
    'shantone2' : {
        'ShanLoC': 'ႇ',
        'Shan': 'ႇ',
        'ShanLoCRomanLoC': '\u0322',
        'OthersRev': [-1, '\u02C2'],
        'OthersNonRev': [-1, '\u02C2'],
    },
    'shantone3' : {
        'ShanLoC': 'ႈ',
        'Shan': 'ႈ',
        'ShanLoCRomanLoC': '\u0310',
        'OthersRev': [-1, '\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2'],
    },
    'shantone5' : {
        'ShanLoC': 'ႉ',
        'Shan': 'ႉ',
        'ShanLoCRomanLoC': 'ʹ',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2'],
    },
    'shantone6' : {
        'ShanLoC': 'ႊ',
        'Shan': 'ႊ',
        'ShanLoCRomanLoC': '˝',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2\u02C2'],
    },
    'KhmerTone3' : {
        'KhmerLoC': '៍',
        'KhmerLoCRomanLoC': '\u02DA',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2'],
    },
    'KhmerTone4' : {
        'KhmerLoC': '៎',
        'KhmerLoCRomanLoC': '’',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2'],
    },
    'KhmerTone5' : {
        'KhmerLoC': '៏',
        'KhmerLoCRomanLoC': 'ʻ',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2'],
    },
  'Khmerbreve': {
      'KhmerLoC': '័',
      'KhmerLoCRomanLoC': '\u0306',
     'OthersRev': [-1, '\u02C2'],
     'OthersNonRev': [-1, '\u02C2'],
  },
  'Khmervisarga2': {
      'KhmerLoC': 'ៈ',
      'KhmerLoCRomanLoC': '\u0300',
     'OthersRev': [-1, '\u02C2'],
     'OthersNonRev': [-1, '\u02C2'],
  },
  'Khmershortener': {
      'KhmerLoC': '់',
      'KhmerLoCRomanLoC': '\u0301',
     'OthersRev': [-1, '\u02C2'],
     'OthersNonRev': [-1, '\u02C2'],
  },
    'ThamTone1': {
        'ThamLoC': '᩵',
        'TaiTham': '᩵',
        'LaoTham': '᩵',
        'LueTham': '᩵',
        'KhuenTham': '᩵',
        'ThamLoCRomanLoC': '\u2032',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
    },
    'ThamTone2': {
        'ThamLoC': '᩶',
        'TaiTham': '᩶',
        'LaoTham': '᩶',
        'LueTham': '᩶',
        'KhuenTham': '᩶',
        'ThamLoCRomanLoC': '\u2033',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
    },
    'ThamTone3': {
        'ThamLoC': '᩷',
        'TaiTham': '᩷',
        'LaoTham': '᩷',
        'LueTham': '᩷',
        'KhuenTham': '᩷',
        'ThamLoCRomanLoC': 'ˆ',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
    },
    'ThamTone4': {
        'ThamLoC': '᩸',
        'TaiTham': '᩸',
        'LaoTham': '᩸',
        'LueTham': '᩸',
        'KhuenTham': '᩸',
        'ThamLoCRomanLoC': 'ᴶ',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
    },
    'ThamTone5': {
        'ThamLoC': '᩹',
        'TaiTham': '᩹',
        'LaoTham': '᩹',
        'LueTham': '᩹',
        'KhuenTham': '᩹',
        'ThamLoCRomanLoC': 'ʵ',
        'OthersRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
        'OthersNonRev': [-1, '\u02C2\u02C2\u02C2\u02C2\u02C2'],
    }
}