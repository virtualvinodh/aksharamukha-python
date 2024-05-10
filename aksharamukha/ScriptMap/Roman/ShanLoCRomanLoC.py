# -*- coding: utf-8 -*-

# Script Mapping for ISO

VowelMap =  [
            '\u0061',
            '\u0101',
            '\u0069',
            '\u012B',
            '\u0075',
            '\u016B',
            '\u1E5B',
            '\u1E5D',
            '\u1E37',
            '\u1E39',
            '\u0065',
            '\u0061\u0069',
            '\u006F',
            '\u0061\u0075'
            ]

SouthVowelMap = [
                '\u0115',
                '\u014F',
                ]

ModernVowelMap = [
                 'è',
                 '\u00F4',
                 ]

SinhalaVowelMap = [
                  '\u01E3'
                  ]

VowelSignMap =  VowelMap[1:]

SouthVowelSignMap = SouthVowelMap[:]

ModernVowelSignMap = ModernVowelMap[:]

SinhalaVowelSignMap = SinhalaVowelMap[:]

AyogavahaMap = [
               '\u006D\u0310\u02BD',
               '\u1E43',
               'ʺ'
               ]

ViramaMap =  [
             '\u00D7'
             ]

ConsonantMap =  [
                '\u006B',
                '\u006B\u0068',
                '\u0067',
                '\u0067\u0068',
                '\u1E45',

                '\u0063',
                '\u0063\u0068',
                'z',
                '\u006A\u0068',
                '\u00F1',

                '\u1E6D',
                '\u1E6D\u0068',
                '\u1E0D',
                '\u1E0D\u0068',
                '\u1E47',

                '\u0074',
                '\u0074\u0068',
                '\u0064',
                '\u0064\u0068',
                '\u006E',

                '\u0070',
                '\u0070\u0068',
                '\u0062',
                '\u0062\u0068',
                '\u006D',

                '\u0079',
                '\u0072',
                '\u006C',
                '\u0076',

                '\u015B',
                '\u1E63',
                '\u0073',
                '\u0068',
                ]

SouthConsonantMap = [
                    'ḷ',
                    '\u1E3B',
                    '\u1E5F',
                    '\u1E49'
                    ]

NuktaConsonantMap =  [
                     '\u0071',
                     '\u006B\u035F\u0068',
                     '\u0121',
                     '\u007A',
                     '\u0072\u0324',
                     '\u0072\u0324\u0068',
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
        '\u006F\u1E43'
        ]

SignMap =[
         '\u0027',
         ',',
         '.'
         ]

Aytham =['\u1E35']

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