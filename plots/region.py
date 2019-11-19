import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


regioes = {
    '1': 'Norte',
    '2': 'Nordeste',
    '3': 'Sudeste',
    '4': 'Sul',
    '5': 'Centro-Oeste',
}

with (Path(__file__).parent.parent / 'teste-2019-11-06.json').open() as f:
    noticias = json.load(f)

ocorrencias = {
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
}

for noticia in noticias:
    for loc in noticia['location']:
        state = str(loc[1])[0]
        ocorrencias[state] += 1

y_pos = np.arange(len(ocorrencias))

# Create bars
plt.bar(y_pos, ocorrencias.values())

# Create names on the x-axis
plt.xticks(y_pos, regioes.values())

# Show graphic
plt.show()
