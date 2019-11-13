import json
from sys import argv

import matplotlib.pyplot as plt

regioes = {
    '1': 'Norte',
    '2': 'Nordeste',
    '3': 'Sudeste',
    '4': 'Sul',
    '5': 'Centro-Oeste',
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
    '3': {d: 0 for d in doencas},
    '4': {d: 0 for d in doencas},
    '5': {d: 0 for d in doencas},
}

with open(argv[1]) as f:
    noticias = json.load(f)

for noticia in noticias:
    for dis in noticia['diseases']:
        for loc in noticia['location']:
            reg = str(loc[1])[0]
            ocorrencias[reg][dis] += 1

# ocorrencias.pop('aids')
#
# y_pos = np.arange(len(ocorrencias))
#
# # Create bars
# plt.bar(y_pos, ocorrencias.values())
#
# # Create names on the x-axis
# plt.xticks(y_pos, ocorrencias.keys())
#
# # Show graphic
# plt.show()

# a = np.random.random((16, 16))

a = [
    n
    for (k, v) in ocorrencias.items()
    for (k2, n) in v.items()
]

plt.imshow(a, cmap='hot', interpolation='nearest')
plt.show()
