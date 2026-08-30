"""涌现式游戏内容生成器：随机 Lenia 参数 = 物种基因
扫描 60 组随机参数，收集存活物种（alive>0.05），生成物种图鉴
示范：程序化生成（PCG）——同一混沌，不同规则 = 不同生物/世界
"""
import sys, os
import numpy as np
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from emergence_lab import Lenia
from emergence_lab.core.metrics import EmergenceMetrics

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'creatures')
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(7)  # 固定种子，可复现
SPECIES = []

# 物种命名（按表现分类）
def name_species(alive, entropy, edge):
    if alive < 0.05: return '灭绝种'
    if entropy > 3.5 and edge > 0.3: return '文明种'   # 高复杂度
    if entropy > 3.0: return '繁盛种'
    if alive > 0.6: return '广布种'
    return '边缘种'

for i in range(60):
    R = int(rng.integers(8, 22))
    mu = round(rng.uniform(0.08, 0.28), 4)
    sigma = round(rng.uniform(0.008, 0.05), 4)
    l = Lenia(R=R, mu=mu, sigma=sigma)
    l.init_grid(shape=(96, 96), mode='random')
    r = l.run(steps=120, verbose=False)
    r['R'] = R; r['mu'] = mu; r['sigma'] = sigma
    r['kind'] = name_species(r['alive'], r['entropy'], r['edge_density'])
    SPECIES.append(r)

# 按涌现分排序
SPECIES.sort(key=lambda s: s['emergence_score'], reverse=True)

print("=== 物种图鉴（60 组随机基因，存活 + 评分）===")
print(f"{'#':>3} {'物种':<6}{'R':>4}{'mu':>7}{'sigma':>7}{'alive':>7}{'ent':>6}{'score':>7}{'state':>10}")
print("-" * 62)
alive_count = 0
for i, s in enumerate(SPECIES, 1):
    mark = '★' if s['kind'] in ('文明种', '繁盛种') else ' '
    if s['alive'] > 0.05: alive_count += 1
    print(f"{i:>3} {mark}{s['kind']:<5}{s['R']:>4}{s['mu']:>7.3f}{s['sigma']:>7.3f}{s['alive']:>7.3f}{s['entropy']:>6.2f}{s['emergence_score']:>7.3f}{s['state']:>10}")

print(f"\n存活物种: {alive_count}/60 | 灭绝: {60-alive_count} | 文明/繁盛种: {sum(1 for s in SPECIES if s['kind'] in ('文明种','繁盛种'))}")

# 保存图鉴
gallery = [{'rank': i, 'kind': s['kind'], 'R': s['R'], 'mu': s['mu'], 'sigma': s['sigma'],
            'alive': round(s['alive'],3), 'entropy': round(s['entropy'],2), 'score': round(s['emergence_score'],3)} for i, s in enumerate(SPECIES, 1)]
with open(os.path.join(OUT, 'creature-gallery.json'), 'w', encoding='utf-8') as f:
    json.dump({'note': '同一混沌(随机初始化) + 不同规则 = 不同物种', 'species': gallery}, f, ensure_ascii=False, indent=1)
print(f"\n图鉴已保存: {OUT}/creature-gallery.json")
