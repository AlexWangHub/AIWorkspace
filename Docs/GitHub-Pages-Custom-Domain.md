# GitHub Pages 绑定自定义域名（以 vibewhip.com 为例）

## 背景

我们的 App 声明页面（营销页、隐私政策、技术支持）托管在 GitHub Pages 上，原始访问地址为：

```
https://alexwanghub.github.io/AIWorkspace/VibeWhip/
https://alexwanghub.github.io/AIWorkspace/ClipVault/
...
```

绑定自定义域名 `vibewhip.com` 后，访问地址变为：

```
https://vibewhip.com/VibeWhip/
https://vibewhip.com/ClipVault/
...
```

原来的 `github.io` 地址会自动 301 重定向到新域名，不会有死链。

---

## 我们一共配了哪些 DNS 记录？

在腾讯云 DNS 解析控制台，为 `vibewhip.com` 添加了以下记录：

### 1. A 记录 × 2 —— 让 `vibewhip.com` 指向 GitHub 服务器

| 记录类型 | 主机记录 | 记录值 |
|---------|---------|--------|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |

**作用**：当用户在浏览器输入 `vibewhip.com` 时，DNS 把域名解析到 GitHub Pages 的服务器 IP 地址。

**为什么是 2 条？** GitHub 官方提供了 4 个 IP（108/109/110/111），但腾讯云免费套餐限制同一主机记录最多 2 条负载均衡，所以只加了 2 条，功能完全正常，只是冗余少一点。

> GitHub Pages 完整 IP 列表（如果套餐支持可以全加）：
> - 185.199.108.153
> - 185.199.109.153
> - 185.199.110.153
> - 185.199.111.153

### 2. CNAME 记录 × 1 —— 让 `www.vibewhip.com` 也能访问

| 记录类型 | 主机记录 | 记录值 |
|---------|---------|--------|
| CNAME | `www` | `alexwanghub.github.io` |

**作用**：当用户输入 `www.vibewhip.com` 时，DNS 把它指向 `alexwanghub.github.io`，GitHub 再自动转到正确的页面。

**注意**：CNAME 记录值只写 `alexwanghub.github.io`，不要带仓库名。

### 3. TXT 记录 × 1 —— 验证域名所有权

| 记录类型 | 主机记录 | 记录值 |
|---------|---------|--------|
| TXT | `_github-pages-challenge-AlexWangHub` | `7346725b93cc35b10553bfee114517` |

**作用**：GitHub 通过查询这条 TXT 记录来确认"这个域名确实是你的"，防止别人冒用你的域名。验证通过后这条记录建议保留，不要删。

---

## 三种记录的通俗理解

```
用户输入 vibewhip.com
       │
       ▼
   DNS 查询 A 记录
       │
       ▼
  "去找 185.199.108.153"  ──→  GitHub Pages 服务器  ──→  返回网页内容
```

```
用户输入 www.vibewhip.com
       │
       ▼
   DNS 查询 CNAME 记录
       │
       ▼
  "去找 alexwanghub.github.io"  ──→  GitHub Pages 服务器  ──→  返回网页内容
```

```
GitHub 验证域名所有权
       │
       ▼
   DNS 查询 TXT 记录
       │
       ▼
  找到 _github-pages-challenge-AlexWangHub 的值
       │
       ▼
  值匹配 ──→ ✅ 验证通过，确认你是域名所有者
```

| 记录类型 | 一句话解释 |
|---------|-----------|
| **A 记录** | 域名 → IP 地址（告诉浏览器去哪台服务器找网页） |
| **CNAME 记录** | 域名 → 另一个域名（别名转发，`www` 版本跳到主域名） |
| **TXT 记录** | 域名上挂一段文本（用于身份验证，证明"这域名是我的"） |

---

## GitHub 端配置

1. 进入 `AIWorkspace` 仓库 → **Settings** → **Pages**
2. **Custom domain** 填入 `vibewhip.com` → 点 **Save**
3. 等 DNS 生效后勾选 **Enforce HTTPS**（启用 HTTPS）

GitHub 会自动在仓库根目录生成一个 `CNAME` 文件，内容为 `vibewhip.com`。

---

## 配置完成后的最终地址

| App | 首页 | 隐私政策 | 技术支持 |
|-----|------|---------|---------|
| VibeWhip | `https://vibewhip.com/VibeWhip/` | `https://vibewhip.com/VibeWhip/privacy.html` | `https://vibewhip.com/VibeWhip/support.html` |
| ClipVault | `https://vibewhip.com/ClipVault/` | `https://vibewhip.com/ClipVault/privacy.html` | `https://vibewhip.com/ClipVault/support.html` |
| DropShelf | `https://vibewhip.com/DropShelf/` | `https://vibewhip.com/DropShelf/privacy.html` | `https://vibewhip.com/DropShelf/support.html` |
| PicFlow | `https://vibewhip.com/PicFlow/` | `https://vibewhip.com/PicFlow/privacy.html` | `https://vibewhip.com/PicFlow/support.html` |
| ClipToNotion | `https://vibewhip.com/ClipToNotion/` | `https://vibewhip.com/ClipToNotion/privacy.html` | `https://vibewhip.com/ClipToNotion/support.html` |

---

## 常用排查命令

```bash
# 检查 A 记录是否生效
dig vibewhip.com +short -t A

# 检查 CNAME 记录是否生效
dig www.vibewhip.com +short -t CNAME

# 检查 TXT 验证记录是否生效
dig TXT _github-pages-challenge-AlexWangHub.vibewhip.com +short

# 检查 HTTPS 证书状态
curl -I https://vibewhip.com
```

---

## 注意事项

- DNS 变更通常几分钟生效，最多 24 小时
- 一个 GitHub 仓库只能绑定一个自定义域名
- TXT 验证记录验证通过后也建议保留，不要删除
- 页面内部链接使用的是相对路径，换域名后无需修改任何 HTML 代码
