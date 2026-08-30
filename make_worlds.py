"""「知」主题·多世界素材：同一混沌，不同规则 → 不同世界
对照实验叙事：同样的信息（混沌起点），不同的判断（规则参数），产生不同的世界
输出：4 世界代表帧 + 四联对比图 + 元数据
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from emergence_lab import Lenia
from emergence_lab.core.metrics import EmergenceMetrics

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'zh-assets', 'worlds')
os.makedirs(OUT, exist_ok=True)

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
cmap = LinearSegmentedColormap.from_list('zh_glow', ['#050510', '#0d1b3d', '#1e4d8c', '#3fa7d6', '#8be0ff', '#ffffff'])

H, W = 540, 960
SEED = 42  # 固定混沌起点

def seeded_init(lenia, seed):
    """固定种子的 init_grid（复制原逻辑，保证所有世界同一混沌起点）"""
    h, w = lenia.grid.shape if lenia.grid is not None else (H, W)
    h, w = H, W
    lenia._make_kernel((h, w))
    rng = np.random.default_rng(seed)
    grid = rng.uniform(0, 0.2, (h, w)).astype(np.float32)
    cy, cx = h // 2, w // 2
    r = min(h, w) // 6
    blob = rng.uniform(0.2, 0.6, (2*r+1, 2*r+1))
    grid[cy-r:cy+r+1, cx-r:cx+r+1] = blob
    lenia.grid = grid
    lenia.history = [grid.copy()]

def render(grid, path, title=None):
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=1, interpolation='bilinear')
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.patch.set_facecolor('#050510'); ax.set_facecolor('#050510')
    if title:
        ax.set_title(title, color='#8be0ff', fontsize=24, pad=12, fontfamily='sans-serif')
    plt.tight_layout(pad=0)
    plt.savefig(path, dpi=100, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0)
    plt.close(fig)

# 四组"基因"（经典 Lenia 生物参数）
WORLDS = [
    {'name': 'orbium', 'params': (13, 0.15, 0.014), 'title': '世界一 · 生命体', 'note': 'Orbium · 自我维持的有机体'},
    {'name': 'hydro', 'params': (14, 0.26, 0.036), 'title': '世界二 · 分裂者', 'note': 'Hydrogeminium · 生长与分裂'},
    {'name': 'gyro', 'params': (14, 0.175, 0.027), 'title': '世界三 · 旋转者', 'note': 'Gyroginium · 循环与秩序'},
    {'name': 'smooth', 'params': (10, 0.267, 0.045), 'title': '世界四 · 平滑域', 'note': 'Smooth Life · 流体的秩序'},
]

meta = {'seed': SEED, 'grid': f'{H}x{W}', 'worlds': []}

for w in WORLDS:
    R, mu, sigma = w['params']
    l = Lenia(R=R, mu=mu, sigma=sigma)
    seeded_init(l, SEED)
    for _ in range(300):
        l.run(steps=1, verbose=False)
    grid_np = np.array(l.grid)
    render(grid_np, os.path.join(OUT, f"world_{w['name']}.png"), w['title'])
    r = EmergenceMetrics.full_report(grid_np)
    meta['worlds'].append({'name': w['name'], 'params': w['params'], 'alive': round(r['alive'],3),
                           'entropy': round(r['entropy'],2), 'score': round(r['emergence_score'],3), 'note': w['note']})
    print(f"  {w['name']:<8} R={R} mu={mu} sigma={sigma} | alive={r['alive']:.3f} entropy={r['entropy']:.2f} score={r['emergence_score']:.3f}")

# 四联对比图（1920x1080）
fig, axes = plt.subplots(2, 2, figsize=(19.2, 10.8), dpi=100)
fig.patch.set_facecolor('#050510')
for ax, w in zip(axes.flat, WORLDS):
    img = plt.imread(os.path.join(OUT, f"world_{w['name']}.png"))
    ax.imshow(img)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(w['title'], color='#8be0ff', fontsize=20, pad=8, fontfamily='sans-serif')
plt.tight_layout(pad=0.3)
plt.savefig(os.path.join(OUT, 'worlds_quad.png'), dpi=100, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0)
plt.close(fig)

import json
with open(os.path.join(OUT, 'metadata.json'), 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=1)

print("\n=== 完成 ===")
print("输出:", OUT)
for f in sorted(os.listdir(OUT)):
    print(" ", f)
