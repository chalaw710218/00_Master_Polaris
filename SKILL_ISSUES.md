# 🚨 極星宇宙全內閣技能架構與格式規範檢核報告 (SKILL ISSUES)

> ⚠️ **本檔由 `skill_scanner.py` 自動產生，請勿手改**  
> 執行者：**執行長 雪 (Yuki)** ｜ 依據：《00-00 極星格式規範 v1.0》  
> 掃描檔案總數：現役 **174** 份（已排除鏡像 **448** 份、封存 **53** 份）

---

## 🎯 格式規範合規總覽 (Format Standard Compliance Summary)

- **完全合規技能數（0 錯誤 0 提醒）**：**32** / **174** (18.4%)
- **無嚴重錯誤技能數（0 錯誤，含過渡提醒）**：**32** / **174** (18.4%)

### 📋 規則違規統計清冊

| 規則代號 | 規範項目 | 嚴重度 | 違反數量 | 處置方向 |
| :--- | :--- | :---: | :---: | :--- |
| **E1** | 缺少 name 或 description | ❌ 錯誤 | `0` 份 | 補齊 Frontmatter 必填欄位 |
| **E2** | name 格式非法（只能小寫/數字/連字號，<=64字） | ❌ 錯誤 | `0` 份 | 重新命名為小寫連字號格式 |
| **E3** | name 與所在資料夾名稱不一致 | ❌ 錯誤 | `1` 份 | 校正 name 使其與資料夾完全一致 |
| **E4** | description 超過 1024 字元 | ❌ 錯誤 | `0` 份 | 簡化描述至精簡字數 |
| **E5** | metadata.status 非 active/draft/archived | ❌ 錯誤 | `142` 份 | 正確設定狀態標籤 |
| **E6** | active 技能缺少 evidence 憑證或檔案不存在 | ❌ 錯誤 | `0` 份 | 補齊測試程式或降回 draft |
| **E7** | atom-* 技能缺少 metadata.group 或 parent | ❌ 錯誤 | `109` 份 | 於 metadata 補齊組別與母體標籤 |
| **E8** | 舊版 SKILL_*.md 滯留於非封存目錄 | ❌ 錯誤 | `0` 份 | 移入同層之 `_archive/` 目錄 |
| **E9** | 資料檔非 UTF-8 編碼 (.md/.txt/.json/.py) | ❌ 錯誤 | `0` 份 | 轉換為標準 UTF-8 編碼 |
| **W1** | description 超過 200 字（建議精簡） | ⚠️ 提醒 | `84` 份 | 精簡為做什麼/何時用/何時不用 |
| **W2** | 缺少 metadata.owner 或 metadata.version | ⚠️ 提醒 | `142` 份 | 補齊負責閣員與版本標籤 |
| **W3** | frontmatter 存在自訂欄位未收入 metadata | ⚠️ 提醒 | `40` 份 | 將自訂鍵搬入 metadata 底下 |
| **W4** | SKILL.md 內文超過 500 行 | ⚠️ 提醒 | `2` 份 | 將理論背景拆分至 references/ |
| **W5** | 工作資料夾存在殘留檔案 (.bak/.pyc/__pycache__) | ⚠️ 提醒 | `18` 處 | 執行清理或封存 |

---

## ❌ 一、技能檔嚴格違規清冊 (Skill Errors)

### 📄 [.agents/skills/atom-abacus-ice-friction-stripper/SKILL.md](.agents/skills/atom-abacus-ice-friction-stripper/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-abacus-macro-compound-learner/SKILL.md](.agents/skills/atom-abacus-macro-compound-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-abacus-munger-inversion-veto/SKILL.md](.agents/skills/atom-abacus-munger-inversion-veto/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-abacus-munger-vision-moat/SKILL.md](.agents/skills/atom-abacus-munger-vision-moat/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-abacus-negative-float-cashflow/SKILL.md](.agents/skills/atom-abacus-negative-float-cashflow/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-abacus-survival-reservoir-opex/SKILL.md](.agents/skills/atom-abacus-survival-reservoir-opex/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-ada-agentic-paradigm-researcher/SKILL.md](.agents/skills/atom-ada-agentic-paradigm-researcher/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-ada-efficient-inference-scout/SKILL.md](.agents/skills/atom-ada-efficient-inference-scout/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-ada-frontier-paper-evaluator/SKILL.md](.agents/skills/atom-ada-frontier-paper-evaluator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-ada-research-dossier-evolver/SKILL.md](.agents/skills/atom-ada-research-dossier-evolver/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-deming-andon-gatekeeper/SKILL.md](.agents/skills/atom-deming-andon-gatekeeper/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-deming-joy-flow-allocator/SKILL.md](.agents/skills/atom-deming-joy-flow-allocator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-deming-poka-yoke-engineer/SKILL.md](.agents/skills/atom-deming-poka-yoke-engineer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-deming-quality-sopk-learner/SKILL.md](.agents/skills/atom-deming-quality-sopk-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-deming-sopk-attribution/SKILL.md](.agents/skills/atom-deming-sopk-attribution/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-falcon-legal-vault-decadal-evolver/SKILL.md](.agents/skills/atom-falcon-legal-vault-decadal-evolver/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-falcon-precedent-caselaw-analyst/SKILL.md](.agents/skills/atom-falcon-precedent-caselaw-analyst/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-falcon-regulatory-moat-architect/SKILL.md](.agents/skills/atom-falcon-regulatory-moat-architect/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-falcon-statute-legislative-learner/SKILL.md](.agents/skills/atom-falcon-statute-legislative-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-josef-data-diagram-artisan/SKILL.md](.agents/skills/atom-josef-data-diagram-artisan/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-josef-info-hierarchy-visualizer/SKILL.md](.agents/skills/atom-josef-info-hierarchy-visualizer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-josef-senior-accessibility-visuals/SKILL.md](.agents/skills/atom-josef-senior-accessibility-visuals/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-josef-typography-optical-engine/SKILL.md](.agents/skills/atom-josef-typography-optical-engine/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-josef-visual-aesthetics-learner/SKILL.md](.agents/skills/atom-josef-visual-aesthetics-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-kage-decadal-audit-evolver/SKILL.md](.agents/skills/atom-kage-decadal-audit-evolver/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-kage-learning-clutch-judge/SKILL.md](.agents/skills/atom-kage-learning-clutch-judge/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-kage-synaptic-metabolic-learner/SKILL.md](.agents/skills/atom-kage-synaptic-metabolic-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-kage-vault-hypothesis-reflector/SKILL.md](.agents/skills/atom-kage-vault-hypothesis-reflector/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-kage-walk-reflector/SKILL.md](.agents/skills/atom-kage-walk-reflector/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-linus-kernel-evolution-learner/SKILL.md](.agents/skills/atom-linus-kernel-evolution-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-neo-ergonomic-spin-tester/SKILL.md](.agents/skills/atom-neo-ergonomic-spin-tester/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-neo-frontend-tech-evaluator/SKILL.md](.agents/skills/atom-neo-frontend-tech-evaluator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-neo-frontend-vault-evolver/SKILL.md](.agents/skills/atom-neo-frontend-vault-evolver/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-neo-web-vitals-autophagy/SKILL.md](.agents/skills/atom-neo-web-vitals-autophagy/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-raven-causal-nexus-tracer/SKILL.md](.agents/skills/atom-raven-causal-nexus-tracer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-raven-deep-barrier-breaker/SKILL.md](.agents/skills/atom-raven-deep-barrier-breaker/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-raven-investigative-mind-evolver/SKILL.md](.agents/skills/atom-raven-investigative-mind-evolver/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-raven-shadow-finance-forensics/SKILL.md](.agents/skills/atom-raven-shadow-finance-forensics/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-taste-antislop-gatekeeper/SKILL.md](.agents/skills/atom-taste-antislop-gatekeeper/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-taste-hyperlocal-design-system/SKILL.md](.agents/skills/atom-taste-hyperlocal-design-system/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-taylor-marketing-psychology-learner/SKILL.md](.agents/skills/atom-taylor-marketing-psychology-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atom-yuki-autonomous-executive-learner/SKILL.md](.agents/skills/atom-yuki-autonomous-executive-learner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-boss-direct-copy/SKILL.md](.agents/skills/atoms/atom-boss-direct-copy/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-closing-gamification-xp/SKILL.md](.agents/skills/atoms/atom-closing-gamification-xp/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-closing-git-security-gate/SKILL.md](.agents/skills/atoms/atom-closing-git-security-gate/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-cognition-artifact-compiler/SKILL.md](.agents/skills/atoms/atom-cognition-artifact-compiler/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-cognition-vault-auditor/SKILL.md](.agents/skills/atoms/atom-cognition-vault-auditor/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-colab-session-guardian/SKILL.md](.agents/skills/atoms/atom-colab-session-guardian/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-colab-task-dispatcher/SKILL.md](.agents/skills/atoms/atom-colab-task-dispatcher/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-deming-pokayoke-joy/SKILL.md](.agents/skills/atoms/atom-deming-pokayoke-joy/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-deming-redbead-funnel/SKILL.md](.agents/skills/atoms/atom-deming-redbead-funnel/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-event-intel-copy/SKILL.md](.agents/skills/atoms/atom-event-intel-copy/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-evolution-knowledge-pruner/SKILL.md](.agents/skills/atoms/atom-evolution-knowledge-pruner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-evolution-meta-mutator/SKILL.md](.agents/skills/atoms/atom-evolution-meta-mutator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-forensic-judicial-audit/SKILL.md](.agents/skills/atoms/atom-forensic-judicial-audit/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-forensic-ubo-asymmetry/SKILL.md](.agents/skills/atoms/atom-forensic-ubo-asymmetry/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-gentle-optical-tokens/SKILL.md](.agents/skills/atoms/atom-gentle-optical-tokens/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-gentle-tremor-guard/SKILL.md](.agents/skills/atoms/atom-gentle-tremor-guard/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-growth-quality-gate/SKILL.md](.agents/skills/atoms/atom-growth-quality-gate/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-kage-clout-tea/SKILL.md](.agents/skills/atoms/atom-kage-clout-tea/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-learning-autonomous-navigator/SKILL.md](.agents/skills/atoms/atom-learning-autonomous-navigator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-learning-circuit-breaker-guard/SKILL.md](.agents/skills/atoms/atom-learning-circuit-breaker-guard/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-learning-cognitive-vault-keeper/SKILL.md](.agents/skills/atoms/atom-learning-cognitive-vault-keeper/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-learning-decadal-conflict-auditor/SKILL.md](.agents/skills/atoms/atom-learning-decadal-conflict-auditor/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-learning-prm-step-verifier/SKILL.md](.agents/skills/atoms/atom-learning-prm-step-verifier/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-learning-spin-tone-discriminator/SKILL.md](.agents/skills/atoms/atom-learning-spin-tone-discriminator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-learning-synaptic-equation-engine/SKILL.md](.agents/skills/atoms/atom-learning-synaptic-equation-engine/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-linus-compute-architecture/SKILL.md](.agents/skills/atoms/atom-linus-compute-architecture/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-linus-db-cache-concurrency/SKILL.md](.agents/skills/atoms/atom-linus-db-cache-concurrency/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-linus-network-transport/SKILL.md](.agents/skills/atoms/atom-linus-network-transport/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-linus-security-sandbox/SKILL.md](.agents/skills/atoms/atom-linus-security-sandbox/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-meow-voice/SKILL.md](.agents/skills/atoms/atom-meow-voice/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-onboarding-office-scaffolder/SKILL.md](.agents/skills/atoms/atom-onboarding-office-scaffolder/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-onboarding-roster-sync/SKILL.md](.agents/skills/atoms/atom-onboarding-roster-sync/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-persona-concentric-compiler/SKILL.md](.agents/skills/atoms/atom-persona-concentric-compiler/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-persona-utterance-miner/SKILL.md](.agents/skills/atoms/atom-persona-utterance-miner/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-photo-classifier/SKILL.md](.agents/skills/atoms/atom-photo-classifier/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-radar-edge-quantizer/SKILL.md](.agents/skills/atoms/atom-radar-edge-quantizer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-radar-first-principles/SKILL.md](.agents/skills/atoms/atom-radar-first-principles/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-reverse-protocol-auditor/SKILL.md](.agents/skills/atoms/atom-reverse-protocol-auditor/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-reverse-sandbox-triage/SKILL.md](.agents/skills/atoms/atom-reverse-sandbox-triage/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-shadow-circadian-guardian/SKILL.md](.agents/skills/atoms/atom-shadow-circadian-guardian/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-shadow-episodic-vault/SKILL.md](.agents/skills/atoms/atom-shadow-episodic-vault/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-slimming-4d-dispatcher/SKILL.md](.agents/skills/atoms/atom-slimming-4d-dispatcher/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-slimming-working-card/SKILL.md](.agents/skills/atoms/atom-slimming-working-card/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-taylor-campaign-launchpad/SKILL.md](.agents/skills/atoms/atom-taylor-campaign-launchpad/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-taylor-four-prism-copy/SKILL.md](.agents/skills/atoms/atom-taylor-four-prism-copy/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-taylor-funnel-telemetry/SKILL.md](.agents/skills/atoms/atom-taylor-funnel-telemetry/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-taylor-ip-meow-marketer/SKILL.md](.agents/skills/atoms/atom-taylor-ip-meow-marketer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-bi-protagonist/SKILL.md](.agents/skills/atoms/atom-threads-bi-protagonist/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-engine/SKILL.md](.agents/skills/atoms/atom-threads-engine/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-frontdoor/SKILL.md](.agents/skills/atoms/atom-threads-frontdoor/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-neighbor-crm/SKILL.md](.agents/skills/atoms/atom-threads-neighbor-crm/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-post-dispatcher/SKILL.md](.agents/skills/atoms/atom-threads-post-dispatcher/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-preflight-gate/SKILL.md](.agents/skills/atoms/atom-threads-preflight-gate/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-reply-bridge/SKILL.md](.agents/skills/atoms/atom-threads-reply-bridge/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-rss-watcher/SKILL.md](.agents/skills/atoms/atom-threads-rss-watcher/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-tea-funnel/SKILL.md](.agents/skills/atoms/atom-threads-tea-funnel/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-telemetry-compass/SKILL.md](.agents/skills/atoms/atom-threads-telemetry-compass/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-tree-watcher/SKILL.md](.agents/skills/atoms/atom-threads-tree-watcher/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-threads-trio-crafter/SKILL.md](.agents/skills/atoms/atom-threads-trio-crafter/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-trend-radar-converter/SKILL.md](.agents/skills/atoms/atom-trend-radar-converter/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-trend-scout/SKILL.md](.agents/skills/atoms/atom-trend-scout/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-trend-visual-parody/SKILL.md](.agents/skills/atoms/atom-trend-visual-parody/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-yuki-brand-redline-gate/SKILL.md](.agents/skills/atoms/atom-yuki-brand-redline-gate/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-yuki-cabinet-orchestrator/SKILL.md](.agents/skills/atoms/atom-yuki-cabinet-orchestrator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-yuki-founder-shield/SKILL.md](.agents/skills/atoms/atom-yuki-founder-shield/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-yuki-hyperlocal-artisan/SKILL.md](.agents/skills/atoms/atom-yuki-hyperlocal-artisan/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/atoms/atom-yuki-strategic-arbitrator/SKILL.md](.agents/skills/atoms/atom-yuki-strategic-arbitrator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）
- ❌ atom 技能缺少必填中繼資料：metadata.group, metadata.parent

### 📄 [.agents/skills/bionic-cognition-compiler/SKILL.md](.agents/skills/bionic-cognition-compiler/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-abacus/SKILL.md](.agents/skills/bionic-learning-abacus/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-ada/SKILL.md](.agents/skills/bionic-learning-ada/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-deming/SKILL.md](.agents/skills/bionic-learning-deming/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-falcon/SKILL.md](.agents/skills/bionic-learning-falcon/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-josef/SKILL.md](.agents/skills/bionic-learning-josef/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-kage/SKILL.md](.agents/skills/bionic-learning-kage/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-linus/SKILL.md](.agents/skills/bionic-learning-linus/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-neo/SKILL.md](.agents/skills/bionic-learning-neo/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-raven/SKILL.md](.agents/skills/bionic-learning-raven/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-system/SKILL.md](.agents/skills/bionic-learning-system/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-taylor/SKILL.md](.agents/skills/bionic-learning-taylor/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-learning-yuki/SKILL.md](.agents/skills/bionic-learning-yuki/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/bionic-self-evolution/SKILL.md](.agents/skills/bionic-self-evolution/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/daily-closing-sop/SKILL.md](.agents/skills/daily-closing-sop/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/google-colab-commander/SKILL.md](.agents/skills/google-colab-commander/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/hot-trend-scout/SKILL.md](.agents/skills/hot-trend-scout/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/inspiring-moments/SKILL.md](.agents/skills/inspiring-moments/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/one-shot-photo-marketer/SKILL.md](.agents/skills/one-shot-photo-marketer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/packs/pack-qu-guang-guang/SKILL.md](.agents/skills/packs/pack-qu-guang-guang/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/persona-reverse-engineer/SKILL.md](.agents/skills/persona-reverse-engineer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/polaris-cabinet-onboarding/SKILL.md](.agents/skills/polaris-cabinet-onboarding/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/polaris-forensic-investigator/SKILL.md](.agents/skills/polaris-forensic-investigator/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/polaris-frontier-radar/SKILL.md](.agents/skills/polaris-frontier-radar/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/polaris-gentle-ui/SKILL.md](.agents/skills/polaris-gentle-ui/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/polaris-slimming/SKILL.md](.agents/skills/polaris-slimming/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/rea-reverse-engineer/SKILL.md](.agents/skills/rea-reverse-engineer/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/shadow-soul-memory/SKILL.md](.agents/skills/shadow-soul-memory/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/taste-skill/SKILL.md](.agents/skills/taste-skill/SKILL.md)
- ❌ name (`design-taste-frontend`) 與所在資料夾 (`taste-skill`) 不符
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/threads-autonomous-walker/SKILL.md](.agents/skills/threads-autonomous-walker/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/threads-growth-auditor/SKILL.md](.agents/skills/threads-growth-auditor/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/threads-publisher/SKILL.md](.agents/skills/threads-publisher/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

### 📄 [.agents/skills/threads-rss-sentinel/SKILL.md](.agents/skills/threads-rss-sentinel/SKILL.md)
- ❌ metadata.status 非法（需為 active/draft/archived，目前為 `未填`）

---

## ❌ 二、未歸檔之舊版技能檔 (Backups outside _archive/)

✅ **零滯留**：所有舊版與歷史檔皆已妥善存放於 `_archive/` 或 `_master_history/`。

---

## ❌ 三、非 UTF-8 資料檔清冊 (Non-UTF-8 Data Files)

✅ **零異常**：全工作區所有 `.md`、`.txt`、`.json`、`.jsonl`、`.py` 檔案皆為 100% 正確的 UTF-8 編碼。

---

## ⚠️ 四、技能檔格式提醒清冊 (Skill Format Warnings)

### 📄 [.agents/skills/atom-abacus-ice-friction-stripper/SKILL.md](.agents/skills/atom-abacus-ice-friction-stripper/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 253 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-abacus-macro-compound-learner/SKILL.md](.agents/skills/atom-abacus-macro-compound-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 214 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-abacus-munger-inversion-veto/SKILL.md](.agents/skills/atom-abacus-munger-inversion-veto/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-abacus-munger-vision-moat/SKILL.md](.agents/skills/atom-abacus-munger-vision-moat/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 246 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-abacus-negative-float-cashflow/SKILL.md](.agents/skills/atom-abacus-negative-float-cashflow/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 211 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-abacus-survival-reservoir-opex/SKILL.md](.agents/skills/atom-abacus-survival-reservoir-opex/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 232 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-ada-agentic-paradigm-researcher/SKILL.md](.agents/skills/atom-ada-agentic-paradigm-researcher/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 243 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-ada-efficient-inference-scout/SKILL.md](.agents/skills/atom-ada-efficient-inference-scout/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 269 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-ada-frontier-paper-evaluator/SKILL.md](.agents/skills/atom-ada-frontier-paper-evaluator/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 262 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-ada-research-dossier-evolver/SKILL.md](.agents/skills/atom-ada-research-dossier-evolver/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 239 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-deming-andon-gatekeeper/SKILL.md](.agents/skills/atom-deming-andon-gatekeeper/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-deming-joy-flow-allocator/SKILL.md](.agents/skills/atom-deming-joy-flow-allocator/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 240 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-deming-poka-yoke-engineer/SKILL.md](.agents/skills/atom-deming-poka-yoke-engineer/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 213 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-deming-quality-sopk-learner/SKILL.md](.agents/skills/atom-deming-quality-sopk-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 220 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-deming-sopk-attribution/SKILL.md](.agents/skills/atom-deming-sopk-attribution/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 211 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-falcon-legal-vault-decadal-evolver/SKILL.md](.agents/skills/atom-falcon-legal-vault-decadal-evolver/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 233 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-falcon-precedent-caselaw-analyst/SKILL.md](.agents/skills/atom-falcon-precedent-caselaw-analyst/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-falcon-regulatory-moat-architect/SKILL.md](.agents/skills/atom-falcon-regulatory-moat-architect/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 211 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-falcon-statute-legislative-learner/SKILL.md](.agents/skills/atom-falcon-statute-legislative-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 217 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-josef-data-diagram-artisan/SKILL.md](.agents/skills/atom-josef-data-diagram-artisan/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 219 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-josef-info-hierarchy-visualizer/SKILL.md](.agents/skills/atom-josef-info-hierarchy-visualizer/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 227 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-josef-senior-accessibility-visuals/SKILL.md](.agents/skills/atom-josef-senior-accessibility-visuals/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 255 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-josef-typography-optical-engine/SKILL.md](.agents/skills/atom-josef-typography-optical-engine/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 235 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-josef-visual-aesthetics-learner/SKILL.md](.agents/skills/atom-josef-visual-aesthetics-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 228 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-kage-decadal-audit-evolver/SKILL.md](.agents/skills/atom-kage-decadal-audit-evolver/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 207 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-kage-learning-clutch-judge/SKILL.md](.agents/skills/atom-kage-learning-clutch-judge/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 238 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-kage-synaptic-metabolic-learner/SKILL.md](.agents/skills/atom-kage-synaptic-metabolic-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 213 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'status', 'type', 'version']`

### 📄 [.agents/skills/atom-kage-vault-hypothesis-reflector/SKILL.md](.agents/skills/atom-kage-vault-hypothesis-reflector/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 213 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-kage-walk-reflector/SKILL.md](.agents/skills/atom-kage-walk-reflector/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 248 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-linus-kernel-evolution-learner/SKILL.md](.agents/skills/atom-linus-kernel-evolution-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 223 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-neo-ergonomic-spin-tester/SKILL.md](.agents/skills/atom-neo-ergonomic-spin-tester/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 229 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-neo-frontend-tech-evaluator/SKILL.md](.agents/skills/atom-neo-frontend-tech-evaluator/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 259 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-neo-frontend-vault-evolver/SKILL.md](.agents/skills/atom-neo-frontend-vault-evolver/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 223 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-neo-web-vitals-autophagy/SKILL.md](.agents/skills/atom-neo-web-vitals-autophagy/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 256 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['exit_code_verified', 'parent_skill', 'role_key', 'type', 'version']`

### 📄 [.agents/skills/atom-raven-causal-nexus-tracer/SKILL.md](.agents/skills/atom-raven-causal-nexus-tracer/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 221 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-raven-deep-barrier-breaker/SKILL.md](.agents/skills/atom-raven-deep-barrier-breaker/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 201 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-raven-investigative-mind-evolver/SKILL.md](.agents/skills/atom-raven-investigative-mind-evolver/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 235 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-raven-shadow-finance-forensics/SKILL.md](.agents/skills/atom-raven-shadow-finance-forensics/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 224 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-taste-antislop-gatekeeper/SKILL.md](.agents/skills/atom-taste-antislop-gatekeeper/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 244 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-taste-hyperlocal-design-system/SKILL.md](.agents/skills/atom-taste-hyperlocal-design-system/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 233 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-taylor-marketing-psychology-learner/SKILL.md](.agents/skills/atom-taylor-marketing-psychology-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 203 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atom-yuki-autonomous-executive-learner/SKILL.md](.agents/skills/atom-yuki-autonomous-executive-learner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 236 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['base_master', 'role_key', 'version']`

### 📄 [.agents/skills/atoms/atom-boss-direct-copy/SKILL.md](.agents/skills/atoms/atom-boss-direct-copy/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-closing-gamification-xp/SKILL.md](.agents/skills/atoms/atom-closing-gamification-xp/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 287 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-closing-git-security-gate/SKILL.md](.agents/skills/atoms/atom-closing-git-security-gate/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 248 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-cognition-artifact-compiler/SKILL.md](.agents/skills/atoms/atom-cognition-artifact-compiler/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 292 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-cognition-vault-auditor/SKILL.md](.agents/skills/atoms/atom-cognition-vault-auditor/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 270 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-colab-session-guardian/SKILL.md](.agents/skills/atoms/atom-colab-session-guardian/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 245 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-colab-task-dispatcher/SKILL.md](.agents/skills/atoms/atom-colab-task-dispatcher/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 266 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-deming-pokayoke-joy/SKILL.md](.agents/skills/atoms/atom-deming-pokayoke-joy/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 247 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-deming-redbead-funnel/SKILL.md](.agents/skills/atoms/atom-deming-redbead-funnel/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 244 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-event-intel-copy/SKILL.md](.agents/skills/atoms/atom-event-intel-copy/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-evolution-knowledge-pruner/SKILL.md](.agents/skills/atoms/atom-evolution-knowledge-pruner/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-evolution-meta-mutator/SKILL.md](.agents/skills/atoms/atom-evolution-meta-mutator/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-forensic-judicial-audit/SKILL.md](.agents/skills/atoms/atom-forensic-judicial-audit/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 225 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-forensic-ubo-asymmetry/SKILL.md](.agents/skills/atoms/atom-forensic-ubo-asymmetry/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 261 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-gentle-optical-tokens/SKILL.md](.agents/skills/atoms/atom-gentle-optical-tokens/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-gentle-tremor-guard/SKILL.md](.agents/skills/atoms/atom-gentle-tremor-guard/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-growth-quality-gate/SKILL.md](.agents/skills/atoms/atom-growth-quality-gate/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-kage-clout-tea/SKILL.md](.agents/skills/atoms/atom-kage-clout-tea/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 201 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-learning-autonomous-navigator/SKILL.md](.agents/skills/atoms/atom-learning-autonomous-navigator/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-learning-circuit-breaker-guard/SKILL.md](.agents/skills/atoms/atom-learning-circuit-breaker-guard/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-learning-cognitive-vault-keeper/SKILL.md](.agents/skills/atoms/atom-learning-cognitive-vault-keeper/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-learning-decadal-conflict-auditor/SKILL.md](.agents/skills/atoms/atom-learning-decadal-conflict-auditor/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-learning-prm-step-verifier/SKILL.md](.agents/skills/atoms/atom-learning-prm-step-verifier/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-learning-spin-tone-discriminator/SKILL.md](.agents/skills/atoms/atom-learning-spin-tone-discriminator/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-learning-synaptic-equation-engine/SKILL.md](.agents/skills/atoms/atom-learning-synaptic-equation-engine/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-linus-compute-architecture/SKILL.md](.agents/skills/atoms/atom-linus-compute-architecture/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 220 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-linus-db-cache-concurrency/SKILL.md](.agents/skills/atoms/atom-linus-db-cache-concurrency/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 207 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-linus-network-transport/SKILL.md](.agents/skills/atoms/atom-linus-network-transport/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 212 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-linus-security-sandbox/SKILL.md](.agents/skills/atoms/atom-linus-security-sandbox/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 229 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-meow-voice/SKILL.md](.agents/skills/atoms/atom-meow-voice/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-onboarding-office-scaffolder/SKILL.md](.agents/skills/atoms/atom-onboarding-office-scaffolder/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 254 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-onboarding-roster-sync/SKILL.md](.agents/skills/atoms/atom-onboarding-roster-sync/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 229 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-persona-concentric-compiler/SKILL.md](.agents/skills/atoms/atom-persona-concentric-compiler/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 267 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-persona-utterance-miner/SKILL.md](.agents/skills/atoms/atom-persona-utterance-miner/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 235 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-photo-classifier/SKILL.md](.agents/skills/atoms/atom-photo-classifier/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-radar-edge-quantizer/SKILL.md](.agents/skills/atoms/atom-radar-edge-quantizer/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 291 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-radar-first-principles/SKILL.md](.agents/skills/atoms/atom-radar-first-principles/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 226 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-reverse-protocol-auditor/SKILL.md](.agents/skills/atoms/atom-reverse-protocol-auditor/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 274 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-reverse-sandbox-triage/SKILL.md](.agents/skills/atoms/atom-reverse-sandbox-triage/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 267 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-shadow-circadian-guardian/SKILL.md](.agents/skills/atoms/atom-shadow-circadian-guardian/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 227 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-shadow-episodic-vault/SKILL.md](.agents/skills/atoms/atom-shadow-episodic-vault/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 259 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-slimming-4d-dispatcher/SKILL.md](.agents/skills/atoms/atom-slimming-4d-dispatcher/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 240 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-slimming-working-card/SKILL.md](.agents/skills/atoms/atom-slimming-working-card/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 257 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-taylor-campaign-launchpad/SKILL.md](.agents/skills/atoms/atom-taylor-campaign-launchpad/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-taylor-four-prism-copy/SKILL.md](.agents/skills/atoms/atom-taylor-four-prism-copy/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-taylor-funnel-telemetry/SKILL.md](.agents/skills/atoms/atom-taylor-funnel-telemetry/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-taylor-ip-meow-marketer/SKILL.md](.agents/skills/atoms/atom-taylor-ip-meow-marketer/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-bi-protagonist/SKILL.md](.agents/skills/atoms/atom-threads-bi-protagonist/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-engine/SKILL.md](.agents/skills/atoms/atom-threads-engine/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-frontdoor/SKILL.md](.agents/skills/atoms/atom-threads-frontdoor/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-neighbor-crm/SKILL.md](.agents/skills/atoms/atom-threads-neighbor-crm/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-post-dispatcher/SKILL.md](.agents/skills/atoms/atom-threads-post-dispatcher/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-preflight-gate/SKILL.md](.agents/skills/atoms/atom-threads-preflight-gate/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-reply-bridge/SKILL.md](.agents/skills/atoms/atom-threads-reply-bridge/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-rss-watcher/SKILL.md](.agents/skills/atoms/atom-threads-rss-watcher/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-tea-funnel/SKILL.md](.agents/skills/atoms/atom-threads-tea-funnel/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-telemetry-compass/SKILL.md](.agents/skills/atoms/atom-threads-telemetry-compass/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-tree-watcher/SKILL.md](.agents/skills/atoms/atom-threads-tree-watcher/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-threads-trio-crafter/SKILL.md](.agents/skills/atoms/atom-threads-trio-crafter/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-trend-radar-converter/SKILL.md](.agents/skills/atoms/atom-trend-radar-converter/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-trend-scout/SKILL.md](.agents/skills/atoms/atom-trend-scout/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-trend-visual-parody/SKILL.md](.agents/skills/atoms/atom-trend-visual-parody/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-yuki-brand-redline-gate/SKILL.md](.agents/skills/atoms/atom-yuki-brand-redline-gate/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-yuki-cabinet-orchestrator/SKILL.md](.agents/skills/atoms/atom-yuki-cabinet-orchestrator/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-yuki-founder-shield/SKILL.md](.agents/skills/atoms/atom-yuki-founder-shield/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-yuki-hyperlocal-artisan/SKILL.md](.agents/skills/atoms/atom-yuki-hyperlocal-artisan/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/atoms/atom-yuki-strategic-arbitrator/SKILL.md](.agents/skills/atoms/atom-yuki-strategic-arbitrator/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/bionic-cognition-compiler/SKILL.md](.agents/skills/bionic-cognition-compiler/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 292 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/bionic-learning-abacus/SKILL.md](.agents/skills/bionic-learning-abacus/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-ada/SKILL.md](.agents/skills/bionic-learning-ada/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 208 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-deming/SKILL.md](.agents/skills/bionic-learning-deming/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-falcon/SKILL.md](.agents/skills/bionic-learning-falcon/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-josef/SKILL.md](.agents/skills/bionic-learning-josef/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 362 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-kage/SKILL.md](.agents/skills/bionic-learning-kage/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-linus/SKILL.md](.agents/skills/bionic-learning-linus/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-neo/SKILL.md](.agents/skills/bionic-learning-neo/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 704 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`
- ⚠️ 技能內文超過 500 行（目前 733 行），建議將理論移至 references/

### 📄 [.agents/skills/bionic-learning-raven/SKILL.md](.agents/skills/bionic-learning-raven/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 244 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-learning-system/SKILL.md](.agents/skills/bionic-learning-system/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 239 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'is_master', 'lock_status', 'version']`

### 📄 [.agents/skills/bionic-learning-taylor/SKILL.md](.agents/skills/bionic-learning-taylor/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 243 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`
- ⚠️ 技能內文超過 500 行（目前 778 行），建議將理論移至 references/

### 📄 [.agents/skills/bionic-learning-yuki/SKILL.md](.agents/skills/bionic-learning-yuki/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 364 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'base_master', 'can_evolve_independently', 'delegated_chapters', 'is_daughter_variant', 'lock_status', 'role_key', 'version']`

### 📄 [.agents/skills/bionic-self-evolution/SKILL.md](.agents/skills/bionic-self-evolution/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/daily-closing-sop/SKILL.md](.agents/skills/daily-closing-sop/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/google-colab-commander/SKILL.md](.agents/skills/google-colab-commander/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 364 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/hot-trend-scout/SKILL.md](.agents/skills/hot-trend-scout/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 332 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/inspiring-moments/SKILL.md](.agents/skills/inspiring-moments/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 264 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['author', 'authorized_by', 'role_key', 'verified_by', 'version']`

### 📄 [.agents/skills/one-shot-photo-marketer/SKILL.md](.agents/skills/one-shot-photo-marketer/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/packs/pack-qu-guang-guang/SKILL.md](.agents/skills/packs/pack-qu-guang-guang/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/persona-reverse-engineer/SKILL.md](.agents/skills/persona-reverse-engineer/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/polaris-cabinet-onboarding/SKILL.md](.agents/skills/polaris-cabinet-onboarding/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 232 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/polaris-forensic-investigator/SKILL.md](.agents/skills/polaris-forensic-investigator/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 283 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'role_owners', 'version']`

### 📄 [.agents/skills/polaris-frontier-radar/SKILL.md](.agents/skills/polaris-frontier-radar/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 296 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'role_key', 'version']`

### 📄 [.agents/skills/polaris-gentle-ui/SKILL.md](.agents/skills/polaris-gentle-ui/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 350 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['authorized_by', 'role_key', 'version']`

### 📄 [.agents/skills/polaris-slimming/SKILL.md](.agents/skills/polaris-slimming/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 217 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/rea-reverse-engineer/SKILL.md](.agents/skills/rea-reverse-engineer/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/shadow-soul-memory/SKILL.md](.agents/skills/shadow-soul-memory/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/taste-skill/SKILL.md](.agents/skills/taste-skill/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 904 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version
- ⚠️ frontmatter 最外層含有過渡自訂欄位，應搬入 metadata：`['hooks']`

### 📄 [.agents/skills/threads-autonomous-walker/SKILL.md](.agents/skills/threads-autonomous-walker/SKILL.md)
- ⚠️ description 建議控制在 200 字以內（目前 356 字）
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/threads-growth-auditor/SKILL.md](.agents/skills/threads-growth-auditor/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/threads-publisher/SKILL.md](.agents/skills/threads-publisher/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

### 📄 [.agents/skills/threads-rss-sentinel/SKILL.md](.agents/skills/threads-rss-sentinel/SKILL.md)
- ⚠️ 缺少建議欄位：metadata.owner, metadata.version

---

## ⚠️ 五、工作資料夾殘留垃圾清冊 (Residual Artifacts)

| 殘留類型 | 檔案相對路徑 | 建議動作 |
| :--- | :--- | :--- |
| __pycache__ 快取資料夾 | [.agents/skills/bionic-learning-system/bionic_core/__pycache__](.agents/skills/bionic-learning-system/bionic_core/__pycache__) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [.agents/skills/bionic-learning-system/bionic_core/__pycache__/cycle_ledger.cpython-312.pyc](.agents/skills/bionic-learning-system/bionic_core/__pycache__/cycle_ledger.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [.agents/skills/bionic-learning-system/bionic_core/__pycache__/evidence_gate.cpython-312.pyc](.agents/skills/bionic-learning-system/bionic_core/__pycache__/evidence_gate.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [.agents/skills/bionic-learning-system/bionic_core/__pycache__/founder_auth.cpython-312.pyc](.agents/skills/bionic-learning-system/bionic_core/__pycache__/founder_auth.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [.agents/skills/bionic-learning-system/bionic_core/__pycache__/rule_store.cpython-312.pyc](.agents/skills/bionic-learning-system/bionic_core/__pycache__/rule_store.cpython-312.pyc) | 刪除或移至 _archive/ |
| __pycache__ 快取資料夾 | [.agents/skills/hot-trend-scout/scripts/__pycache__](.agents/skills/hot-trend-scout/scripts/__pycache__) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [.agents/skills/hot-trend-scout/scripts/__pycache__/scan_taiwan_trends.cpython-312.pyc](.agents/skills/hot-trend-scout/scripts/__pycache__/scan_taiwan_trends.cpython-312.pyc) | 刪除或移至 _archive/ |
| __pycache__ 快取資料夾 | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/bionic_knowledge_gate.cpython-312.pyc](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/bionic_knowledge_gate.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/data_integrity_guard.cpython-312.pyc](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/data_integrity_guard.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/feedback_loop.cpython-312.pyc](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/feedback_loop.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/interaction_safety_gate.cpython-312.pyc](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/interaction_safety_gate.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/service_truth_gate.cpython-312.pyc](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/service_truth_gate.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/threads_publisher.cpython-312.pyc](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/threads_publisher.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/topic_safety_gate.cpython-312.pyc](00-03_Brand_LifeButler/00-03-06_Threads_Meow_Hub/scripts/__pycache__/topic_safety_gate.cpython-312.pyc) | 刪除或移至 _archive/ |
| __pycache__ 快取資料夾 | [scripts/__pycache__](scripts/__pycache__) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [scripts/__pycache__/bionic_knowledge_gate.cpython-312.pyc](scripts/__pycache__/bionic_knowledge_gate.cpython-312.pyc) | 刪除或移至 _archive/ |
| 殘留檔案 (*.pyc) | [scripts/__pycache__/build_all_proposals.cpython-312.pyc](scripts/__pycache__/build_all_proposals.cpython-312.pyc) | 刪除或移至 _archive/ |
