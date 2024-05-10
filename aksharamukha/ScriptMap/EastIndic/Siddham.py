# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '\U00011580',
            '\U00011581',
            '\U00011582',
            '\U00011583',
            '\U00011584',
            '\U00011585',
            '\U00011586',
            '\U00011587',
            '\U00011588',
            '\U00011589',
            '\U0001158A',
            '\U0001158B',
            '\U0001158C',
            '\U0001158D'
            ]

SouthVowelMap = [
                '\U0001158A\u02BD',
                '\U0001158C\u02BD',
                ]

ModernVowelMap = [
                 '\U0001158A\u02BD',
                 '\U00011581\u02BD',
                 ]

SinhalaVowelMap = [
                  '\U0001158A\u02BD'
                  ]

VowelSignMap =  [
                '\U000115AF',
                '\U000115B0',
                '\U000115B1',
                '\U000115B2',
                '\U000115B3',
                '\U000115B4',
                '\U000115B5',
                '𑖿𑖩𑖰\u02BD',
                '𑖿𑖩𑖱\u02BD',
                '\U000115B8',
                '\U000115B9',
                '\U000115BA',
                '\U000115BB',
                ]

SouthVowelSignMap = [
                    '\U000115B8\u02BD',
                    '\U000115BA\u02BD',
                    ]

ModernVowelSignMap =[
                    '\U000115B8\u02BD',
                    '\U000115AF\u02BD'
                    ]

SinhalaVowelSignMap = [
                    '\U000115B8\u02BD',
                      ]

AyogavahaMap = [
               '\U000115BC',
               '\U000115BD',
               '\U000115BE'
               ]

ViramaMap =  [
             '\U000115BF'
             ]

ConsonantMap =  [
                '\U0001158E',
                '\U0001158F',
                '\U00011590',
                '\U00011591',
                '\U00011592',

                '\U00011593',
                '\U00011594',
                '\U00011595',
                '\U00011596',
                '\U00011597',

                '\U00011598',
                '\U00011599',
                '\U0001159A',
                '\U0001159B',
                '\U0001159C',

                '\U0001159D',
                '\U0001159E',
                '\U0001159F',
                '\U000115A0',
                '\U000115A1',

                '\U000115A2',
                '\U000115A3',
                '\U000115A4',
                '\U000115A5',
                '\U000115A6',

                '\U000115A7',
                '\U000115A8',
                '\U000115A9',
                '\U000115AA',

                '\U000115AB',
                '\U000115AC',
                '\U000115AD',
                '\U000115AE'
                ]

SouthConsonantMap = [
                    '𑖩𑗀',
                    '𑖬𑗀',
                    '𑖨𑗀',
                    '𑖡𑗀'
                    ]

NuktaConsonantMap =  [
                     '𑖎𑗀',
                     '𑖏𑗀',
                     '𑖐𑗀',
                     '𑖕𑗀',
                     '𑖚𑗀',
                     '𑖛𑗀',
                     '𑖣𑗀',
                     '𑖧𑗀'
                     ]

SinhalaConsonantMap =[
                     '\U000115BC\u02BD\U00011590',
                     '\U000115BC\u02BD\U00011595',
                     '\U000115BC\u02BD\U0001159A',
                     '\U000115BC\u02BD\U0001159F',
                     '\U000115BC\u02BD\U000115A4',
                      ]

NuktaMap = [
           '\U000115C0'
           ]

OmMap = [
        '𑖌𑖼'
        ]

SignMap =[
         '\u02BD\u02BD',
         '\U000115C2',
         '\U000115C3'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '0',
             '1',
             '2',
             '3',
             '4',
             '5',
             '6',
             '7',
             '8',
             '9'
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
