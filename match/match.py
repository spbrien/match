# -*- coding: utf-8 -*-

"""Main module."""

from fuzzywuzzy import fuzz, process

from utils import uniq


def match_partial_strings(str1, str2, threshold=90):
    ratio = fuzz.partial_ratio(str1, str2)
    if ratio >= threshold:
        return True
    else:
        return False


def match_full_strings(str1, str2, threshold=90):
    ratio = fuzz.ratio(str1, str2)
    if ratio >= threshold:
        return True
    else:
        return False


def extract_matches_from_list(s, l, limit=50, threshold=90):
    return [
        i for i in process.extract(
            s,
            l,
            limit=limit,
            scorer=fuzz.partial_ratio
        ) if i[1] > threshold
    ]

def get_replacement_name(item):
    if len(item['matches']) == 0:
        return None

    perfect_match = next(
        iter(
            [
                i[0] for i in item['matches']
                if i[1]
            ] or []
        ), None
    )

    if perfect_match:
        return perfect_match

    return None

def match_factory(list_to_check_against, list_to_check=None, threshold=90):

    def find_match(items):
        match_check = [{
            'name': item,
            'matches': extract_matches_from_list(
                item,
                list_to_check_against,
                threshold=threshold
            )
        } for item in uniq(items)]

        process_easy_replacements = [
            {
                'matches': item['matches'],
                'name': item['name'],
                'replacement_name': get_replacement_name(item)
            } for item in uniq(match_check)
        ]

        return {
            'matched': [
                i for i in process_easy_replacements
                if i['replacement_name'] and len(i['matches']) > 0
            ],
            'unmatched': [
                i for i in process_easy_replacements
                if not i['replacement_name'] and len(i['matches']) > 0
            ],
            'new': [
                i for i in process_easy_replacements
                if not i['replacement_name'] and len(i['matches']) == 0
            ],
        }

    return find_match(list_to_check) if list_to_check else find_match
