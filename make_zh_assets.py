"""「知」主题素材生成：Lenia 混沌→结构演化
叙事：随机噪声（知道之前的混沌）→ 结构涌现（信息自己长出来）
输出：1920x1080 关键帧 PNG x5 + 慢速 GIF + 元数据 JSON
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

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'zh-assets')
os.makedirs(OUT, exist_ok=True)

# 16:9 网格
H, W = 540, 960
# 中文字体（Windows）
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
# 深底发光 colormap
cmap = LinearSegmentedColormap.from_list('zh_glow', ['#050510', '#0d1b3d', '#1e4d8c', '#3fa7d6', '#8be0ff', '#ffffff'])

def render(grid, path, title=None):
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)  # 1920x1080
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=1, interpolation='bilinear')
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.patch.set_facecolor('#050510')
    ax.set_facecolor('#050510')
    if title:
        ax.set_title(title, color='#8be0ff', fontsize=22, pad=12, fontfamily='serif')
    plt.tight_layout(pad=0)
    plt.savefig(path, dpi=100, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0)
    plt.close(fig)

# Lenia 演化
l = Lenia(R=20, mu=0.14, sigma=0.024)
l.init_grid(shape=(H, W), mode='random')

# 初始混沌帧（step 0）
KEY_FRAMES = {0: 'know_01_chaos', 50: 'know_02_seed', 150: 'know_03_emerge', 300: 'know_04_structure', 500: 'know_05_world'}
TITLES = {0: '混沌 · 知道之前', 50: '种子 · 第一条规则', 150: '涌现 · 结构自发', 300: '秩序 · 复杂生长', 500: '世界 · 稳定繁荣'}
gif_frames = []
render(np.array(l.grid), os.path.join(OUT, "know_01_chaos.png"), TITLES[0])
meta = {'params': {'R': 20, 'mu': 0.14, 'sigma': 0.024, 'grid': f'{H}x{W}'}, 'frames': [
    {'step': 0, 'name': 'know_01_chaos', 'alive': 1.0, 'score': round(EmergenceMetrics.full_report(np.array(l.grid))['emergence_score'],3)}]}
print(f"  step    0: know_01_chaos (初始混沌)")

for step in range(1, 501):
    l.run(steps=1, verbose=False)
    if step in KEY_FRAMES:
        grid_np = np.array(l.grid)
        render(grid_np, os.path.join(OUT, f"{KEY_FRAMES[step]}.png"), TITLES[step])
        r = EmergenceMetrics.full_report(grid_np)
        meta['frames'].append({'step': step, 'name': KEY_FRAMES[step], 'alive': round(r['alive'],3), 'score': round(r['emergence_score'],3)})
        print(f"  step {step:>4}: {KEY_FRAMES[step]} alive={r['alive']:.3f} score={r['emergence_score']:.3f}")
    if step % 25 == 0:
        gif_frames.append(np.array(l.grid))

# 慢速 GIF（25 帧）
import imageio.v2 as imageio
gif_frames = [ (frame * 255).astype(np.uint8) for frame in gif_frames ]
imageio.mimsave(os.path.join(OUT, 'zh_emergence.gif'), gif_frames, fps=5)

with open(os.path.join(OUT, 'metadata.json'), 'w', encoding='utf-8') as f:
    import json; json.dump(meta, f, ensure_ascii=False, indent=1)

print("\n=== 完成 ===")
print("输出目录:", OUT)
for f in sorted(os.listdir(OUT)):
    print(" ", f)
