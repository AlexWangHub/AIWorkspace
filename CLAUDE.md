# VibeWhip AI 进击场 — 项目说明

## 核心目标

**所有内容（App、AI快讯、AI论文、技术文章）都是引流漏斗，最终目的是引导用户扫码加入知识星球。**

知识星球二维码展示在网站右下角固定浮窗（`assets/zhishixingqiu.jpg`），这是整个项目的核心转化入口。

## 项目定位

- **网站名称**：VibeWhip AI 进击场
- **域名**：https://vibewhip.com
- **部署方式**：GitHub Pages（静态站）
- **作者身份**：@VibeWhip（独立开发者 · AI信息前哨 · macOS工具匠人）

## 内容策略（围绕知识星球引流）

| 模块 | 内容 | 引流逻辑 |
|------|------|----------|
| macOS 应用下载 | 5款免费App（VibeWhip/ClipVault/DropShelf/PicFlow/ClipToNotion） | 免费工具吸引开发者/效率用户，建立信任后转化 |
| 今日AI快讯Top5 | 每日精选5条AI动态，~200字/条 | 高频更新制造回访习惯，星球提供更深度内容 |
| 今日AI论文Top5 | 每日精选5篇arXiv热门论文 | 吸引技术向用户，星球提供论文深度解读 |
| 内部文章 | 技术深度文章（如Git Worktree指南） | 展示专业度，星球提供更多独家内容 |

## 项目结构

```
Declaration/
├── index.html              # 主页（单页面，4个模块）
├── sitemap.xml             # SEO sitemap
├── robots.txt              # SEO robots
├── CNAME                   # 自定义域名：vibewhip.com
├── assets/
│   ├── main_logo.png       # 网站Logo
│   └── zhishixingqiu.jpg   # 知识星球二维码（核心转化素材）
├── downloads/              # App下载包（.zip）
├── articles/               # 内部文章目录（放.md文件）
├── blogs/                  # 渲染后的HTML文章
├── VibeWhip/               # App详情页
├── ClipVault/
├── DropShelf/
├── PicFlow/
└── ClipToNotion/
```

App 源文件：`/Users/blibli/Desktop/AIWorkspace/AppTest/`
Logo 源文件：`/Users/blibli/Desktop/AIWorkspace/Workflow/main_logo.png`
星球图片源文件：`/Users/blibli/Desktop/AIWorkspace/Workflow/知识星球.jpg`

## 每日更新流程

已创建 Skill `vibewhip-daily-update`，对我说"更新网站"即可触发：

1. 搜索今日 AI 快讯 Top5
2. 搜索今日 AI 论文 Top5
3. 检查 `articles/` 是否有新 .md 文章
4. 检查 `AppTest/` 的 App 是否有更新
5. 用 `replace_in_file` 精准更新 `index.html` 中的快讯和论文内容
6. 更新 `sitemap.xml` 日期
7. Git commit & push

## 设计规范

- **暗色主题**：bg `#0a0a0b`，surface `#141416`
- **主色调**：紫色渐变 `#8b5cf6 → #06b6d4`
- **字体**：Noto Sans SC + JetBrains Mono
- **无"联系"链接**
- **知识星球浮窗始终固定在右下角**

## 注意事项

- 浏览量和下载量目前用 localStorage 本地统计
- 所有内容必须真实有据，不编造新闻和论文
- 每条新闻/论文约200字中文
- arXiv论文链接必须真实有效
- 更新时用 `replace_in_file` 精准替换，不要重写整个 index.html
