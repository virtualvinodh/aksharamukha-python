# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011F04',
            '\U00011F05',
            '\U00011F06',
            '\U00011F07',
            '\U00011F08',
            '\U00011F09',
            '\U00011F0A',
            '\U00011F0B',
            '\U00011F0C',
            '\U00011F0D',
            '\U00011F0E',
            '\U00011F0F',
            '\U00011F10',
            '\U00011F10\U00011F34',
            ]

SouthVowelMap = [
                '\U00011F0E\u02BD',
                '\U00011F10\u02BD',
                ]

ModernVowelMap = [
                 '\U00011F04\U00011F40',
                 '\U00011F05\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U00011F04\U00011F40\U00011F34'
                  ]

VowelSignMap =  [
                '\U00011F34',
                '\U00011F36',
                '\U00011F37',
                '\U00011F38',
                '\U00011F39',
                '\U00011F3A',
                '\U00011F42\U00011F0B',
                '\U00011F42\U00011F0C',
                '\U00011F42\U00011F0D',
                '\U00011F3E',
                '\U00011F3F',
                '\U00011F3E\U00011F34',
                '\U00011F3F\U00011F34',
                ]

SouthVowelSignMap = [
                    '\U00011F3E\u02BD',
                    '\U00011F3E\U00011F34\u02BD',
                    ]

ModernVowelSignMap =[
                    '\U00011F40',
                    '\U00011F34\u02BD']

SinhalaVowelSignMap = [
                      '\U00011F40\U00011F34'
                      ]

AyogavahaMap = [
               '\U00011F00',
               '\U00011F01',
               '\U00011F03'
               ]

ViramaMap =  [
             '\U00011F41'
             ]

ConsonantMap =  [
                '\U00011F12',
                '\U00011F13',
                '\U00011F14',
                '\U00011F15',
                '\U00011F16',

                '\U00011F17',
                '\U00011F18',
                '\U00011F19',
                '\U00011F1A',
                '\U00011F1B',

                '\U00011F1C',
                '\U00011F1D',
                '\U00011F1E',
                '\U00011F1F',
                '\U00011F20',

                '\U00011F21',
                '\U00011F22',
                '\U00011F23',
                '\U00011F24',
                '\U00011F25',

                '\U00011F26',
                '\U00011F27',
                '\U00011F28',
                '\U00011F29',
                '\U00011F2A',

                '\U00011F2B',
                '\U00011F2C',
                '\U00011F2D',
                '\U00011F2E',

                '\U00011F2F',
                '\U00011F30',
                '\U00011F31',
                '\U00011F32'
                ]

SouthConsonantMap = [
                    '\U00011F2D\u02BD',
                    '\U00011F2D\u02BD',
                    '\U00011F2C\u02BD',
                    '\U00011F25\u02BD'
                    ]

NuktaConsonantMap =  [
                     '\U00011F12\u02BD',
                     '\U00011F13\u02BD',
                     '\U00011F14\u02BD',
                     '\U00011F19\u02BD',
                     '\U00011F1E\u02BD',
                     '\U00011F1E\u02BD',
                     '\U00011F27\u02BD',
                     '\U00011F2B\u02BD'
                     ]

SinhalaConsonantMap =[
                     '\U00011F00\U00011F14\u02BD',
                     '\U00011F00\U00011F19\u02BD',
                     '\U00011F00\U00011F1E\u02BD',
                     '\U00011F00\U00011F23\u02BD',
                     '\U00011F00\U00011F28\u02BD',
                      ]

NuktaMap = [
           '\u02BD\u02BD\u02BD\u02BD'
           ]

OmMap = [
        '\U00011F10\U00011F00'
        ]

SignMap =[
         '\u02BD\u02BD\u02BD',
         '\U00011F43',
         '\U00011F44'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']


NumeralMap = [
             '\U00011F50',
             '\U00011F51',
             '\U00011F52',
             '\U00011F53',
             '\U00011F54',
             '\U00011F55',
             '\U00011F56',
             '\U00011F57',
             '\U00011F58',
             '\U00011F59',
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
