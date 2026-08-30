"""NCA 死亡过程诊断 — 修复前基线"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from emergence_lab import NCA

nca = NCA(channels=16, fire_rate=0.5)
nca.init_grid(shape=(128, 128), seed_size=4)
alive_series = []
for step in range(1, 101):
    # 手动步进（借用 run 的内部逻辑，但逐帧打印）
    import numpy as np
    from scipy.ndimage import convolve
    grid = nca.grid.copy()
    alive = grid[:, :, 3] > 0.1
    if step % 10 == 0 or step == 1:
        alive_series.append(round(float(np.mean(alive)), 4))
    if step == 100:
        break
    # 跑一步
    import importlib
    # 简单方式：直接调用 run 前先复制 grid 状态
    break

# 用 run 跑全量
nca2 = NCA(channels=16, fire_rate=0.5)
nca2.init_grid(shape=(128, 128), seed_size=4)
r = nca2.run(steps=100, record_every=10, verbose=True)
print("\n=== 最终报告 ===")
for k, v in r.items():
    print(f"  {k}: {v}")
