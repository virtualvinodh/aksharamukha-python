# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011200',
            '\U00011201',
            '\U00011240',
            '\U00011202',
            '\U00011203',
            '\U00011203\u02BD',
            '\U00011226\U0001122D\u02BD',
            '\U00011226\U0001122E\u02BD',
            '\U00011227\U0001122D\u02BD',
            '\U00011227\U0001122E\u02BD',
            '\U00011204',
            '\U00011205',
            '\U00011206',
            '\U00011207',
            ]

SouthVowelMap = [
                '\U00011204\u02BD',
                '\U00011206\u02BD',
                ]

ModernVowelMap = [
                 '\U00011204\u02BD',
                 '\U00011201\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U00011204\u02BD'
                  ]

VowelSignMap =  [
                '\U0001122C',
                '\U0001122D',
                '\U0001122E',
                '\U0001122F',
                '\U0001122F\u02BD',
                '\U00011241',
                '\U00011235\U00011226\U0001122E\u02BD',
                '\U00011235\U00011227\U0001122D\u02BD',
                '\U00011235\U00011227\U0001122E\u02BD',
                '\U00011230',
                '\U00011231',
                '\U00011232',
                '\U00011233',
                ]

SouthVowelSignMap = [
                '\U00011230\u02BD',
                '\U00011232\u02BD',
                    ]

ModernVowelSignMap =[
                 '\U00011230\u02BD',
                 '\U0001122C\u02BD',
                    ]

SinhalaVowelSignMap = [
                  '\U00011230\u02BD'
                      ]

AyogavahaMap = [
               '\U00011234\u02BD',
               '\U00011234',
               '\U0001122A\U00011235\u02BD'
               ]

ViramaMap =  [
             '\U00011235'
             ]

ConsonantMap =  [
                '\U00011208',
                '\U00011209',
                '\U0001120A',
                '\U0001120C',
                '\U0001120D',

                '\U0001120E',
                '\U0001120F',
                '\U00011210',
                '\U00011210\u02BD',
                '\U00011213',

                '\U00011214',
                '\U00011215',
                '\U00011216',
                '\U00011217',
                '\U00011218',

                '\U00011219',
                '\U0001121A',
                '\U0001121B',
                '\U0001121D',
                '\U0001121E',

                '\U0001121F',
                '\U00011220',
                '\U00011221',
                '\U00011223',
                '\U00011224',

                '\U00011225',
                '\U00011226',
                '\U00011227',
                '\U00011228',

                '\U00011229\U00011236',
                '\U00011229\U00011236\u02BD',
                '\U00011229',
                '\U0001122A'
                ]

SouthConsonantMap = [
                    '\U0001122B',
                    '\U0001122B\U00011236',
                    '\U00011226\U00011236',
                    '\U0001121E\U00011236'
                    ]

NuktaConsonantMap =  [
                     '\U00011208\U00011236',
                     '\U00011209\U00011236',
                     '\U0001120A\U00011236',
                     '\U00011210\U00011236',
                     '\U00011216\U00011236',
                     '\U00011217\U00011236',
                     '\U00011220\U00011236',
                     '\U00011225\U00011236'
                     ]

SinhalaConsonantMap =[
                     '\U00011234\U0001120A\u02BD',
                     '\U00011234\U00011210\u02BD',
                     '\U00011234\U00011216\u02BD',
                     '\U00011234\U0001121B\u02BD',
                     '\U00011234\U00011221\u02BD',
                      ]

NuktaMap = [
           '\U00011236'
           ]

OmMap = [
        '\U00011206\U00011234'
        ]

SignMap =[
         '\u02BD\u02BD',
         '\U00011238',
         '\U00011239'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '\u0AE6',
             '\u0AE7',
             '\u0AE8',
             '\u0AE9',
             '\u0AEA',
             '\u0AEB',
             '\u0AEC',
             '\u0AED',
             '\u0AEE',
             '\u0AEF'
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
