import json
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

regioes = {
    '1': 'Norte',
    '2': 'Nordeste',
    '5': 'Centro-Oeste',
    '3': 'Sudeste',
    '4': 'Sul',
}

doencas = [
    'aids',
    'catapora',
    'conjuntivite',
    'dengue',
    'febre amarela',
    'gripe',
    'meningite',
    'sarampo',
    'sífilis',
    'zika',
]

ocorrencias = {
    '1': {d: 0 for d in doencas},
    '2': {d: 0 for d in doencas},
    '5': {d: 0 for d in doencas},
    '3': {d: 0 for d in doencas},
    '4': {d: 0 for d in doencas},
}

with open(argv[1]) as f:
    noticias = json.load(f)

for noticia in noticias:
    for dis in noticia['diseases']:
        for loc in noticia['location']:
            reg = str(loc[1])[0]
            ocorrencias[reg][dis] += 1


x_pos = np.arange(len(doencas))
y_pos = np.arange(len(regioes))

plt.xticks(x_pos, doencas, rotation=45)
plt.yticks(y_pos, regioes.values())

data = np.array([
    [n for (k2, n) in v.items()]
    for (k, v) in ocorrencias.items()
])

im = plt.imshow(data, cmap='Blues', interpolation='nearest')

valfmt = matplotlib.ticker.StrMethodFormatter('{x}')

textcolors = ["black", "white"]
threshold = im.norm(data.max()) / 2.

kw = dict(horizontalalignment="center",
          verticalalignment="center")

texts = []
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
        text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
        texts.append(text)

print(ocorrencias)

plt.show()
