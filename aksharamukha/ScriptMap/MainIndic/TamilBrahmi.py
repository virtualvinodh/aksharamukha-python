# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011005',
            '\U00011006',
            '\U00011007',
            '\U00011008',
            '\U00011009',
            '\U0001100A',
            '\U0001102D\U0001103C\u02BD',
            '\U0001102D\U0001103D\u02BD',
            '\U0001102E\U0001103C\u02BD',
            '\U0001102E\U0001103D\u02BD',
            '\U0001100F',
            '\U00011010',
            '\U00011011',
            '\U00011012',
            ]

SouthVowelMap = [
                '\U0001100F\U00011046',
                '\U00011011\U00011046',
                ]

ModernVowelMap = [
                 '\U0001100F\U00011046\u02BD',
                 '\U00011006\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U0001100F\u02BD'
                  ]

VowelSignMap =  [
                '\U00011038',
                '\U0001103A',
                '\U0001103B',
                '\U0001103C',
                '\U0001103D',
                '\U00011046\U0001102D\U0001103C\u02BD',
                '\U00011046\U0001102D\U0001103D\u02BD',
                '\U00011046\U0001102E\U0001103C\u02BD',
                '\U00011046\U0001102E\U0001103D\u02BD',
                '\U00011042',
                '\U00011043',
                '\U00011044',
                '\U00011045',
                ]

SouthVowelSignMap = [
                    '\U00011042\U00011046',
                    '\U00011044\U00011046',
                    ]

ModernVowelSignMap =[
                    '\U00011042\U00011046\u02BD',
                    '\U00011038\u02BD'
                    ]

SinhalaVowelSignMap = [
                      '\U00011042\u02BD'
                      ]

AyogavahaMap = [
                '\U0001102B\U00011046\u02BD',
                '\U0001102B\U00011046\u02BD',
                '\U00011002\u02BD'
               ]

ViramaMap =  [
             '\U00011046'
             ]

ConsonantMap =  [
                '\U00011013',
                '\U00011013\u02BD',
                '\U00011013\u02BD',
                '\U00011013\u02BD',
                '\U00011017',

                '\U00011018',
                '\U00011018\u02BD',
                '\U0001101A',
                '\U0001101A\u02BD',
                '\U0001101C',

                '\U0001101D',
                '\U0001101D\u02BD',
                '\U0001101D\u02BD',
                '\U0001101D\u02BD',
                '\U00011021',

                '\U00011022',
                '\U00011022\u02BD',
                '\U00011022\u02BD',
                '\U00011025',
                '\U00011026',

                '\U00011027',
                '\U00011027\u02BD',
                '\U00011027\u02BD',
                '\U00011027\u02BD',
                '\U0001102B',

                '\U0001102C',
                '\U0001102D',
                '\U0001102E',
                '\U0001102F',

                '\U00011030',
                '\U00011031',
                '\U00011032',
                '\U00011033'
                ]

SouthConsonantMap = [
                    '\U00011034',
                    '\U00011035',
                    '\U00011036',
                    '\U00011037'
                    ]

NuktaConsonantMap =  [
                     '\U00011013\u02BD',
                     '\U00011013\u02BD',
                     '\U00011013\u02BD',
                     '\U0001101A\u02BD',
                     '\U0001101D\u02BD',
                     '\U0001101D\u02BD',
                     '\U00011027\u02BD',
                     '\U0001102C\u02BD'
                     ]

SinhalaConsonantMap =[
                     '\U00011017\U00011046\U00011013\u02BD',
                     '\U0001101C\U00011046\U0001101A\u02BD',
                     '\U00011021\U00011046\U0001101D\u02BD',
                     '\U00011026\U00011046\U00011022\u02BD',
                     '\U0001102B\U00011046\U00011027\u02BD',
                      ]

NuktaMap = [
           '\u02BD\u02BD\u02BD\u02BD'
           ]

OmMap = [
        '\U00011011\U0001102B\U00011046'
        ]

SignMap =[
         "'",
         '\u002E',
         '\u002E\u002E'
         ]

Aytham =['\U00011002']

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
