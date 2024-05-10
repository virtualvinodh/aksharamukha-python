# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011305',
            '\U00011306',
            '\U00011307',
            '\U00011308',
            '\U00011309',
            '\U0001130A',
            '\U0001130B',
            '\U00011360',
            '\U0001130C',
            '\U00011361',
            '\U0001130F',
            '\U00011310',
            '\U00011313',
            '\U00011314',
            ]

SouthVowelMap = [
                '\U0001130F\U00011300',
                '\U00011313\U00011300',
                ]

ModernVowelMap = [
                 '\U0001130F\u02BD',
                 '\U00011306\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U0001130F\u02BD'
                  ]

VowelSignMap =  [
                '\U0001133E',
                '\U0001133F',
                '\U00011340',
                '\U00011341',
                '\U00011342',
                '\U00011343',
                '\U00011344',
                '\U00011362',
                '\U00011363',
                '\U00011347',
                '\U00011348',
                '\U0001134B',
                '\U00011357',
                ]

SouthVowelSignMap = [
                    '\U00011347\U00011300',
                    '\U0001134B\U00011300',
                    ]

ModernVowelSignMap =[
                    '\U00011347\u02BD',
                    '\U0001133E\u02BD']

SinhalaVowelSignMap = [
                      '\U00011347\u02BD'
                      ]

AyogavahaMap = [
               '\U00011301',
               '\U00011302',
               '\U00011303',
               ]

ViramaMap =  [
               '\U0001134D',
             ]

ConsonantMap =  [
                '\U00011315',
                '\U00011316',
                '\U00011317',
                '\U00011318',
                '\U00011319',

                '\U0001131A',
                '\U0001131B',
                '\U0001131C',
                '\U0001131D',
                '\U0001131E',

                '\U0001131F',
                '\U00011320',
                '\U00011321',
                '\U00011322',
                '\U00011323',

                '\U00011324',
                '\U00011325',
                '\U00011326',
                '\U00011327',
                '\U00011328',

                '\U0001132A',
                '\U0001132B',
                '\U0001132C',
                '\U0001132D',
                '\U0001132E',

                '\U0001132F',
                '\U00011330',
                '\U00011332',
                '\U00011335',

                '\U00011336',
                '\U00011337',
                '\U00011338',
                '\U00011339'
                ]

SouthConsonantMap = [
                    '\U00011333',
                    '\U00011333\U0001133C',
                    '\U00011330\U0001133C',
                    '\U00011328\U0001133C'
                    ]

NuktaConsonantMap =  [
                     '\U00011315\U0001133C',
                     '\U00011316\U0001133C',
                     '\U00011317\U0001133C',
                     '\U0001131C\U0001133C',
                     '\U00011321\U0001133C',
                     '\U00011322\U0001133C',
                     '\U0001132B\U0001133C',
                     '\U0001132F\U0001133C'
                     ]

SinhalaConsonantMap =[
                     '\U00011301\u02BD\U00011317',
                     '\U00011301\u02BD\U0001131C',
                     '\U00011301\u02BD\U00011321',
                     '\U00011301\u02BD\U00011326',
                     '\U00011301\u02BD\U0001132C',
                      ]

NuktaMap = [
           '\U0001133C'
           ]

OmMap = [
        '\U00011350'
        ]

SignMap =[
         '\U0001133D',
         '\u0964',
         '\u0965'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '\u0BE6',
             '\u0BE7',
             '\u0BE8',
             '\u0BE9',
             '\u0BEA',
             '\u0BEB',
             '\u0BEC',
             '\u0BED',
             '\u0BEE',
             '\u0BEF'
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
