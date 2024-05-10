# -*- coding: utf-8 -*-

# Script Mapping for ISO

VowelMap =  [
            '\u0061',
            '\u0101',
            '\u0069',
            '\u012B',
            '\u0075',
            '\u016B',
            'rĕ',
            'rö',
            'lĕ',
            'lö',
            'e',
            '\u0061\u0069',
            'o',
            '\u0061\u0075'
            ]

SouthVowelMap = [
                'ĕ\u02BD',
                'ŏ\u02BD',
                ]

ModernVowelMap = [
                 'ĕ',
                 '\u00F4',
                 ]

SinhalaVowelMap = [
                  'ö'
                  ]

VowelSignMap =  VowelMap[1:]

SouthVowelSignMap = SouthVowelMap[:]

ModernVowelSignMap = ModernVowelMap[:]

SinhalaVowelSignMap = SinhalaVowelMap[:]

AyogavahaMap = [
               'ng',
               'ng',
               'h'
               ]

ViramaMap =  [
             '\u00D7'
             ]

ConsonantMap =  [
                '\u006B',
                'k\u02BD',
                '\u0067',
                'g\u0068',
                'ng',

                '\u0063',
                '\u0063\u02BD',
                '\u006A',
                '\u006A\u02BD',
                '\u00F1',

                '\u1E6D',
                '\u1E6D\u02BD',
                '\u1E0D',
                '\u1E0D\u02BD',
                'n',

                '\u0074',
                '\u0074\u02BD',
                '\u0064',
                '\u0064\u0068',
                '\u006E',

                '\u0070',
                '\u0070\u02BD',
                '\u0062',
                '\u0062\u02BD',
                '\u006D',

                '\u0079',
                '\u0072',
                '\u006C',
                'w',

                's',
                's',
                '\u0073',
                '\u0068',
                ]

SouthConsonantMap = [
                    '\u1E37',
                    '\u1E3B',
                    '\u1E5F',
                    '\u1E49'
                    ]

NuktaConsonantMap =  [
                     'kh\u02BD',
                     '\u006B\u035F\u0068',
                     'gh\u02BD',
                     '\u007A',
                     '\u1E5B',
                     '\u1E5B\u0068',
                     '\u0066',
                     '\u1E8F'
                     ]

SinhalaConsonantMap =[
                     '\u006E\u0306\u0067',
                     '\u006E\u0306\u006A',
                     '\u006E\u0306\u1E0D',
                     '\u006E\u0306\u0064',
                     '\u006D\u0306\u0062',
                      ]
NuktaMap = [
           '\u0308'
           ]

OmMap = [
        '\u014D\u1E41'
        ]

Aytham =['\u1E35']

SignMap =[
         '’',
         '\u002E',
         '\u002E\u002E'
         ]

NumeralMap = [
             '\u0030',
             '\u0031',
             '\u0032',
             '\u0033',
             '\u0034',
             '\u0035',
             '\u0036',
             '\u0037',
             '\u0038',
             '\u0039',
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])