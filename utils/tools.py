#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ahocorasick  # noqa

from settings import settings

def build():
    trie = ahocorasick.Automaton()
    for index, word in enumerate(settings.BLAKCLIST):
        trie.add_word(word, (index, word))
    trie.make_automaton()
    return trie


def check_blacklist(title, matcher):
    black_status = False
    for black_item in matcher.iter(title):
        if black_item:
            black_status = True
            continue
    return black_status
