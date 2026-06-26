#!/usr/bin/env bash
# 结构 + 保护区不变量回归测试。
# 用途：自我进化（步骤 9）改动 skill 自身后自动运行；自检失败应立即回滚。
# 退出码：0 = 全部通过，1 = 有失败项，2 = 无法定位 skill 根目录。
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 2
cd "$ROOT" || exit 2
[ -f SKILL.md ] || { echo "找不到 SKILL.md，ROOT=$ROOT"; exit 2; }

pass=0; fail=0
ok(){ echo "  ✅ $1"; pass=$((pass+1)); }
no(){ echo "  ❌ $1"; fail=$((fail+1)); }

echo "【1】frontmatter 必填字段"
grep -qE '^name:' SKILL.md && ok "name" || no "缺 name"
grep -qE '^description:' SKILL.md && ok "description" || no "缺 description（保护区：触发语义）"

echo "【2】引用完整性（无死链）"
U="$(mktemp)"; A="$(mktemp)"
grep -oE 'references/[A-Za-z0-9_-]+\.md' SKILL.md | sort -u > "$U"
find references -name '*.md' -printf 'references/%f\n' 2>/dev/null | sort > "$A"
dead="$(comm -23 "$U" "$A")"
[ -z "$dead" ] && ok "无死链" || no "死链: $dead"
orphan="$(comm -13 "$U" "$A")"
[ -z "$orphan" ] && ok "无孤儿文件" || no "孤儿: $orphan"
rm -f "$U" "$A"

echo "【3】闭环阶段（保护区：8 阶段不可缺）"
for s in "步骤 1" "步骤 2" "步骤 3" "步骤 4" "步骤 5" "步骤 6" "步骤 7" "步骤 8"; do
  grep -q "$s" SKILL.md && ok "$s" || no "缺 $s"
done
grep -q "自适应循环" SKILL.md && ok "自适应循环" || no "缺 自适应循环"
grep -q "迭代上限" SKILL.md && ok "终止条件(迭代上限)" || no "缺 终止条件"
grep -q "收敛" SKILL.md && ok "收敛判据" || no "缺 收敛判据"

echo "【4】产物模板齐全"
for t in readme analysis tasks iteration-log final-report; do
  [ -f "references/${t}-template.md" ] && ok "${t}-template.md" || no "缺 ${t}-template.md"
done

echo "【5】保护区不变量（自我进化禁止破坏）"
grep -q "步骤 9" SKILL.md && ok "步骤 9 进化环节存在" || no "缺 步骤 9"
[ -f references/evolution.md ] && ok "evolution.md 存在" || no "缺 evolution.md"
grep -q "审批门" references/evolution.md 2>/dev/null && ok "审批门(改前询问用户)存在" || no "缺 审批门"
grep -q "回滚" references/evolution.md 2>/dev/null && ok "回滚机制存在" || no "缺 回滚"
grep -q "保护区" references/evolution.md 2>/dev/null && ok "保护区定义存在" || no "缺 保护区"
grep -q "绝不做" references/boundaries.md 2>/dev/null && ok "边界'绝不做'存在" || no "缺 边界'绝不做'"
grep -q "掩盖" references/boundaries.md 2>/dev/null && ok "禁止伪装通过 存在" || no "缺 禁止伪装通过"

echo ""
echo "===== structure-check: PASS=$pass FAIL=$fail ====="
[ "$fail" -eq 0 ] && exit 0 || exit 1
