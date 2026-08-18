# -*- coding: utf-8 -*-

from . import PreProcess as PP
from . import GeneralMap as GM

def ApplyPreProcessing(Strng,Source,Target):
    if Target == "PhagsPa":
        Options = ['PhagsPaArrange']
    else:
        Options = []

    #print('Getting preprocesssing ')

    for Option in Options:
        if Option.find(Target) != -1:
            Strng = GM.resolve(PP,Option,Strng,Source)
            #print (Strng)
        else:
            Strng = GM.resolve(PP,Option,Strng,Target)
            #print(Strng)

    return Strng
