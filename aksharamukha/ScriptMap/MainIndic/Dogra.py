# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011800',
            '\U00011801',
            '\U00011802',
            '\U00011803',
            '\U00011804',
            '\U00011805',
            '\U00011824\U0001182D\u02BD',
            '\U00011824\U0001182E\u02BD',
            '\U00011825\U0001182D\u02BD',
            '\U00011825\U0001182E\u02BD',
            '\U00011806',
            '\U00011807',
            '\U00011808',
            '\U00011809',
            ]

SouthVowelMap = [
                '\U00011806\u02BD',
                '\U00011808\u02BD',
                ]

ModernVowelMap = [
                 '\U00011806\u02BD',
                 '\U00011801\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U00011806\u02BD'
                  ]

VowelSignMap =  [
                '\U0001182C',
                '\U0001182D',
                '\U0001182E',
                '\U0001182F',
                '\U00011830',
                '\U00011831',
                '\U00011832',
                '\U00011839\U00011825\U0001182D\u02BD',
                '\U00011839\U00011825\U0001182E\u02BD',
                '\U00011833',
                '\U00011834',
                '\U00011835',
                '\U00011836',
                ]

SouthVowelSignMap = [
                    '\U00011833\u02BD',
                    '\U00011835\u02BD',
                    ]

ModernVowelSignMap =[
                    '\U00011833\u02BD',
                    '\U0001182C\u02BD']

SinhalaVowelSignMap = [
                      '\U00011833\u02BD'
                      ]

AyogavahaMap = [
               '\U00011837\u02BD',
               '\U00011837',
               '\U00011838'
               ]

ViramaMap =  [
             '\U00011839'
             ]

ConsonantMap =  [
                '\U0001180A',
                '\U0001180B',
                '\U0001180C',
                '\U0001180D',
                '\U0001180E',

                '\U0001180F',
                '\U00011810',
                '\U00011811',
                '\U00011812',
                '\U00011813',

                '\U00011814',
                '\U00011815',
                '\U00011816',
                '\U00011817',
                '\U00011818',

                '\U00011819',
                '\U0001181A',
                '\U0001181B',
                '\U0001181C',
                '\U0001181D',

                '\U0001181E',
                '\U0001181F',
                '\U00011820',
                '\U00011821',
                '\U00011822',

                '\U00011823',
                '\U00011824',
                '\U00011825',
                '\U00011826',

                '\U00011827',
                '\U00011828',
                '\U00011829',
                '\U0001182A'
                ]

SouthConsonantMap = [
                    '\U00011825\U0001183A',
                    '\U00011828\U0001183A',
                    '\U00011824\U0001183A',
                    '\U0001181D\U0001183A'
                    ]

NuktaConsonantMap =  [
                     '\U0001180A\U0001183A',
                     '\U0001180B\U0001183A',
                     '\U0001180C\U0001183A',
                     '\U00011811\U0001183A',
                     '\U0001182B',
                     '\U00011817\U0001183A',
                     '\U0001181F\U0001183A',
                     '\U00011823\U0001183A'
                     ]

SinhalaConsonantMap =[
                     '\U00011837\U0001180C\u02BD',
                     '\U00011837\U00011811\u02BD',
                     '\U00011837\U00011816\u02BD',
                     '\U00011837\U0001181B\u02BD',
                     '\U00011837\U00011820\u02BD',
                      ]

NuktaMap = [
           '\U0001183A'
           ]

OmMap = [
        '\U00011808\U00011837'
        ]

SignMap =[
         '\u093D',
         '\u0964',
         '\u0965'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '\u0966',
             '\u0967',
             '\u0968',
             '\u0969',
             '\u096A',
             '\u096B',
             '\u096C',
             '\u096D',
             '\u096E',
             '\u096F'
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
