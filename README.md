# adaptive-dev-loop

`adaptive-dev-loop` 是一个面向 Codex/AI 编程代理的研发流程 skill，用于把一个开发需求从需求接收推进到可交付代码。它强调先澄清、再分析、再实现，并通过自测和代码审查形成可追踪的闭环。

## 核心能力

- 需求澄清：使用 grilling 盘问式访谈明确目标、范围、边界和验收标准。
- 项目理解：编码前先阅读项目现状，记录技术栈、目录结构、既有规范和影响范围。
- 方案设计：在现有架构内制定修改方案，列出风险、取舍和验证方式。
- 任务拆分：把方案拆成可独立验证的小任务，并持续记录执行状态。
- 编码与验证：完成代码修改后运行构建、测试和 lint，并记录客观结果。
- 自适应循环：当自测或审查发现问题时，按根因回流到需求、方案、任务或编码阶段。

## 工作流程

| 阶段 | 产物 |
|------|------|
| 需求接受 | `dev-loop/YYYY-MM-DD/<需求短名>/loop.md` |
| 需求澄清 | `loop.md` 中确认后的需求理解与验收标准 |
| 理解项目与影响分析 | `loop.md`，复杂时拆 `analysis.md` |
| 修改方案设计 | `loop.md` 中的方案、风险和验证章节 |
| 任务拆分 | `loop.md` 中的任务表 |
| 编码实现 | 项目代码修改与任务状态更新 |
| 自测 | `loop.md` 中的测试和构建结果，失败回流时拆 `iteration-log.md` |
| 代码审查 | `loop.md` 中的审查记录 |
| 交付汇报 | `loop.md` 的交付报告章节 |

## 仓库结构

```text
.
├── SKILL.md
└── references/
    ├── analysis-template.md
    ├── boundaries.md
    ├── final-report-template.md
    ├── grilling.md
    ├── iteration-log-template.md
    ├── loop-template.md
    ├── readme-template.md
    ├── review-checklist.md
    └── tasks-template.md
```

## 关键规则

- 所有阶段都要生成可检查的 Markdown 产物，默认放在 `dev-loop/YYYY-MM-DD/<需求短名>/loop.md`。
- 需求澄清和修改方案设计必须经过 grilling 和用户确认；若用户明确授权按推荐自动推进，也必须记录候选方案、推荐项、验收标准和授权依据。
- 自测或审查失败时，不做静默降级，不通过跳过测试、吞异常或改断言伪装通过。
- 触达迭代上限或同一问题反复出现时，停止自动尝试并升级给用户决策。
- 编码前必须阅读 `references/boundaries.md`，明确哪些操作可以直接做、哪些需要先确认。

## 使用方式

将本仓库作为 Codex skill 安装或挂载后，通过显式唤醒使用：

```text
/adaptive-dev-loop 给订单模块增加批量导出功能
```

skill 会根据 `SKILL.md` 中定义的流程推进，默认生成单个 `loop.md`；复杂分析、失败回流或完整审计模式才使用 `references/` 下的拆分模板。自检优先运行 `python scripts/structure_check.py`。
