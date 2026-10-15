
本指南專注於兩大硬核目標：
1. **GitHub + Hugo 建構 SOP**：如何從零在 GitHub 建立 Hugo 網站倉庫、雙主題與 GitHub Actions 自動部署。
2. **寫文章 Skill 設計**：如何在專案中建立客製化 AI 代理技能 (`.agent/skills/{SKILL_NAME}/SKILL.md`)，規範寫作格式、台灣用語與圖文修訂習慣，讓 AI 能依據 Skill 指令自動撰寫第一篇隨筆。

> 💡 **提示**：文中凡包含 `{}` 包裹的欄位（如 `{YOUR_GITHUB_USERNAME}`），均為**使用者需事先替換的自訂變數**。

---

## 🏗️ 第一部分： 在 GitHub 上建構 Hugo 筆記網站 (GitHub & Hugo Setup)

### 1.1 前置準備 (Prerequisites)
* 安裝 `git` 與 `hugo` (extended 版本)。
* 在 GitHub 上建立全新公開/私有倉庫：`https://github.com/{YOUR_GITHUB_USERNAME}/{YOUR_BLOG_REPO_NAME}`。

### 1.2 本地建立 Hugo 專案與安裝雙主題 (Site Initialization)
```bash
# 1. 建立 Hugo 靜態網站專案
hugo new site {YOUR_BLOG_REPO_NAME} --format yaml
cd {YOUR_BLOG_REPO_NAME}

# 2. 初始化 Git 倉庫
git init

# 3. 以 Submodule 安裝 PaperMod 與 Hugo-Book 雙主題
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule add https://github.com/alex-shv/hugo-book.git themes/hugo-book
```

### 1.3 核心設定檔 `hugo.yml` 設定範本
在專案根目錄替換 `hugo.yml`：
```yaml
baseURL: "https://{YOUR_GITHUB_USERNAME}.github.io/{YOUR_BLOG_REPO_NAME}/"
languageCode: "zh-tw"
hasCJKLanguage: true
title: "{YOUR_SITE_TITLE}"
theme: ["PaperMod", "hugo-book"]

outputs:
  home: [HTML, RSS, JSON]

params:
  BookSection: kb
  githubRepo: "https://github.com/{YOUR_GITHUB_USERNAME}/{YOUR_BLOG_REPO_NAME}"
  githubBranch: "main"
  DateFormat: "2006-01-02"
  defaultTheme: auto
  ShowReadingTime: true
  ShowBreadCrumbs: true
  ShowToc: true
  TocOpen: true

taxonomies:
  category: categories
  tag: tags
  series: series

menu:
  main:
    - identifier: search
      name: "🔍 搜尋"
      url: /search/
      weight: 5
    - identifier: kb
      name: "🧠 知識庫 (KB)"
      url: /kb/
      weight: 6
    - identifier: categories
      name: "📁 分類"
      url: /categories/
      weight: 10
    - identifier: posts
      name: "📝 文章隨筆"
      url: /posts/
      weight: 20

markup:
  goldmark:
    renderer:
      unsafe: true
```

### 1.4 設定 GitHub Actions 自動發布 (.github/workflows/deploy.yml)
建立 `.github/workflows/deploy.yml` 檔案：
```yaml
name: Deploy Hugo Site to GitHub Pages

on:
  push:
    branches: ["main"]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo
        uses: actions/setup-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true

      - name: Build Site
        run: hugo --minify

      - name: Upload Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## ⚙️ 第二部分： 建構「寫文章」AI 代理技能 (Building Note Writing Skill)

為了讓 AI 代理程式能依據規範自動撰寫與維護文章，我們在專案中建立一個 **Agent Skill** 檔案：`.agent/skills/{SKILL_NAME}/SKILL.md`。

### 2.1 SKILL.md 檔案結構範本
請建立檔案 `.agent/skills/{SKILL_NAME}/SKILL.md`：

```markdown
---
name: {SKILL_NAME}
description: 專門負責為 {YOUR_SITE_TITLE} 撰寫、建構與修訂文章隨筆，確保符合雙軌結構、台灣語境與封面圖規範。
---

# ✍️ {YOUR_SITE_TITLE} 文章撰寫技能 (Note Writing Skill)

當使用者要求「撰寫新文章」、「建立部落格隨筆」或「發布活動/實戰紀錄」時，觸發本技能並執行以下步驟：

## 1. 建立 Hugo Leaf Bundle 目錄與檔案
* **文章路徑**：`content/posts/YYYYMMDD_{TOPIC_NAME}/index.md`
* **圖片路徑**：`content/posts/YYYYMMDD_{TOPIC_NAME}/cover.jpg`

## 2. YAML Frontmatter 格式規範
```yaml
---
title: "{YOUR_POST_TITLE}"
date: {YYYY-MM-DDTHH:MM:SS+08:00}
tags:
  - {TAG_1}
  - {TAG_2}
categories:
  - {CATEGORY_1}
cover:
    image: "cover.jpg"
    alt: "{COVER_ALT_TEXT}"
    relative: true
summary: "{SUMMARY_TEXT}"
---
```

## 3. 圖文修訂習慣與原則
1. **精簡中文圖原則 (Zero-Text Clean Visuals)**：
   * 封面圖統一生成 **16:9** 比例。
   * 圖片內嚴禁出現簡體字、錯字或無意義文字亂碼。優先生成「繁體中文的視覺插圖或實景照片」。先寫文在規劃產圖
2. **台灣語境規範**：
   * 內文必須採用繁體中文（台灣習慣用語），嚴禁使用中國大陸用語（如：資訊/軟體/支援/最佳化/檔案/資料）。
3. **極簡相對路徑**：
   * 文章內的圖片與內部連結一律採用相對路徑 (`./cover.jpg` 或 `../../kb/`)。

## 4. 全局標籤與分類控管 (PostLabels Mechanism)
1. ** PostLabels.md 控制平面**：
   * 在專案根目錄維護一個 `PostLabels.md` 檔案，定義標準分類 (Categories)、流域名稱 (Basins) 與白名單標籤總表。
2. ** Taxonomy 自動偵測與同步 (Auto-Discovery)**：
   * 寫作完成後，可透過自動化腳本掃描標題與內文關鍵字（如 `n8n`, `WalkGIS`, `ATAK`, `淡水河` 等）：
     `python scripts/blog/extract_blog_metadata.py && python scripts/blog/update_blog_metadata.py`
   * 腳本會自動將符合白名單的關鍵字補寫回 YAML Frontmatter 的 `tags` 中，並同步更新 `PostLabels.md`。

## 5. 完成寫作後的自動化檢驗
1. 檢查 Frontmatter 格式是否健全。
2. 確認 `cover.jpg` 已經成功存入同個資料夾。
```

---

## 🤖 第三部分： Agentic AI 啟動指令 (Universal Agent Bootstrap Prompt)

開啟 Agentic AI 視窗時，複製以下 Prompt 貼給 AI，引導 AI 讀取並執行剛剛建立的 Skill：

```markdown
<AGENT_BOOTSTRAP_PROMPT>
你現在是「{YOUR_SITE_TITLE}」筆記網站的 Agentic AI Pair Programmer。
請遵守以下設定與工作流程：

1. 【專案結構】：
   - 專案為 Hugo 靜態網站 (位於 {PATH_TO_YOUR_BLOG_REPO})。
   - content/kb/ 為結構化知識庫 (Hugo Book 視角)。
   - content/posts/ 為時間流隨筆 (PaperMod 視角)。
   - 根目錄維護 PostLabels.md 全局標籤控管控制平面。

2. 【技能加載】：
   - 寫文章與修訂習慣已定義於技能 `.agent/skills/{SKILL_NAME}/SKILL.md` 中。
   - 當接到寫文章需求時，自動讀取並遵循該 SKILL.md 規範（包含 16:9 無文字亂碼封面圖、台灣語境、相對路徑、PostLabels 標籤自動同步）。

3. 【相對路徑與修訂】：
   - 檔案路徑與圖片引用一律使用相對路徑。

請確認你已讀取並內化上述規範。收到請簡短回覆：「{YOUR_SITE_TITLE} Agent 準備就緒！請指示下一步行動（例如：建立專案結構、配置技能或撰寫第一篇文章）。」
</AGENT_BOOTSTRAP_PROMPT>
```

---

## 🚀 第四部分： 從建構到開始寫第一篇文實作流程 (End-to-End Workflow)

1. **第 1 步 (建構 GitHub 網站)**：
   * 執行 `1.2` 節指令初始化 Hugo 專案。
   * 設定 `1.3` 的 `hugo.yml` 與 `1.4` 的 `.github/workflows/deploy.yml`。
2. **第 2 步 (建立寫文章 Skill)**：
   * 建立 `.agent/skills/{SKILL_NAME}/SKILL.md` 檔案，填入 `2.1` 節的規範。
3. **第 3 步 (啟動 AI 代理)**：
   * 複製 `第三部分` 的 Prompt 發給 AI。
4. **第 4 步 (寫第一篇文章)**：
   * 指令 AI：「請調用 `{SKILL_NAME}` 技能，幫我在 `content/posts/20260901_first_post/` 建立第一篇主題為 {YOUR_FIRST_POST_TOPIC} 的筆記隨筆，並配一張 16:9 無文字亂碼封面圖 cover.jpg」。
5. **第 5 步 (Taxonomy 自動對照整合與發布)**：
   * 執行 `python scripts/blog/extract_blog_metadata.py && python scripts/blog/update_blog_metadata.py` 完成標籤自動探勘與 `PostLabels.md` 更新。
   * 執行 `hugo server -D` 本地預覽。
   * 執行 `git add . && git commit -m "feat: site setup and first post" && git push origin main` 完成發布！
