import json
import re
import unicodedata
from pathlib import Path
from typing import List

diseases = [
    'catapora',
    'catapora',
    'conjuntivite',
    'dengue',
    'febre amarela',
    'gripe',
    'meningite',
    'rubéola',
    'sarampo',
    'sífilis',
    'zika',
]

DOUBLE_WS = re.compile(r'\s\s+')

with open(Path(__file__).parent / 'municipios.json') as f:
    cities = [
        {
            **c,
            're': re.compile(r'\b' + c['nome'] + r'\b'),
        }
        for c in json.load(f)
    ]


def extract_title(response):
    strs: List[str] = response.xpath('//h1/text()').extract()
    strs += response.xpath('//title/text()').extract()

    for s in strs:
        s = s.strip()
        if len(s) != 0:
            return s


def extract_content(response):
    c = ''.join(response.xpath('//p/text()').extract())
    c = DOUBLE_WS.sub('\n', c)
    return c.strip()


def extract_diseases(content):
    return [
        d
        for d in diseases
        if d in content.lower()
    ]


def extract_location(content):
    return [
        [c['nome'], c['codigo_uf']]
        for c in cities
        if c['re'].search(content) is not None
    ]


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii
