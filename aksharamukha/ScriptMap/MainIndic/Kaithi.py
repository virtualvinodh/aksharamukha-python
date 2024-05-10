# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011083',
            '\U00011084',
            '\U00011085',
            '\U00011086',
            '\U00011087',
            '\U00011088',
            '𑂩𑂱\u02BD',
            '𑂩𑂲\u02BD',
            '𑂪𑂱\u02BD',
            '𑂪𑂲\u02BD',
            '\U00011089',
            '\U0001108A',
            '\U0001108B',
            '\U0001108C',
            ]

SouthVowelMap = [
                '\U00011089\u02BD',
                '\U0001108B\u02BD',
                ]

ModernVowelMap = [
                 '\U00011089\u02BD',
                 '\U00011084\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U00011089\u02BD'
                  ]

VowelSignMap =  [
                '\U000110B0',
                '\U000110B1',
                '\U000110B2',
                '\U000110B3',
                '\U000110B4',
                '\U000110C2',
                '𑂹𑂩𑂲\u02BD',
                '𑂹𑂪𑂱\u02BD',
                '𑂹𑂪𑂲\u02BD',
                '\U000110B5',
                '\U000110B6',
                '\U000110B7',
                '\U000110B8',
                ]

SouthVowelSignMap = [
                    '\U000110B5\u02BD',
                    '\U000110B7\u02BD',
                    ]

ModernVowelSignMap =[
                    '\U000110B5\u02BD',
                    '\U000110B0\u02BD']

SinhalaVowelSignMap = [
                      '\U000110B5\u02BD'
                      ]

AyogavahaMap = [
               '\U00011080',
               '\U00011081',
               '\U00011082'
               ]

ViramaMap =  [
             '\U000110B9'
             ]

ConsonantMap =  [
                '\U0001108D',
                '\U0001108E',
                '\U0001108F',
                '\U00011090',
                '\U00011091',

                '\U00011092',
                '\U00011093',
                '\U00011094',
                '\U00011095',
                '\U00011096',

                '\U00011097',
                '\U00011098',
                '\U00011099',
                '\U0001109B',
                '\U0001109D',

                '\U0001109E',
                '\U0001109F',
                '\U000110A0',
                '\U000110A1',
                '\U000110A2',

                '\U000110A3',
                '\U000110A4',
                '\U000110A5',
                '\U000110A6',
                '\U000110A7',

                '\U000110A8',
                '\U000110A9',
                '\U000110AA',
                '\U000110AB',

                '\U000110AC',
                '\U000110AD',
                '\U000110AE',
                '\U000110AF'
                ]

SouthConsonantMap = [
                    '𑂪𑂺',
                    '𑂭𑂺',
                    '𑂩𑂺',
                    '𑂢𑂺'
                    ]

NuktaConsonantMap =  [
                     '𑂍𑂺',
                     '𑂎𑂺',
                     '𑂏𑂺',
                     '𑂔𑂺',
                     '𑂚',
                     '𑂜',
                     '𑂤𑂺',
                     '𑂨𑂺'
                     ]

SinhalaConsonantMap =[
                     '𑂀𑂏\u02BD',
                     '𑂀𑂔\u02BD',
                     '𑂀𑂙\u02BD',
                     '𑂀𑂠\u02BD',
                     '𑂀𑂥\u02BD',
                      ]

NuktaMap = [
           '𑂺'
           ]

OmMap = [
        '𑂋𑂁'
        ]

SignMap =[
         '\u093D',
         '𑃀',
         '𑃁'
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
