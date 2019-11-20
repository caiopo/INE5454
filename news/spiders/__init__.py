from datetime import datetime

import scrapy

from urllib.parse import urlparse

from news.extractors import extract_content, extract_diseases, extract_location, extract_title
from news.items import NewsItem

DEPTH_THRESHOLD = 7


class NewsSpider(scrapy.Spider):
    name = 'newsbot'

    start_urls = [
        'https://g1.globo.com/sp/santos-regiao/noticia/2019/10/11/'
        'macaco-morto-com-suspeita-de-febre-amarela-e-encontrado-em-eldorado-sp.ghtml',
        'https://g1.globo.com/mundo/noticia/2019/10/28/'
        'cidade-do-paquistao-registra-900-casos-de-criancas-com-hiv-pediatra-e-acusado-de-reutilizar-seringas.ghtml',
        'https://g1.globo.com/sp/bauru-marilia/noticia/2019/10/29/'
        'hospital-referencia-no-tratamento-de-cancer-retoma-atendimentos-apos-suspeita-de-sarampo-em-funcionarios.ghtml',
        'https://noticias.uol.com.br/internacional/ultimas-noticias/2019/10/28/'
        'paquistao-criancas-hiv-agulha.htm',
        'https://noticias.uol.com.br/ultimas-noticias/agencia-estado/2019/07/22/'
        'casos-de-sarampo-ja-causam-internacao-e-alerta-em-cidades-do-interior-paulista.htm',
        'https://noticias.uol.com.br/saude/ultimas-noticias/redacao/2018/02/14/'
        'mais-de-200-pessoas-sao-diagnosticadas-com-dsts-no-carnaval-de-salvador.htm',
        'https://www.terra.com.br/vida-e-estilo/saude/'
        'mortes-por-meningite-antes-do-inverno-poem-em-alerta-cidades-paulistas,c99a597c3bf700276342b99a71b809f028zly97q.html',
        'https://www.terra.com.br/vida-e-estilo/saude/'
        'numero-de-casos-de-sarampo-sobe-para-633-em-sao-paulo,a40c662473509d672c4d8a9306650aafc2nqi9g7.html',
        'https://www.terra.com.br/vida-e-estilo/minha-vida/'
        'numero-de-casos-positivos-para-sifilis-crescem-no-carnaval-de-salvador,ba1c881bbe26498e628b96c8013b497dnp0uxkpr.html',
    ]

    def parse(self, response, depth=0):
        content = extract_content(response)
        diseases = extract_diseases(content)

        if diseases:
            yield NewsItem(
                title=extract_title(response),
                diseases=diseases,
                location=extract_location(content),
                retrieved_datetime=datetime.now(),
                depth=depth,
                url=response.request.url,
                content=content,
            )

        yield from self.get_links(response, bool(diseases), depth)

    def get_links(self, response, found, depth):
        if depth < DEPTH_THRESHOLD:
            next_depth = 0 if found else depth + 1
            for a in response.xpath('//a/@href'):
                url = a.get()
                if valid_url(url):
                    yield response.follow(url, self.parse, cb_kwargs={'depth': next_depth})


domains = ['twitter', '']
extensions = ['.jpg', '.png']


def valid_url(url: str):
    url = urlparse(url)

    not_forbidden = not any(d in url.netloc for d in domains)
    not_photo = not any(url.path.endswith(e) for e in extensions)
    http = url.scheme.startswith('http')

    return not_photo and http and not_forbidden
