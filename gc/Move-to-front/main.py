#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============
#      Date: 01.05.2017
#       Author: Chusovitin Anton Romanovich
# ==============

#https://rosettacode.org/wiki/Move-to-front_algorithm#Python:_Procedural

from __future__ import print_function
from string import ascii_lowercase
SYMBOLTABLE = list(chr(i) for i in range(0,1000))
#SYMBOLTABLE = ['0','1']#list(ascii_lowercase)
print(SYMBOLTABLE)

def move2front_encode(strng, symboltable):
    sequence, pad = [], symboltable[::]
    for char in strng:
        indx = pad.index(char)
        sequence.append(indx)
        pad = [pad.pop(indx)] + pad
    return sequence


def move2front_decode(sequence, symboltable):
    chars, pad = [], symboltable[::]
    for indx in sequence:
        char = pad[indx]
        chars.append(char)
        pad = [pad.pop(indx)] + pad
    return ''.join(chars)


if __name__ == '__main__':
    for s in ['01010101010101010', '111101000101011', '0101110101011010']:
        encode = move2front_encode(s, SYMBOLTABLE)
        print('%14r encodes to %r' % (s, encode), end=', ')
        print()
        #decode = move2front_decode(encode, SYMBOLTABLE)
        #print('which decodes back to %r' % decode)
        #assert s == decode, 'Whoops!'