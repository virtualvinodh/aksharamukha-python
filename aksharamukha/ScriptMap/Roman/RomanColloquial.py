# -*- coding: utf-8 -*-

# Script Mapping for ISO

VowelMap =  [
            '\u0061',
            'a',
            '\u0069',
            'i',
            '\u0075',
            'u',
            'ri',
            'ri',
            'li',
            'li',
            'e',
            'ai',
            'o',
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
               '\u004D',
               '\u004D',
               'h'
               ]

ViramaMap =  [
             '\u00D7'
             ]

ConsonantMap =  [
                '\u006B',
                '\u006B\u0068',
                '\u0067',
                '\u0067\u0068',
                'ng',

                'ch',
                'chh',
                '\u006A',
                '\u006A\u0068',
                'nj',

                't\'',
                'th',
                'd\'',
                'dh',
                'n',

                't',
                'th',
                'd',
                'dh',
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

                'sh',
                'sh',
                '\u0073',
                '\u0068',
                ]

SouthConsonantMap = [
                    'l',
                    'zh',
                    'r',
                    'n'
                    ]

NuktaConsonantMap =  [
                     'q',
                     'kh',
                     'g',
                     'z',
                     'r\'',
                     'r\'h',
                     'f',
                     'y'
                     ]

SinhalaConsonantMap =[
                     'ng',
                     'nj',
                     'nd',
                     'nd',
                     'mb',
                      ]

NuktaMap = [
           '\u02BD\u02BD'
           ]

OmMap = [
        'Om'
        ]

SignMap =[
         '\'',
         '\u002E',
         '\u002E\u002E'
         ]

Aytham =['g']

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