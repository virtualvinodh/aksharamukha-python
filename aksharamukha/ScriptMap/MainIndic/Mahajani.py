# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011150',
            '\U00011150\u02BD',
            '\U00011151',
            '\U00011151\u02BD',
            '\U00011152',
            '\U00011152\u02BD',
            '\U0001116D\U00011152\u02BD',
            '\U0001116D\U00011152\u02BD',
            '\U0001116E\U00011152\u02BD',
            '\U0001116E\U00011152\u02BD',
            '\U00011153',
            '\U00011151\u02BD',
            '\U00011154',
            '\U00011152\u02BD',
            ]

SouthVowelMap = [
                '\U00011153\u02BD',
                '\U00011154\u02BD',
                ]

ModernVowelMap = [
                 '\U00011153\u02BD',
                 '\U00011150\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U00011153\u02BD'
                  ]

VowelSignMap =  [
                '\U00011150\u02BD',
                '\U00011151\u02BD',
                '\u02BF\U00011151',
                '\U00011152\u02BD',
                '\U00011152\u02BD',
                '\U0001116D\U00011152\u02BD',
                '\U0001116D\U00011152\u02BD',
                '\U0001116E\U00011152\u02BD',
                '\U0001116E\U00011152\u02BD',
                '\U00011153\u02BD',
                '\U00011151\u02BD',
                '\U00011154\u02BD',
                '\U00011152\u02BD',
                ]

SouthVowelSignMap = [
                     '\U00011153\u02BD',
                     '\U00011154\u02BD',
                    ]

ModernVowelSignMap =[
                     '\U00011153\u02BD',
                     '\U00011150\u02BD',
                    ]

SinhalaVowelSignMap = [
                    '\U00011153\u02BD'
                      ]

AyogavahaMap = [
               '\U00011167\u02BD',
               '\U00011167\u02BD',
               '\U00011171\u02BD'
               ]

ViramaMap =  [
             '\u02BE'
             ]

ConsonantMap =  [
                '\U00011155',
                '\U00011156',
                '\U00011157',
                '\U00011158',
                '\U00011167\u02BD',

                '\U00011159',
                '\U0001115A',
                '\U0001115B',
                '\U0001115C',
                '\U0001115D',

                '\U0001115E',
                '\U0001115F',
                '\U00011160',
                '\U00011161',
                '\U00011162',

                '\U00011163',
                '\U00011164',
                '\U00011165',
                '\U00011166',
                '\U00011167',

                '\U00011168',
                '\U00011169',
                '\U0001116A',
                '\U0001116B',
                '\U0001116C',

                '\U0001115B\u02BD',
                '\U0001116D',
                '\U0001116E',
                '\U0001116F',

                '\U00011170\U00011173',
                '\U00011156\U00011173\u02BD',
                '\U00011170',
                '\U00011171'
                ]

SouthConsonantMap = [
                    '\U0001116E\U00011173',
                    '\U0001116E\U00011173\u02BD',
                    '\U0001116D\U00011173',
                    '\U00011167\U00011173'
                    ]

NuktaConsonantMap =  [
                     '\U00011155\U00011173',
                     '\U00011156\U00011173',
                     '\U00011157\U00011173',
                     '\U0001115B\U00011173',
                     '\U00011172',
                     '\U00011161\U00011173',
                     '\U00011169\U00011173',
                     '\U0001115B\u02BD'
                     ]

SinhalaConsonantMap =[
                     '\U00011167\U00011157\u02BD',
                     '\U00011167\U0001115B\u02BD',
                     '\U00011167\U00011160\u02BD',
                     '\U00011167\U00011165\u02BD',
                     '\U00011167\U0001116A\u02BD',
                      ]

NuktaMap = [
           '\U00011173'
           ]

OmMap = [
        '\U00011154\U0001116C'
        ]

SignMap =[
         '\u02BD\u02BD',
         '।',
         '॥'
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
