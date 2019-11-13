import json
from pathlib import Path
from sys import argv

import matplotlib.pyplot as plt
import numpy as np

# with (Path(__file__).parent.parent / 'teste-2019-11-06.json').open() as f:
with open(argv[1]) as f:
    noticias = json.load(f)

ocorrencias = {}

for noticia in noticias:
    for dis in noticia['diseases']:
        ocorrencias[dis] = ocorrencias.get(dis, 0) + 1

ocorrencias.pop('aids')

y_pos = np.arange(len(ocorrencias))

# Create bars
plt.bar(y_pos, ocorrencias.values())

# Create names on the x-axis
plt.xticks(y_pos, ocorrencias.keys())

# Show graphic
plt.show()
