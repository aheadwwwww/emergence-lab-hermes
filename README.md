# emergence-lab · Hermes 接管版

> 原仓库：https://github.com/aheadwwwww/emergence-lab（OpenClaw 遗留，2026-08-29 由 Hermes 接管）
> 探索笔记：见 [EXPLORATION.md](EXPLORATION.md) | 知识库：`D:/桌面/hermes的东西/knowledge-base/涌现实验.md`

## 本版相对原仓库的修复

1. **import 修复**：目录名 `emergence-lab` → `emergence_lab`（包名与目录名一致）
2. **NCA 复活**：存活保持 + 萌发生长 + 权重演化三刀，score 0.006 → 0.799（详见 EXPLORATION.md 第二节）
3. **可视化产物**：`output/` 三个 GIF（Lenia 涌现 / NCA 生长 / 信息素扩散）

## 快速开始

```bash
cd D:/桌面/hermes的东西/emergence-lab
python -m venv .venv
.venv/Scripts/pip install "numpy<2" scipy matplotlib imageio jax
# 运行示例（PYTHONPATH 指向包父目录）
PYTHONPATH="$(pwd -W)" .venv/Scripts/python emergence_lab/examples/example_lenia_basic.py
```

## 目录

```
emergence-lab/
├── emergence_lab/     # 修复后的包（models/core/experiments/examples/docs）
├── output/            # 三个涌现 GIF
├── EXPLORATION.md     # 探索笔记（解剖/修复/观察/边界回答）
├── diagnose_nca.py    # NCA 死亡诊断脚本（修复前基线）
└── make_gifs.py       # GIF 生成脚本
```

## 状态

- 状态：已修复、已跑通（三模型全部 structure）
- 原仓库：只读保留在 GitHub
