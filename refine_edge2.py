"""NCA 边缘带细化：seed=2, K=0.01（弱保持），fire_rate 细网格
目标：精确定位混沌边缘带（涌现峰），收尾研究线
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from emergence_lab import Lenia
from emergence_lab.core.metrics import EmergenceMetrics
import numpy as np
from scipy.ndimage import convolve

OUT = os.path.dirname(os.path.abspath(__file__))

class NCA_K:
    def __init__(self, channels=16, fire_rate=0.5, keep_strength=0.01):
        self.channels = channels; self.fire_rate = fire_rate; self.keep_strength = keep_strength
        self.grid = None; self.history = []
    def init_grid(self, shape=(96, 96), seed_size=2):
        h, w = shape
        self.grid = np.zeros((h, w, self.channels), dtype=np.float32)
        cy, cx = h // 2, w // 2
        r = seed_size // 2
        self.grid[cy-r:cy+r, cx-r:cx+r, 3] = 1.0
        self.grid[cy-r:cy+r, cx-r:cx+r, :3] = 0.5
        rng = np.random.default_rng()
        sh, sw = max(2*r,1), max(2*r,1)
        self.grid[cy-r:cy+r, cx-r:cx+r, 4:] = rng.uniform(0.1, 0.3, (sh, sw, self.channels-4))
        self.history = [self.grid.copy()]
    def run(self, steps=100, verbose=False):
        sobel_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32)/8.0
        sobel_y = np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32)/8.0
        lap = np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float32)
        for i in range(steps):
            g = self.grid.copy()
            alive = g[:, :, 3] > 0.1
            pre = np.zeros_like(alive)
            for di in [-1,0,1]:
                for dj in [-1,0,1]:
                    pre |= np.roll(np.roll(alive, di, axis=0), dj, axis=1)
            p = []
            for c in range(self.channels):
                p += [convolve(g[:,:,c], sobel_x, mode='wrap'), convolve(g[:,:,c], sobel_y, mode='wrap'), convolve(g[:,:,c], lap, mode='wrap')]
            p = np.stack(p, axis=-1)
            rng = np.random.default_rng()
            if not hasattr(self, '_W'):
                self._W = rng.normal(0, 0.1, (3*self.channels, self.channels)).astype(np.float32)
                self._b = rng.uniform(-0.01, 0.01, self.channels).astype(np.float32)
            upd = 0.1 * np.tanh(p @ self._W + self._b)
            fire = rng.uniform(0, 1, g.shape[:2]) < self.fire_rate
            active = fire & pre
            self.grid = g + upd * active[..., None]
            dead = self.grid[:, :, 3] < 0.1
            self.grid[dead, :3] = 0
            alive_now = self.grid[:, :, 3] > 0.1
            self.grid[:, :, 3] = np.where(alive_now, self.grid[:, :, 3] + self.keep_strength*(1.0-self.grid[:,:,3]), self.grid[:,:,3])
            grow = pre & ~alive_now & fire
            self.grid[grow, 3] += 0.15
            self._W += rng.normal(0, 0.002, self._W.shape).astype(np.float32)
            self.grid = np.clip(self.grid, 0, 1)
        return EmergenceMetrics.full_report(self.grid[:, :, 3])

print("=== NCA 边缘带细化：seed=2, K=0.01, fire_rate 细网格（96x96, 100步）===")
print(f"{'fire':>6}{'alive':>8}{'ent':>6}{'edge':>7}{'score':>7}{'state':>10}")
print("-" * 50)
rows = []
for fr in [0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.30]:
    n = NCA_K(fire_rate=fr, keep_strength=0.01)
    n.init_grid(shape=(96, 96), seed_size=2)
    r = n.run(steps=100)
    rows.append((fr, r))
    print(f"{fr:>6.2f}{r['alive']:>8.3f}{r['entropy']:>6.2f}{r['edge_density']:>7.3f}{r['emergence_score']:>7.3f}{r['state']:>10}")

print("\n=== 分析 ===")
scores = [(fr, r['emergence_score']) for fr, r in rows]
peak = max(scores, key=lambda x: x[1])
band = [(fr, r['alive']) for fr, r in rows if 0.1 < r['alive'] < 0.9]
print(f"涌现峰: fire_rate={peak[0]:.2f}, score={peak[1]:.3f}")
print(f"半活带: fire_rate ∈ {[round(b[0],2) for b in band]}")

import json
with open(os.path.join(OUT, 'edge-refine2-raw.json'), 'w') as f:
    json.dump([{'fire_rate': fr, 'alive': r['alive'], 'entropy': r['entropy'], 'edge': r['edge_density'], 'score': r['emergence_score'], 'state': r['state']} for fr, r in rows], f, indent=1)
print("数据: edge-refine2-raw.json")
