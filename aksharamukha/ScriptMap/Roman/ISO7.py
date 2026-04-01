# -*- coding: utf-8 -*-

# Script Mapping for ISO7

VowelMap =  [
            'a',
            'aa',
            'i',
            'ii',
            'u',
            'uu',
            '\u0072\u0325',
            '\u0072\u0325\u0304',
            '\u006C\u0325',
            '\u006C\u0325\u0304',
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
                 '\u00E6',
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
               '\u006D\u0310',
               ';m',
               '\u1E25'
               ]

ViramaMap =  [
             '\u00D7'
             ]

ConsonantMap =  [
                'k',
                '\u006B\u0068',
                '\u0067',
                '\u0067\u0068',
                ';n',

                'c',
                '\u0063\u0068',
                'j',
                '\u006A\u0068',
                '~n',

                '.t',
                '\u1E6D\u0068',
                '\u1E0D',
                '\u1E0D\u0068',
                '.n',

                't',
                '\u0074\u0068',
                '\u0064',
                '\u0064\u0068',
                'n',

                'p',
                '\u0070\u0068',
                '\u0062',
                '\u0062\u0068',
                'm',

                'y',
                'r',
                'l',
                'v',

                'sh',
                '.s',
                's',
                'h',
                ]

SouthConsonantMap = [
                    '.l',
                    '_l',
                    '_r',
                    '_n'
                    ]

NuktaConsonantMap =  [
                     '\u0071',
                     '\u006B\u035F\u0068',
                     '\u0121',
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

Aytham =['_k']

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
