#!/usr/bin/env python3
"""Rewrite all remaining HTML files to default English with data-zh/data-en pattern."""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Translation dictionaries for bare Chinese text per file
# These map bare Chinese text → English translation

CLIPVAULT_INDEX_TRANSLATIONS = {
    "macOS 智能剪贴板管理器": "macOS Smart Clipboard Manager",
    "复制即保存": "Copy to Save",
    "一款赛博朋克风格的 macOS 剪贴板管理器。": "A cyberpunk-style macOS clipboard manager.",
    "自动捕获剪贴板历史，内置区域截图与屏幕录制，全局快捷键一键呼出。": "Auto-capture clipboard history, built-in screenshots & screen recording, global hotkey activation.",
    "在 Mac App Store 下载": "Download on Mac App Store",
    "自动捕获你复制的一切内容——文本、链接、图片、邮箱、电话、颜色代码，统统保存到本地数据库。智能识别内容类型，分类整理，随时回溯历史记录。": "Automatically captures everything you copy — text, links, images, emails, phone numbers, color codes — all saved to a local database. Smart content type recognition, organized by category, with instant history recall.",
    "安静地待在菜单栏，点击即可查看最近 50 条记录。键盘快捷导航，数字键直接复制。": "Stays quietly in the menu bar. Click to view last 50 records. Keyboard navigation, number keys to copy directly.",
    "内置截图工具，拖拽选区精准截取。截图自动保存并纳入 ClipVault 统一管理。": "Built-in screenshot tool with precise drag-to-select. Screenshots auto-saved and managed by ClipVault.",
    "选区录制或全屏录制，带有霓虹风格录制指示器。录制结果自动纳入 ClipVault 管理。": "Area or fullscreen recording with neon-style indicator. Recordings auto-managed by ClipVault.",
    "按内容类型、日期范围、标签多维度筛选，支持模糊搜索。150ms 防抖实时搜索，无论有多少条记录都能瞬间定位。支持网格/列表双布局视图切换。": "Filter by content type, date range, tags. Fuzzy search with 150ms debounce for instant results regardless of record count. Grid/list dual-view layout.",
    "三个可自定义热键——呼出面板、截图、录屏。在任何应用中一键触发，不打断心流。": "Three customizable hotkeys — panel, screenshot, recording. One-key trigger from any app without breaking flow.",
    "从 Mac App Store 下载安装，首次启动按引导完成权限授予": "Download from Mac App Store, follow the setup guide on first launch",
    "在设置中自定义全局快捷键（可选），设置面板/截图/录屏热键": "Customize global hotkeys in settings (optional) for panel/screenshot/recording",
    "正常复制任何内容，ClipVault 自动捕获。随时回溯、搜索、一键复制": "Copy anything normally, ClipVault captures automatically. Recall, search, one-click copy anytime",
    "ClipVault 是一款 100% 离线应用。所有数据仅存储在你的 Mac 本地，\n                    不连接任何服务器，不上传任何数据，不包含任何追踪或分析 SDK。\n                    你的剪贴板内容只属于你。": "ClipVault is a 100% offline app. All data is stored locally on your Mac, with no server connections, no data uploads, and no tracking or analytics SDKs. Your clipboard content belongs only to you.",
    "首页": "Home",
    "技术支持": "Support",
    "隐私政策": "Privacy",
}

CLIPVAULT_PRIVACY_TRANSLATIONS = {
    "最后更新日期：2026 年 3 月 23 日": "Last updated: March 23, 2026",
    "🛡️ ClipVault 是一款 100% 离线应用。不收集、不存储、不传输任何用户数据到任何服务器。你的隐私是我们的首要考量。": "🛡️ ClipVault is a 100% offline app. It does not collect, store, or transmit any user data to any server. Your privacy is our top priority.",
    "ClipVault（以下简称「本应用」）是一款 macOS 智能剪贴板管理器，帮助用户自动捕获和管理剪贴板历史，并提供区域截图与屏幕录制功能。本隐私政策说明了本应用如何处理你的信息。": 'ClipVault (hereinafter "the App") is a macOS smart clipboard manager that helps users auto-capture and manage clipboard history, with area screenshot and screen recording features. This privacy policy explains how the App handles your information.',
    "本应用不收集任何个人信息。": "The App does not collect any personal information.",
    "具体而言：": "Specifically:",
    "不收集用户身份信息（姓名、邮箱、设备标识符等）": "No collection of user identity information (name, email, device identifiers, etc.)",
    "不收集使用分析数据或行为数据": "No collection of usage analytics or behavioral data",
    "不使用任何第三方分析或追踪 SDK": "No third-party analytics or tracking SDKs",
    "不包含广告或广告追踪": "No ads or ad tracking",
    "不使用 Cookie 或类似追踪技术": "No cookies or similar tracking technologies",
    "本应用不建立任何网络连接。": "The App does not establish any network connections.",
    "ClipVault 是一款完全离线的应用，不与任何服务器通信。没有 API 调用、没有云同步、没有遥测数据上报。应用的所有功能均在你的 Mac 本地完成。": "ClipVault is a fully offline app that does not communicate with any server. No API calls, no cloud sync, no telemetry. All features run locally on your Mac.",
    "💡 ClipVault 不需要互联网连接即可正常工作。你的剪贴板数据、截图和录屏文件始终存储在你的 Mac 本地，从不离开你的设备。": "💡 ClipVault does not require an internet connection. Your clipboard data, screenshots, and recordings are always stored locally on your Mac, never leaving your device.",
    "本应用会在你的设备本地存储以下信息，这些数据仅保存在你的 macOS 系统中，不会上传到任何服务器：": "The App stores the following information locally on your device. This data is only saved on your macOS system and is never uploaded to any server:",
    "剪贴板历史记录": "Clipboard History",
    "保存用户复制的文本、链接、图片等内容": "Saves text, links, images copied by the user",
    "本地 SwiftData 数据库": "Local SwiftData Database",
    "图片原始数据": "Image Raw Data",
    "保存复制的图片或截图的原始二进制数据": "Saves raw binary data of copied images or screenshots",
    "截图文件": "Screenshot Files",
    "区域截图功能生成的 PNG 图片": "PNG images from area screenshot feature",
    "本地文件（默认桌面，可自定义）": "Local file (default Desktop, customizable)",
    "录屏文件": "Recording Files",
    "屏幕录制功能生成的 MOV 视频": "MOV videos from screen recording feature",
    "本地文件（默认影片文件夹，可自定义）": "Local file (default Movies folder, customizable)",
    "快捷键配置": "Hotkey Settings",
    "记录用户自定义的三个全局快捷键": "Stores three user-defined global hotkeys",
    "用户偏好设置": "User Preferences",
    "记录界面语言、历史上限、清理策略等设置": "Stores interface language, history limit, cleanup policy settings",
    "自定义标签": "Custom Tags",
    "用户为剪贴板记录添加的分类标签": "Category tags added by users to clipboard records",
    "本应用的核心功能是监控和管理系统剪贴板内容。当「自动捕获剪贴板」功能开启时，本应用会以 1.5 秒的间隔检查系统剪贴板是否有新内容，并将新内容保存到本地数据库。": "The App's core function is to monitor and manage system clipboard content. When auto-capture is enabled, the App checks the clipboard every 1.5 seconds for new content and saves it to the local database.",
    "你可以随时在设置中关闭自动捕获功能。关闭后，本应用不会读取剪贴板。": "You can disable auto-capture anytime in settings. When disabled, the App will not read the clipboard.",
    "本应用的区域截图和屏幕录制功能需要 macOS「屏幕录制」权限。该权限仅用于以下目的：": "The App's screenshot and screen recording features require macOS Screen Recording permission. This permission is only used for:",
    "区域截图": "Area Screenshot",
    "屏幕录制": "Screen Recording",
    "截取或录制的内容仅保存在你的 Mac 本地，不会传输到任何服务器。你可以随时在系统设置中撤销该权限。": "Captured or recorded content is only saved locally on your Mac, never transmitted to any server. You can revoke the permission anytime in System Settings.",
    "本应用使用 Apple Vision 框架在本地对图片进行 OCR 文字识别。整个识别过程完全在你的设备上进行，图片数据不会被发送到任何服务器。": "The App uses Apple Vision framework for local OCR text recognition. The entire process runs on your device — image data is never sent to any server.",
    "本应用可选设置为登录项，使用 macOS SMAppService API 实现开机自启。该功能仅在你主动开启时生效，且可以随时在设置中关闭。": "The App can optionally be set as a login item using macOS SMAppService API. This only takes effect when you enable it and can be disabled anytime in settings.",
    "你对自己的数据拥有完全控制权：": "You have full control over your data:",
    "可以逐条删除历史记录": "Delete individual history records",
    "可以在设置中一键清除所有历史数据": "One-click clear all history in settings",
    "可以手动删除截图和录屏文件": "Manually delete screenshot and recording files",
    "可以在设置中一键清理指定存储目录": "One-click clean specified storage directory in settings",
    "本应用不集成任何第三方 SDK 或服务。没有广告、没有分析工具、没有崩溃报告平台、没有社交媒体 SDK。应用完全使用 Apple 原生框架构建。": "The App does not integrate any third-party SDKs or services. No ads, no analytics, no crash reporting, no social media SDKs. Built entirely with Apple native frameworks.",
    "本应用不针对 13 岁以下的儿童。本应用不会有意收集任何儿童的个人信息。": "The App is not directed at children under 13. The App does not knowingly collect any personal information from children.",
    "如本隐私政策有重大变更，我们将通过应用更新或本页面进行通知。建议你定期查看本页面以了解最新的隐私政策。": "If there are significant changes to this privacy policy, we will notify you through app updates or this page. We recommend checking this page periodically.",
    "如果你对本隐私政策有任何疑问或建议，请通过以下方式联系我们：": "If you have any questions or suggestions about this privacy policy, please contact us at:",
    "首页": "Home",
    "技术支持": "Support",
    "隐私政策": "Privacy",
}

CLIPVAULT_SUPPORT_TRANSLATIONS = {
    "安装并启动 ClipVault": "Install and Launch ClipVault",
    "从 Mac App Store 下载 ClipVault。首次启动时，按照引导页的指引完成基本设置。": "Download ClipVault from the Mac App Store. On first launch, follow the setup guide to complete basic configuration.",
    "授予屏幕录制权限": "Grant Screen Recording Permission",
    "配置全局快捷键（可选）": "Configure Global Hotkeys (Optional)",
    "开始使用": "Start Using",
    "正常复制任何内容，ClipVault 会自动捕获并保存。点击菜单栏图标或按下快捷键即可查看历史、搜索内容、一键复制回剪贴板。": "Copy anything normally and ClipVault will auto-capture and save. Click the menu bar icon or press the hotkey to view history, search, and one-click copy back to clipboard.",
    "截图和屏幕录制功能需要「屏幕录制」权限。请前往：": "Screenshot and recording features require Screen Recording permission. Go to:",
    "系统设置 → 隐私与安全性 → 屏幕录制": "System Settings → Privacy & Security → Screen Recording",
    "在列表中找到 ClipVault 并启用。如果已启用但仍不生效，可以取消勾选后重新勾选，然后重启 ClipVault。": "Find ClipVault in the list and enable it. If already enabled but not working, uncheck and recheck, then restart ClipVault.",
    "请检查以下几点：": "Please check the following:",
    "确认你已经在设置中配置了快捷键（初始安装时没有默认快捷键）": "Confirm you've configured hotkeys in settings (no defaults on fresh install)",
    "确保快捷键没有与其他应用冲突": "Make sure hotkeys don't conflict with other apps",
    "快捷键必须包含至少一个修饰键（⌘ / ⌃ / ⌥ / ⇧）": "Hotkeys must include at least one modifier key (⌘ / ⌃ / ⌥ / ⇧)",
    "尝试重新设置快捷键：先清除，再重新录入": "Try resetting the hotkey: clear first, then re-record",
    "请确认以下几点：": "Please confirm the following:",
    "你可以分别自定义三种数据的存储位置：": "You can customize the storage location for three types of data:",
    "设置 → 存储位置": "Settings → Storage Location",
    "点击「修改路径」按钮选择新的存储目录。": 'Click the "Change Path" button to select a new storage directory.',
    "ClipVault 支持 39 种语言。默认跟随系统语言，也可以手动切换：": "ClipVault supports 39 languages. Default follows system language, or switch manually:",
    "设置 → 通用 → 界面语言": "Settings → General → Interface Language",
    "选择目标语言后，需要重启 App 才能完全生效。": "After selecting a language, restart the App for full effect.",
    "点击任何图片类型的记录进入详情页，你会看到「OCR 识别」按钮。点击后，ClipVault 使用 Apple Vision 框架在本地识别图片中的文字，识别结果可以一键复制。": 'Click any image record to enter details, you\'ll see the "OCR Recognition" button. ClipVault uses Apple Vision framework to locally recognize text in images, with one-click copy of results.',
    "OCR 处理完全在本地进行，不会上传图片到任何服务器。": "OCR processing is entirely local — no images are uploaded to any server.",
    "不会。": "No.",
    "如果上述内容没有解决你的问题，欢迎通过以下方式联系我们。我们通常会在 48 小时内回复。": "If the above didn't solve your issue, feel free to contact us. We typically reply within 48 hours.",
    "发送邮件时请附上你的 macOS 版本和 ClipVault 版本号，以便我们更快定位问题。": "Please include your macOS version and ClipVault version in the email to help us locate the issue faster.",
    "首页": "Home",
    "技术支持": "Support",
    "隐私政策": "Privacy",
    "⚠ 权限相关": "⚠ Permissions",
    "⚠ 配置相关": "⚠ Configuration",
    "⚠ 功能相关": "⚠ Feature",
    "ℹ 功能相关": "ℹ Feature",
    "🔒 隐私相关": "🔒 Privacy",
}


def process_html(filepath, translations, en_title, zh_title):
    """Process an HTML file to default to English."""
    content = read_file(filepath)
    
    # 1. Change html lang
    content = content.replace('<html lang="zh-Hans">', '<html lang="en">')
    
    # 2. Change title
    old_title_match = re.search(r'<title>([^<]+)</title>', content)
    if old_title_match:
        content = content.replace(f'<title>{old_title_match.group(1)}</title>', f'<title>{en_title}</title>')
    
    # 3. Change meta description if present
    # (skip for now, not all files have it)
    
    # 4. Change button label from EN to 中文
    content = content.replace('<span class="lang-label">EN</span>', '<span class="lang-label">中文</span>')
    
    # 5. For existing data-zh/data-en spans that show Chinese default, change to English default
    def fix_data_spans(m):
        full = m.group(0)
        zh = m.group(1)
        en = m.group(2)
        inner = m.group(3)
        # If inner text matches zh text (Chinese default), switch to English
        if inner.strip() == zh.strip() or any(ord(c) > 0x4e00 for c in inner if c.isalpha()):
            return f'data-zh="{zh}" data-en="{en}">{en}<'
        return full
    
    content = re.sub(r'data-zh="([^"]*)" data-en="([^"]*)">(.*?)<', fix_data_spans, content, flags=re.DOTALL)
    
    # 6. Wrap bare Chinese text in spans with data-zh/data-en
    for zh, en in translations.items():
        # Escape for regex
        zh_escaped = re.escape(zh)
        # Only match if not already inside a data-zh attribute
        # Simple approach: replace bare text that's between > and <
        # This handles text nodes
        pattern = f'>\\s*{zh_escaped}\\s*<'
        replacement = f'><span data-zh="{zh}" data-en="{en}">{en}</span><'
        content = re.sub(pattern, replacement, content)
    
    # 7. Replace the script section - remove TreeWalker and dictionary
    # Find and replace the translation script
    script_pattern = r"(function\(\)\s*\{[\s\S]*?const K = 'declaration_lang';[\s\S]*?const T = \{[\s\S]*?\};[\s\S]*?function gL\(\)\{return localStorage\.getItem\(K\)\|\|'zh'\}[\s\S]*?\}\);[\s\n]*\}\)\(\);"
    
    new_script = f"""(function(){{
        var K='declaration_lang';
        function gL(){{return localStorage.getItem(K)||'en';}}
        function sL(l){{localStorage.setItem(K,l);}}
        function apply(lang){{
            document.querySelectorAll('[data-zh]').forEach(function(el){{el.textContent=lang==='zh'?el.getAttribute('data-zh'):el.getAttribute('data-en');}});
            document.documentElement.lang=lang==='zh'?'zh-Hans':'en';
            document.title=lang==='zh'?'{zh_title}':'{en_title}';
            var btn=document.getElementById('langToggle');
            if(btn)btn.querySelector('.lang-label').textContent=lang==='zh'?'EN':'中文';
        }}
        document.addEventListener('DOMContentLoaded',function(){{
            var lang=gL();if(lang==='zh')apply('zh');
            var btn=document.getElementById('langToggle');
            if(btn)btn.addEventListener('click',function(){{var next=gL()==='zh'?'en':'zh';sL(next);apply(next);}});
        }});
    }})();"""
    
    content = re.sub(script_pattern, new_script, content)
    
    # Also try alternate pattern
    if "const T = {" in content:
        # More aggressive: replace the entire IIFE containing the dictionary
        alt_pattern = r"\(function\(\)\s*\{\s*const K = 'declaration_lang';\s*const T = \{[^}]+(?:\{[^}]*\}[^}]*)*\};\s*function gL\(\)[^}]+\}[\s\S]*?\}\)\(\);"
        content = re.sub(alt_pattern, new_script, content)
    
    # Fallback: just fix gL default if dictionary removal failed
    content = content.replace("return localStorage.getItem(K)||'zh'", "return localStorage.getItem(K)||'en'")
    
    # Fix lang switching direction
    content = content.replace("lang==='en' ? el.getAttribute('data-en') : el.getAttribute('data-zh')", 
                             "lang==='zh' ? el.getAttribute('data-zh') : el.getAttribute('data-en')")
    content = content.replace("lang==='en' ? 'en' : 'zh-Hans'",
                             "lang==='zh' ? 'zh-Hans' : 'en'")
    content = content.replace("lang==='en' ? '中文' : 'EN'",
                             "lang==='zh' ? 'EN' : '中文'")
    content = content.replace("if(gL()==='en') apply('en')",
                             "var lang=gL();if(lang==='zh')apply('zh')")
    content = content.replace("var next = gL()==='en' ? 'zh' : 'en'",
                             "var next=gL()==='zh'?'en':'zh'")
    
    write_file(filepath, content)


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✅ Wrote: {path}')


# Process ClipVault files
process_html(
    os.path.join(BASE, 'ClipVault/index.html'),
    CLIPVAULT_INDEX_TRANSLATIONS,
    'ClipVault — Cyberpunk Clipboard Manager',
    'ClipVault — 赛博朋克剪贴板管理器'
)

process_html(
    os.path.join(BASE, 'ClipVault/privacy.html'),
    CLIPVAULT_PRIVACY_TRANSLATIONS,
    'ClipVault - Privacy Policy',
    'ClipVault - 隐私政策'
)

process_html(
    os.path.join(BASE, 'ClipVault/support.html'),
    CLIPVAULT_SUPPORT_TRANSLATIONS,
    'ClipVault - Technical Support',
    'ClipVault - 技术支持'
)

print("\n✅ ClipVault complete!")
