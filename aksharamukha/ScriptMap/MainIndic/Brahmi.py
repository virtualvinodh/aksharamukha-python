# -*- coding: utf-8 -*-

# Script Mapping for Devanagari

VowelMap =  [
            '𑀅',
            '𑀆',
            '𑀇',
            '𑀈',
            '𑀉',
            '𑀊',
            '𑀋',
            '𑀌',
            '𑀍',
            '𑀎',
            '𑀏',
            '𑀐',
            '𑀑',
            '𑀒',
            ]

SouthVowelMap = [
                '𑀏\u02BD',
                '𑀑\u02BD',
                ]

ModernVowelMap = [
                 '𑀏\u02BD',
                 '𑀆\u02BD',
                 ]

SinhalaVowelMap = [
                  '𑀏\u02BD'
                  ]

VowelSignMap =  [
                '𑀸',
                '𑀺',
                '𑀻',
                '𑀼',
                '𑀽',
                '𑀾',
                '𑀿',
                '𑁀',
                '𑁁',
                '𑁂',
                '𑁃',
                '𑁄',
                '𑁅',
                ]

SouthVowelSignMap = [
                    '𑁂\u02BD',
                    '𑁄\u02BD',
                    ]

ModernVowelSignMap =[
                    '𑁂\u02BD',
                    '𑀸\u02BD']

SinhalaVowelSignMap = [
                      '𑁂\u02BD'
                      ]

AyogavahaMap = [
               '𑀀',
               '𑀁',
               '𑀂'
               ]

ViramaMap =  [
             '𑁆'
             ]

ConsonantMap =  [
                '𑀓',
                '𑀔',
                '𑀕',
                '𑀖',
                '𑀗',

                '𑀘',
                '𑀙',
                '𑀚',
                '𑀛',
                '𑀜',

                '𑀝',
                '𑀞',
                '𑀟',
                '𑀠',
                '𑀡',

                '𑀢',
                '𑀣',
                '𑀤',
                '𑀥',
                '𑀦',

                '𑀧',
                '𑀨',
                '𑀩',
                '𑀪',
                '𑀫',

                '𑀬',
                '𑀭',
                '𑀮',
                '𑀯',

                '𑀰',
                '𑀱',
                '𑀲',
                '𑀳'
                ]

SouthConsonantMap = [
                    '𑀴',
                    '𑀴\u02BD',
                    '𑀭\u02BD',
                    '𑀦\u02BD'
                    ]

NuktaConsonantMap =  [
                    '𑀓\u02BD',
                    '𑀔\u02BD',
                    '𑀕\u02BD',
                    '𑀚\u02BD',
                    '𑀟\u02BD',
                    '𑀠\u02BD',
                    '𑀨\u02BD',
                    '𑀬\u02BD'
                     ]

SinhalaConsonantMap =[
                     '𑀀𑀕\u02BD',
                     '𑀀𑀚\u02BD',
                     '𑀀𑀟\u02BD',
                     '𑀀𑀤\u02BD',
                     '𑀀𑀩\u02BD',
                      ]

NuktaMap = [
           '\u02BD\u02BD\u02BD\u02BD'
           ]

OmMap = [
        '𑀑𑀁'
        ]

SignMap =[
         '\u02BD\u02BD',
         '𑁇',
         '𑁈'
         ]

Aytham =[AyogavahaMap[2]+'\u02BD']

NumeralMap = [
             '𑁦',
             '𑁧',
             '𑁨',
             '𑁩',
             '𑁪',
             '𑁫',
             '𑁬',
             '𑁭',
             '𑁮',
             '𑁯',
             ]

from ... import GeneralMap as GM

import os
GM.add_additional_chars(dict([(charlist, globals()[charlist]) for charlist in GM.CharmapLists]),
                        os.path.splitext(__file__)[0].split(os.path.sep)[-1])
