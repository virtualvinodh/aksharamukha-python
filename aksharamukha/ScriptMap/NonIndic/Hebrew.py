# -*- coding: utf-8 -*-

# Script Mapping for ISO

VowelMap =  [
            'א' + '\u05B7',
            'א' + '\u05B8',
            'א' + '\u05B4',
            'א' + '\u05B4\u05D9',
            'א' + '\u05BB',
            'א' + 'וּ' + '',
            'רֻ' + '\u02BD',
            'רוּ' + '\u02BD',
            'לֻ' + '\u02BD',
            'לוּ' + '\u02BD',
            'א' + '\u05B5',
            'א' + '\u05B7' + 'ײ' + '\u05B0' + '\u02BD',
            'א' + '\u05D5\u05B9'  + '',
            'א' + '\u05B7' + 'ו'  + '\u05B0' + '\u02BD',
            ]

SouthVowelMap = [
            'א' + '\u05B6',
            'א' + '\u05B9',
                ]

ModernVowelMap = [
            'א' + '\u05B8\u02BD',
            'א' + '\u05B9\u02BD',
                 ]

SinhalaVowelMap = [
            'א' + '\u05B5\u02BD',
                  ]

VowelSignMap =  [
                '\u05B8',
                '\u05B4',
                '\u05B4\u05D9',
                '\u05BB',
                'וּ',
                '\u05B0' + 'רֻ' + '\u02BD',
                '\u05B0' + 'רוּ' + '\u02BD',
                '\u05B0' + 'לֻ' + '\u02BD',
                '\u05B0' 'לוּ' + '\u02BD',
                '\u05B5',
                '\u05B7' + 'ײ' + '\u05B0' + '\u02BD',
                '\u05D5\u05B9',
                '\u05B7' + 'ו' + '\u05B0' + '\u02BD',
                ]

SouthVowelSignMap = [
                    '\u05B6',
                    '\u05B9',
                    ]

ModernVowelSignMap =[
                    '\u05B8\u02BD',
                    '\u05B9\u02BD']

SinhalaVowelSignMap = [
                      '\u05B5\u02BD'
                      ]

AyogavahaMap = [
               'מְ' + '\u02BC',
               'מְ' + '\u02BC',
               'הְּ'  + '\u02BD'
               ]

ViramaMap =  [
             '\u05B0'
             ]

ConsonantMap =  [
                'כּ',
                'כ\u02BD',
                'ג',
                'ג\u02BD',
                'נ\u02BD',

                'צ׳',
                'צ׳\u02BD',
                'ג׳',
                'ג׳\u02BD',
                'נ\u02BD',

                'ט\u02BD',
                'ט\u02BD',
                'ד\u02BD',
                'ד\u02BD',
                'נ\u02BD',

                'ט',
                'ט\u02BD',
                'ד',
                'ד\u02BD',
                'נ',

                'פּ',
                'פּ\u02BD',
                'בּ',
                'בּ\u02BD',
                'מ',

                'ײ',
                'ר',
                'ל',
                'װ',

                'שׁ\u02BD',
                'שׁ',
                'ס',
                'ה',
                ]

SouthConsonantMap = [
                    'ל\u02BD',
                    'ל\u02BD',
                    'ר\u02BD',
                    'נ\u02BD'
                    ]

NuktaConsonantMap =  [
                     'ק',
                     'כ',
                     'גּ',
                     'ז',
                     'ד\u02BD',
                     'ד\u02BD',
                     'פ',
                     'ײ\u02BD'
                     ]

SinhalaConsonantMap =[
                     'נְגַ\u02BD',
                     'נְגַ׳\u02BD',
                     'נְדַ\u02BD',
                     'נְדַ\u02BD',
                     'מְבַּ\u02BD',
                      ]

NuktaMap = [
           '\u02BE'
           ]

OmMap = [
        'א' + 'וֹמְ'  + '\u02BD'
        ]

SignMap =[
         '\u0027\u02BD',
         '\u002E',
         '\u002E\u002E'
         ]

Aytham =['הְ' + '\u02BD']

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
