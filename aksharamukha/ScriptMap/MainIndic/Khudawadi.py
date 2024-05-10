# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U000112B0',
            '\U000112B1',
            '\U000112B2',
            '\U000112B3',
            '\U000112B4',
            '\U000112B5',
            '𑋙𑋡\u02BD',
            '𑋙𑋢\u02BD',
            '𑋚𑋡\u02BD',
            '𑋚𑋢\u02BD',
            '\U000112B6',
            '\U000112B7',
            '\U000112B8',
            '\U000112B9',
            ]

SouthVowelMap = [
                '\U000112B6\u02BD',
                '\U000112B8\u02BD',
                ]

ModernVowelMap = [
                 '\U000112B6\u02BD',
                 '\U000112B1\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U000112B6\u02BD'
                  ]

VowelSignMap =  [
                '\U000112E0',
                '\U000112E1',
                '\U000112E2',
                '\U000112E3',
                '\U000112E4',
                '𑋪𑋙𑋡\u02BD',
                '𑋪𑋙𑋢\u02BD',
                '𑋪𑋚𑋡\u02BD',
                '𑋪𑋚𑋢\u02BD',
                '\U000112E5',
                '\U000112E6',
                '\U000112E7',
                '\U000112E8',
                ]

SouthVowelSignMap = [
                    '\U000112E5\u02BD',
                    '\U000112E7\u02BD',
                    ]

ModernVowelSignMap =[
                    '\U000112E5\u02BD',
                    '\U000112E0\u02BD'
                    ]

SinhalaVowelSignMap = [
                      '\U000112E5\u02BD'
                      ]

AyogavahaMap = [
               '\U000112DF\u02BD',
               '\U000112DF',
               '𑋞𑋪\u02BD'
               ]

ViramaMap =  [
             '\U000112EA'
             ]

ConsonantMap =  [
                '\U000112BA',
                '\U000112BB',
                '\U000112BC',
                '\U000112BE',
                '\U000112BF',

                '\U000112C0',
                '\U000112C1',
                '\U000112C2',
                '\U000112C4',
                '\U000112C5',

                '\U000112C6',
                '\U000112C7',
                '\U000112C8',
                '\U000112CB',
                '\U000112CC',

                '\U000112CD',
                '\U000112CE',
                '\U000112CF',
                '\U000112D0',
                '\U000112D1',

                '\U000112D2',
                '\U000112D3',
                '\U000112D4',
                '\U000112D6',
                '\U000112D7',

                '\U000112D8',
                '\U000112D9',
                '\U000112DA',
                '\U000112DB',

                '\U000112DC',
                '\U000112DC𑋩',
                '\U000112DD',
                '\U000112DE'
                ]

SouthConsonantMap = [
                    '𑋚𑋩',
                    '𑋚𑋩\u02BD',
                    '𑋙𑋩',
                    '𑋑𑋩'
                    ]

NuktaConsonantMap =  [
                     '𑊺𑋩',
                     '𑊻𑋩',
                     '𑊼𑋩',
                     '𑋂𑋩',
                     '𑋊',
                     '𑋋𑋩',
                     '𑋓𑋩',
                     '𑋘𑋩'
                     ]

SinhalaConsonantMap =[
                     '𑋟𑊼\u02BD',
                     '𑋟𑋂\u02BD',
                     '𑋟𑋈\u02BD',
                     '𑋟𑋏\u02BD',
                     '𑋟𑋔\u02BD',
                      ]

NuktaMap = [
           '𑋩'
           ]

OmMap = [
        '𑊸𑋟'
        ]

SignMap =[
         '\u093D',
         '।',
         '॥'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '\U000112F0',
             '\U000112F1',
             '\U000112F2',
             '\U000112F3',
             '\U000112F4',
             '\U000112F5',
             '\U000112F6',
             '\U000112F7',
             '\U000112F8',
             '\U000112F9',
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
