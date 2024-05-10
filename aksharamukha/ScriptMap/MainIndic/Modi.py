# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011600',
            '\U00011601',
            '\U00011602',
            '\U00011603',
            '\U00011604',
            '\U00011605',
            '\U00011606',
            '\U00011607',
            '\U00011608',
            '\U00011609',
            '\U0001160A',
            '\U0001160B',
            '\U0001160C',
            '\U0001160D',
            ]

SouthVowelMap = [
                '\U0001160A\u02BD',
                '\U0001160C\u02BD',
                ]

ModernVowelMap = [
                 '\U00011600\U00011640',
                 '\U00011601\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U0001160A\u02BD'
                  ]

VowelSignMap =  [
                '\U00011630',
                '\U00011631',
                '\U00011632',
                '\U00011633',
                '\U00011634',
                '\U00011635',
                '\U00011636',
                '\U00011637',
                '\U00011638',
                '\U00011639',
                '\U0001163A',
                '\U0001163B',
                '\U0001163C',
                ]

SouthVowelSignMap = [
                    '\U00011639\u02BD',
                    '\U0001163B\u02BD',
                    ]

ModernVowelSignMap =[
                    '\U00011640',
                    '\U00011630\u02BD'
                    ]

SinhalaVowelSignMap = [
                      '\U00011639\u02BD'
                      ]

AyogavahaMap = [
               '\U0001163D\u02BD',
               '\U0001163D',
               '\U0001163E'
               ]

ViramaMap =  [
             '\U0001163F'
             ]

ConsonantMap =  [
                '\U0001160E',
                '\U0001160F',
                '\U00011610',
                '\U00011611',
                '\U00011612',

                '\U00011613',
                '\U00011614',
                '\U00011615',
                '\U00011616',
                '\U00011617',

                '\U00011618',
                '\U00011619',
                '\U0001161A',
                '\U0001161B',
                '\U0001161C',

                '\U0001161D',
                '\U0001161E',
                '\U0001161F',
                '\U00011620',
                '\U00011621',

                '\U00011622',
                '\U00011623',
                '\U00011624',
                '\U00011625',
                '\U00011626',

                '\U00011627',
                '\U00011628',
                '\U00011629',
                '\U0001162A',

                '\U0001162B',
                '\U0001162C',
                '\U0001162D',
                '\U0001162E'
                ]

SouthConsonantMap = [
                    '\U0001162F',
                    '\U0001162F\u02BD',
                    '\U0001162C\u02BD',
                    '\U00011621\u02BD'
                    ]

NuktaConsonantMap =  [
                     '\U0001160E\u02BD',
                     '\U0001160F\u02BD',
                     '\U00011610\u02BD',
                     '\U00011615\u02BD',
                     '\U0001161A\u02BD',
                     '\U0001161B\u02BD',
                     '\U00011623\u02BD',
                     '\U00011627\u02BD'
                     ]

SinhalaConsonantMap =[
                     '\U0001163D𑘐\u02BD',
                     '\U0001163D𑘕\u02BD',
                     '\U0001163D𑘚\u02BD',
                     '\U0001163D𑘟\u02BD',
                     '\U0001163D𑘤\u02BD',
                      ]

NuktaMap = [
           '\u02BD\u02BD\u02BD\u02BD'
           ]

OmMap = [
        '𑘌𑘽'
        ]

SignMap =[
         '\u093D',
         '\U00011641',
         '\U00011642'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '\U00011650',
             '\U00011651',
             '\U00011652',
             '\U00011653',
             '\U00011654',
             '\U00011655',
             '\U00011656',
             '\U00011657',
             '\U00011658',
             '\U00011659'
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
