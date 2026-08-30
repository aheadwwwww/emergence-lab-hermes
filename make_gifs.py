"""生成三模型涌现 GIF（验收证据）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from emergence_lab import Lenia, NCA, PheromoneCA
from emergence_lab.core.visualization import Visualizer

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(out, exist_ok=True)

# Lenia
lenia = Lenia(R=20, mu=0.14, sigma=0.024)
lenia.init_grid(shape=(192, 192), mode='random')
lenia.run(steps=240, record_every=12, verbose=False)
Visualizer.create_gif(lenia.history, os.path.join(out, 'lenia_emergence.gif'), fps=10)
print('Lenia GIF: %d frames' % len(lenia.history))

# NCA (修复版)
nca = NCA(channels=16, fire_rate=0.5)
nca.init_grid(shape=(96, 96), seed_size=6)
nca.run(steps=200, record_every=10, verbose=False)
hist = [(g[:, :, :4].max(axis=-1)) for g in nca.history]
Visualizer.create_gif(hist, os.path.join(out, 'nca_growth.gif'), fps=8)
print('NCA GIF: %d frames' % len(hist))

# PheromoneCA
pher = PheromoneCA(channels=3, R=12)
pher.init_grid(shape=(96, 96))
pher.run(steps=200, record_every=10, verbose=False)
phist = [g[0].max(axis=-1) if isinstance(g, tuple) else g for g in pher.history]
Visualizer.create_gif(phist, os.path.join(out, 'pheromone_diffusion.gif'), fps=8)
print('Pheromone GIF: %d frames' % len(phist))
print('DONE ->', out)
