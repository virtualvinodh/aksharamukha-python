# -*- coding: utf-8 -*-

# Script Mapping for ISO

VowelMap =  [
            '\u0061',
            'aa',
            '\u0069',
            'ii',
            '\u0075',
            'uu',
            'ri',
            'rii',
            'r\u309Ai',
            'r\u309Aii',
            'ee',
            'ai',
            'oo',
            'au'
            ]

SouthVowelMap = [
                'e',
                'o',
                ]

ModernVowelMap = [
                 'a',
                 'o',
                 ]

SinhalaVowelMap = [
                  'e'
                  ]

VowelSignMap =  VowelMap[1:]

SouthVowelSignMap = SouthVowelMap[:]

ModernVowelSignMap = ModernVowelMap[:]

SinhalaVowelSignMap = SinhalaVowelMap[:]

AyogavahaMap = [
               'n',
               'n',
               'H'
               ]

ViramaMap =  [
             '\u00D7'
             ]

ConsonantMap =  [
                '\u006B',
                '\u006B',
                '\u0067',
                '\u0067',
                'k\u309A',

                'c',
                'c',
                '\u006A',
                '\u006A',
                'J',

                't',
                't',
                'd',
                'd',
                'n',

                't',
                't',
                'd',
                'd',
                '\u006E',

                '\u0070',
                '\u0070',
                '\u0062',
                '\u0062',
                '\u006D',

                '\u0079',
                'r',
                'r\u309A',
                'v',

                'sh',
                'sh',
                '\u0073',
                '\u0068',
                ]

SouthConsonantMap = [
                'r\u309A',
                'r\u309A',
                    'r',
                    'n'
                    ]

NuktaConsonantMap =  [
                     'k',
                     'k',
                     'g',
                     'z',
                     'r',
                     'r',
                     'f',
                     'y'
                     ]

SinhalaConsonantMap =[
                     'ng',
                     'nj',
                     'nd',
                     'nd',
                     'nb',
                      ]

NuktaMap = [
           '\u02BD\u02BD'
           ]

OmMap = [
        'oon'
        ]

SignMap =[
         '\'',
         '。',
         '。。'
         ]

Aytham =['gu']

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