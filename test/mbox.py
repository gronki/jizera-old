#!/usr/bin/env python
# coding=utf8

hh_width = 80

def hh1(s):
    cor = ' '.join(list(s))
    mar = int((hh_width - 3 - len(cor)) * 0.5)
    bar = '+' + '-' * ( len(cor)+2*mar ) + '+'
    pad = ' ' * mar
    return '\n %s\n |%s%s%s|\n %s\n' % (bar,pad,cor,pad,bar)

def hh2(s):
    cor = ' '.join(list(s))
    mar = int((hh_width - 3 - len(cor)) * 0.5)
    bar = '=' * mar
    return '\n %s %s %s' % (bar,cor,bar)

def hh3(s):
    cor = ' '.join(list(s))
    mar = int((hh_width - 1 - 2*7 - len(cor)) * 0.5)
    bar = ' ' * mar
    return '\n %s- - -  %s  - - -%s' % (bar,cor,bar)
