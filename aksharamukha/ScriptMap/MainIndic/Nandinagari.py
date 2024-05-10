# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U000119A0',
            '\U000119A1',
            '\U000119A2',
            '\U000119A3',
            '\U000119A4',
            '\U000119A5',
            '\U000119A6',
            '\U000119A7',
            '𑧉𑧔\u02BD', #lu
            '𑧉𑧕\u02BD', #luu
            '\U000119AA',
            '\U000119AB',
            '\U000119AC',
            '\U000119AD',
            ]

SouthVowelMap = [
                '\U000119AA\u02BD',
                '\U000119AC\u02BD',
                ]

ModernVowelMap = [
                 '\U000119AA\u02BD',
                 '\U000119A1\u02BD',
                 ]

SinhalaVowelMap = [
                '\U000119AA\u02BD',
                  ]

VowelSignMap =  [
                '\U000119D1',
                '\U000119D2',
                '\U000119D3',
                '\U000119D4',
                '\U000119D5',
                '\U000119D6',
                '\U000119D7',
            '\U000119E0𑧉𑧔\u02BD', #lu
            '\U000119E0𑧉𑧕\u02BD', #luu
                '\U000119DA',
                '\U000119DB',
                '\U000119DC',
                '\U000119DD',
                ]

SouthVowelSignMap = [
                '\U000119DA\u02BD',
                '\U000119DC\u02BD',
                    ]

ModernVowelSignMap =[
                    '\U000119D1\u02BD',
                    '\U000119DA\u02BD']

SinhalaVowelSignMap = [
                '\U000119DA\u02BD',
                      ]

AyogavahaMap = [
               '\U000119DE\u02BD',
               '\U000119DE',
               '\U000119DF'
               ]

ViramaMap =  [
             '\U000119E0'
             ]

ConsonantMap =  [
                '\U000119AE',
                '\U000119AF',
                '\U000119B0',
                '\U000119B1',
                '\U000119B2',

                '\U000119B3',
                '\U000119B4',
                '\U000119B5',
                '\U000119B6',
                '\U000119B7',

                '\U000119B8',
                '\U000119B9',
                '\U000119BA',
                '\U000119BB',
                '\U000119BC',

                '\U000119BD',
                '\U000119BE',
                '\U000119BF',
                '\U000119C0',
                '\U000119C1',

                '\U000119C2',
                '\U000119C3',
                '\U000119C4',
                '\U000119C5',
                '\U000119C6',

                '\U000119C7',
                '\U000119C8',
                '\U000119C9',
                '\U000119CA',

                '\U000119CB',
                '\U000119CC',
                '\U000119CD',
                '\U000119CE'
                ]

SouthConsonantMap = [
                    '\U000119CF\u02BD',
                    '\U000119CF',
                    '\U000119D0',
                    '\U000119C1\u02BD'
                    ]

NuktaConsonantMap =  [
                     '\U000119AE\u02BD',
                     '\U000119AF\u02BD',
                     '\U000119B0\u02BD',
                     '\U000119B5\u02BD',
                     '\U000119BA\u02BD',
                     '\U000119BB\u02BD',
                     '\U000119C3\u02BD',
                     '\U000119C7\u02BD'
                     ]

SinhalaConsonantMap =[
                     '\U000119DE\u02BD\U000119B0',
                     '\U000119DE\u02BD\U000119B5',
                     '\U000119DE\u02BD\U000119BA',
                     '\U000119DE\u02BD\U000119BF',
                     '\U000119DE\u02BD\U000119C4',
                      ]

NuktaMap = [
           '\u02BD\u02BD'
           ]

OmMap = [
        '\U000119AC\U000119DE'
        ]

SignMap =[
         '\U000119E1',
         '\u0964',
         '\u0965'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '\u0CE6',
             '\u0CE7',
             '\u0CE8',
             '\u0CE9',
             '\u0CEA',
             '\u0CEB',
             '\u0CEC',
             '\u0CED',
             '\u0CEE',
             '\u0CEF'
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
