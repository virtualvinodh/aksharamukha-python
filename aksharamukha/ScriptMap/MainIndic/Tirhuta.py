# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011481',
            '\U00011482',
            '\U00011483',
            '\U00011484',
            '\U00011485',
            '\U00011486',
            '\U00011487',
            '\U00011488',
            '\U00011489',
            '\U0001148A',
            '\U0001148B',
            '\U0001148C',
            '\U0001148D',
            '\U0001148E',
            ]

SouthVowelMap = [
                '\U00011481\U000114BA',
                '\U00011481\U000114BD',
                ]

ModernVowelMap = [
                 '\U0001148B\u02BD',
                 '\U00011482\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U0001148B\u02BD'
                  ]

VowelSignMap =  [
                '\U000114B0',
                '\U000114B1',
                '\U000114B2',
                '\U000114B3',
                '\U000114B4',
                '\U000114B5',
                '\U000114B6',
                '\U000114B7',
                '\U000114B8',
                '\U000114B9',
                '\U000114BB',
                '\U000114BC',
                '\U000114BE',
                ]

SouthVowelSignMap = [
                    '\U000114BA',
                    '\U000114BD',
                    ]

ModernVowelSignMap =[
                    '\U000114B9\u02BD',
                    '\U000114B0\u02BD'
                    ]

SinhalaVowelSignMap = [
                      '\U000114B9\u02BD'
                      ]

AyogavahaMap = [
               '\U000114BF',
               '\U000114C0',
               '\U000114C1'
               ]

ViramaMap =  [
             '\U000114C2'
             ]

ConsonantMap =  [
                '\U0001148F',
                '\U00011490',
                '\U00011491',
                '\U00011492',
                '\U00011493',

                '\U00011494',
                '\U00011495',
                '\U00011496',
                '\U00011497',
                '\U00011498',

                '\U00011499',
                '\U0001149A',
                '\U0001149B',
                '\U0001149C',
                '\U0001149D',

                '\U0001149E',
                '\U0001149F',
                '\U000114A0',
                '\U000114A1',
                '\U000114A2',

                '\U000114A3',
                '\U000114A4',
                '\U000114A5',
                '\U000114A6',
                '\U000114A7',

                '\U000114A8',
                '\U000114A9',
                '\U000114AA',
                '\U000114AB',

                '\U000114AC',
                '\U000114AD',
                '\U000114AE',
                '\U000114AF'
                ]

SouthConsonantMap = [
                    '𑒝𑓃',
                    '𑒭𑓃',
                    '𑒩\u02BD',
                    '𑒪𑓃'
                    ]

NuktaConsonantMap =  [
                     '\U0001148F\U000114C3',
                     '\U00011490\U000114C3',
                     '\U00011491\U000114C3',
                     '\U00011496\U000114C3',
                     '\U0001149B\U000114C3',
                     '\U0001149C\U000114C3',
                     '\U000114A4\U000114C3',
                     '\U000114A8\U000114C3'
                     ]

SinhalaConsonantMap =[
                     '\U000114BF𑒑\u02BD',
                     '\U000114BF𑒖\u02BD',
                     '\U000114BF𑒛\u02BD',
                     '\U000114BF𑒠\u02BD',
                     '\U000114BF𑒥\u02BD',
                      ]

NuktaMap = [
           '\U000114C3'
           ]

OmMap = [
        '𑓇'
        ]

SignMap =[
         '𑓄',
         '।',
         '॥'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '\U000114D0',
             '\U000114D1',
             '\U000114D2',
             '\U000114D3',
             '\U000114D4',
             '\U000114D5',
             '\U000114D6',
             '\U000114D7',
             '\U000114D8',
             '\U000114D9'
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
