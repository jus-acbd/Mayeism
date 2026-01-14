# create_all_revised_final_fixed.py
import os
import json
from datetime import datetime

print("=== 马烨主义修订版网站生成器（最终版） ===")
print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 1. 创建detail目录
os.makedirs('detail', exist_ok=True)

# 2. 读取修订版数据
try:
    with open('articles_revised.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    print(f"✅ 读取到 {len(articles)} 条修订版数据")
except FileNotFoundError:
    print("❌ 找不到 articles_revised.json 文件")
    print("请先运行 generate_revised_data_final.py")
    exit(1)

# 3. 创建详情页模板（使用无前导零文件名）
detail_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>马烨主义（修订） 第{{display_id}}条 - {{title}}</title>
    <style>
        /* 基础重置 */
        * {{
            box-sizing: border-box;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }}
        
        body {{
            background-color: #f8f9fa;
            color: #333;
            line-height: 1.6;
            margin: 0;
        }}
        
        /* 导航栏 */
        .navbar {{
            background: linear-gradient(135deg, #fa0f07 0%, #eeff00 100%);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }}
        
        .nav-brand {{
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
            color: white;
        }}
        
        .nav-links a {{
            color: white;
            text-decoration: none;
            margin-left: 20px;
        }}
        
        /* 面包屑导航 */
        .breadcrumb {{
            background-color: #dfd4d4;
            color: rgb(0, 0, 0);
            padding: 15px 20px;
            display: flex;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .breadcrumb a {{
            color: #db5b34;
            text-decoration: none;
        }}
        
        /* 条文内容区域 */
        .article-container {{
            padding: 40px 30px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .article-header {{
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}
        
        .article-number {{
            font-size: 3.5rem;
            font-weight: bold;
            color: #fa0f07;
            margin-bottom: 10px;
        }}
        
        .article-title {{
            font-size: 2rem;
            color: #2c3e50;
            margin-bottom: 20px;
            line-height: 1.3;
        }}
        
        .article-meta {{
            color: #7f8c8d;
            font-size: 0.9rem;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        
        .article-content {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            margin-bottom: 40px;
        }}
        
        .content-section {{
            margin-bottom: 30px;
        }}
        
        .content-section h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}
        
        .content-text {{
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        /* 特殊标记 */
        .special-note {{
            background-color: #fff3cd;
            padding: 20px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .feature-list {{
            list-style-type: none;
            padding-left: 0;
            margin: 15px 0;
        }}
        
        .feature-list li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}
        
        .feature-list li:before {{
            content: "•";
            color: #fa0f07;
            font-size: 1.2em;
            position: absolute;
            left: 10px;
        }}
        
        /* 导航按钮 */
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            gap: 15px;
        }}
        
        .nav-btn {{
            padding: 12px 25px;
            background-color: #db5b34;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: background-color 0.3s;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            text-align: center;
            flex: 1;
            max-width: 200px;
        }}
        
        .nav-btn:hover {{
            background-color: #b92929;
        }}
        
        .nav-btn.disabled {{
            background-color: #cccccc;
            cursor: not-allowed;
            opacity: 0.6;
        }}
        
        /* 快速跳转 */
        .quick-jump {{
            display: flex;
            gap: 10px;
            margin: 20px 0;
            align-items: center;
        }}
        
        .jump-input {{
            width: 120px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }}
        
        .jump-btn {{
            padding: 10px 15px;
            background-color: #db5b34;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
        }}
        
        /* 底部 */
        footer {{
            background-color: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
            margin-top: 50px;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .article-container {{
                padding: 20px;
            }}
            
            .article-number {{
                font-size: 2.5rem;
            }}
            
            .article-title {{
                font-size: 1.5rem;
            }}
            
            .article-content {{
                padding: 20px;
            }}
            
            .nav-buttons {{
                flex-direction: column;
            }}
            
            .nav-btn {{
                max-width: 100%;
                width: 100%;
            }}
            
            .quick-jump {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .jump-input {{
                width: 100%;
            }}
        }}
        
        @media (max-width: 480px) {{
            .navbar {{
                padding: 15px 20px;
                flex-direction: column;
                gap: 10px;
            }}
            
            .nav-links {{
                display: flex;
                gap: 15px;
                margin-left: 0;
            }}
            
            .nav-links a {{
                margin-left: 0;
            }}
            
            .breadcrumb {{
                padding: 10px;
                font-size: 0.9rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <a href="../index_revised.html" class="nav-brand">马烨主义（修订版）</a>
        <div class="nav-links">
            <a href="../index.html">首页</a>
            <a href="../index.html">原始版本</a>
        </div>
    </nav>
    
    <!-- 面包屑导航 -->
    <div class="breadcrumb">
        <a href="../index.html">首页</a> &gt; 
        <span>第{display_id}条</span>
    </div>
    
    <!-- 快速跳转 -->
    <div class="article-container">
        <div class="quick-jump">
            <input type="number" id="jumpInput" class="jump-input" placeholder="输入编号 (1-91)" min="1" max="91">
            <button class="jump-btn" onclick="jumpToArticle()">快速跳转</button>
        </div>
        
        <div class="article-header">
            <div class="article-number">第{display_id}条</div>
            <h1 class="article-title">{title}</h1>
            <div class="article-meta">
                <span>📁 分类：{category}</span>
                <span>📅 更新：2026-01-14</span>
                <span>🔢 编号：{display_id}/091</span>
            </div>
        </div>
        
        <div class="article-content">
            <div class="content-section">
                <h3>📋 内容</h3>
                <div class="content-text">{content}</div>
            </div>
            
            {special_content}
            
            {revision_note}
            
            <div class="content-section">
                <h3>📝 解读</h3>
                <div class="content-text">
                </div>
            </div>
        </div>
        
        <!-- 导航按钮 -->
        <div class="nav-buttons">
            {prev_btn}
            <a href="../index.html" class="nav-btn">返回列表</a>
            {next_btn}
        </div>
    </div>
    
    <!-- 底部 -->
    <footer>
        <p>马烨主义（修订版）汇总 © 2026 | 第{display_id}条/共91条</p>
        <p style="margin-top: 5px;">修订日期：2026年1月14日 | 支持输入 1、01、001 格式跳转</p>
        <p style="margin-top: 5px;">页面文件：{id}.html</p>
    </footer>
    
    <script>
        // 快速跳转功能
        function jumpToArticle() {{
            const input = document.getElementById('jumpInput');
            let num = parseInt(input.value);
            
            if (isNaN(num) || num < 1 || num > 91) {{
                alert('请输入有效的条文编号 (1-91)');
                input.focus();
                return;
            }}
            
            // 跳转到对应条文
            if (num !== {id}) {{
                window.location.href = num + '.html';
            }} else {{
                alert('当前已经是第' + num + '条');
            }}
        }}
        
        // 监听输入框回车键
        document.getElementById('jumpInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                jumpToArticle();
            }}
        }});
        
        // 键盘导航
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'ArrowLeft' && {{has_prev}}) {{
                window.location.href = '{{prev_file}}';
            }} else if (e.key === 'ArrowRight' && {{has_next}}) {{
                window.location.href = '{{next_file}}';
            }} else if (e.key === 'Home') {{
                window.location.href = '1.html';
            }} else if (e.key === 'End') {{
                window.location.href = '91.html';
            }}
        }});
        
        // 自动识别禁止性和建议性词汇
        document.addEventListener('DOMContentLoaded', function() {{
            const content = document.querySelector('.content-text');
            const prohibitions = ['不要', '禁止', '避免', '不能', '别', '不宜', '禁止', '禁止使用'];
            const recommendations = ['应该', '可以', '建议', '尽量', '必须', '应当'];
            
            let hasProhibition = false;
            let hasRecommendation = false;
            let prohibitionWords = [];
            let recommendationWords = [];
            
            const text = content.textContent;
            prohibitions.forEach(word => {{
                if (text.includes(word)) {{
                    hasProhibition = true;
                    prohibitionWords.push(word);
                }}
            }});
            
            recommendations.forEach(word => {{
                if (text.includes(word)) {{
                    hasRecommendation = true;
                    recommendationWords.push(word);
                }}
            }});
            
            
            
            // 自动聚焦跳转输入框
            document.getElementById('jumpInput').focus();
            
            // 页面加载时自动滚动到顶部
            window.scrollTo(0, 0);
        }});
    </script>
</body>
</html>'''

# 4. 特殊标记的条文
special_articles = [26, 35, 36, 40]

# 5. 生成所有详情页
print("\n正在生成详情页 (1.html, 2.html, ..., 91.html)...")
for i, article in enumerate(articles):
    article_id = article['id']  # 无前导零：1, 2, 3, ..., 91
    article_num = int(article_id)
    display_id = article_id.zfill(3)  # 显示用：001, 002, ..., 091
    
    # 确定导航按钮
    prev_file = f"{article_num-1}.html" if article_num > 1 else "#"
    next_file = f"{article_num+1}.html" if article_num < 91 else "#"
    has_prev = article_num > 1
    has_next = article_num < 91
    
    prev_display = str(article_num-1).zfill(3)
    next_display = str(article_num+1).zfill(3)
    
    prev_btn = f'<a href="{prev_file}" class="nav-btn">← 上一条</a>' if has_prev else '<button class="nav-btn disabled">← 上一条</button>'
    next_btn = f'<a href="{next_file}" class="nav-btn">下一条→</a>' if has_next else '<button class="nav-btn disabled">下一条→</button>'
    
    # 特殊内容
    special_content = ""
    # if article_num in special_articles:
    #     special_content = '''
    #     <div class="highlight">
    #         <h4 style="color: #ff5722;">✨ 重点条文</h4>
    #         <p>本条在修订版中被特别标记，具有重要指导意义。</p>
    #     </div>
    #     '''
    
    # 修订说明
    revision_note = ""
    if article_num == 55:
        revision_note = '''
        <div class="revision-note">
            <strong>修订历史：</strong>本条内容在修订版中进行了大幅修改，原内容已被替换。
        </div>
        '''
    
    # 处理第90条的特殊内容格式
    content = article['content']
    if article_num == 90:
        content = "马烨的特征包括："
        features = ["飞点", "漏球", "马烨菠萝", "马烨孔雀", "氪佬", "实况大蛇"]
        feature_list = "\n".join([f'<li>{feature}</li>' for feature in features])
        content += f'<ul class="feature-list">{feature_list}</ul>'
    
    # 生成页面内容
    page_content = detail_template.format(
        id=article_id,
        display_id=display_id,
        title=article['title'],
        category=article['category'],
        content=content,
        special_content=special_content,
        revision_note=revision_note,
        prev_btn=prev_btn,
        next_btn=next_btn,
        has_prev=str(has_prev).lower(),
        has_next=str(has_next).lower(),
        prev_file=prev_file,
        next_file=next_file
    )
    
    # 写入文件，使用无前导零文件名
    filename = f'detail/{article_id}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_content)
    
    if (i + 1) % 10 == 0:
        print(f"  已生成 {i+1}/91 个详情页")

print("✅ 详情页生成完成！")

# 6. 生成修订版首页
print("\n正在生成修订版首页...")

# 读取HTML列表
try:
    with open('full_list_revised.html', 'r', encoding='utf-8') as f:
        full_list_html = f.read()
except FileNotFoundError:
    print("❌ 找不到 full_list_revised.html 文件")
    print("请先运行 generate_revised_data_final.py")
    exit(1)

# 首页模板 - 修复了正则表达式转义问题
index_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>马烨主义（修订版） - 共91条详细解读</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }}
        
        body {{
            background-color: #f8f9fa;
            color: #333;
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* 头部样式 */
        header {{
            background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
            color: white;
            padding: 40px 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.8rem;
            margin-bottom: 10px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        }}
        
        .version-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 1rem;
            display: inline-block;
            margin-bottom: 15px;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 25px;
        }}
        
        /* 搜索区域 */
        .search-container {{
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .search-box {{
            display: flex;
            max-width: 600px;
            gap: 10px;
        }}
        
        .search-box input {{
            flex: 1;
            padding: 14px 20px;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
        }}
        
        .search-box button {{
            background-color: #45a049;
            color: white;
            border: none;
            padding: 0 25px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: background-color 0.3s;
            white-space: nowrap;
        }}
        
        .search-box button:hover {{
            background-color: #388E3C;
        }}
        
        .search-tips {{
            font-size: 0.9rem;
            margin-top: 10px;
            opacity: 0.9;
        }}
        
        /* 快速跳转 */
        .quick-jump {{
            display: flex;
            gap: 10px;
            margin: 15px 0;
            align-items: center;
        }}
        
        .jump-input {{
            width: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }}
        
        .jump-btn {{
            padding: 10px 15px;
            background-color: #45a049;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        
        /* 统计卡片 */
        .stats {{
            display: flex;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            flex: 1;
            min-width: 200px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 1rem;
        }}
        
        /* 修订说明 */
        .revision-info {{
            background: #e8f5e9;
            padding: 25px;
            border-radius: 8px;
            margin: 30px 0;
            border-left: 5px solid #4CAF50;
        }}
        
        .revision-info h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        /* 分类统计 */
        .category-stats {{
            margin: 40px 0;
        }}
        
        .category-badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .category-badge {{
            background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .category-badge:hover {{
            transform: translateY(-2px);
        }}
        
        h2 {{
            color: #2c3e50;
            border-left: 5px solid #4CAF50;
            padding-left: 15px;
            margin-bottom: 25px;
            font-size: 1.8rem;
        }}
        
        /* 条文列表 */
        .articles-section {{
            margin: 40px 0;
        }}
        
        .article-list {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }}
        
        .article-header {{
            display: grid;
            grid-template-columns: 80px 1fr 150px;
            background-color: #e8f5e9;
            padding: 15px 20px;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 1px solid #eaeaea;
        }}
        
        .article-row {{
            display: grid;
            grid-template-columns: 80px 1fr 150px;
            padding: 18px 20px;
            border-bottom: 1px solid #f0f0f0;
            text-decoration: none;
            color: inherit;
            transition: background-color 0.2s;
            cursor: pointer;
        }}
        
        .article-row:hover {{
            background-color: #f1f8e9;
        }}
        
        .article-row:nth-child(even) {{
            background-color: #fcfcfc;
        }}
        
        .article-row:nth-child(even):hover {{
            background-color: #f5f5f5;
        }}
        
        .article-number {{
            color: #4CAF50;
            font-weight: bold;
        }}
        
        .article-title {{
            color: #2c3e50;
        }}
        
        .article-category {{
            color: #7f8c8d;
            font-size: 0.9rem;
        }}
        
        /* 特别标记 */
        .article-row.special {{
            border-left: 4px solid #FF9800;
            background-color: #fff8e1;
        }}
        
        .article-row.special:hover {{
            background-color: #ffecb3;
        }}
        
        /* 版本切换 */
        .version-switch {{
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 8px;
        }}
        
        .version-switch a {{
            color: #4CAF50;
            text-decoration: none;
            font-weight: bold;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}
        
        .version-switch a:hover {{
            background-color: #e8f5e9;
        }}
        
        /* 底部 */
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #eaeaea;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9rem;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2.2rem;
            }}
            
            .article-header, .article-row {{
                grid-template-columns: 60px 1fr 100px;
            }}
            
            .search-box {{
                flex-direction: column;
            }}
            
            .search-box input, .search-box button {{
                width: 100%;
            }}
            
            .stat-card {{
                min-width: calc(50% - 10px);
            }}
        }}
        
        @media (max-width: 480px) {{
            body {{
                padding: 10px;
            }}
            
            header {{
                padding: 25px 20px;
            }}
            
            .article-header, .article-row {{
                grid-template-columns: 1fr;
                gap: 5px;
            }}
            
            .stat-card {{
                min-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <!-- 头部区域 -->
    <header>
        <h1>马烨主义（修订版）</h1>
        <div class="version-badge">修订版 2026.01 | 文件名：1.html, 2.html, ..., 91.html</div>
        <div class="subtitle">在马烨主义基础上进行合理化修订，更符合社会规范</div>
        
        <div class="search-container">
            <p>智能搜索：支持多种输入格式</p>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="输入编号、关键词或内容...">
                <button onclick="searchArticle()">搜索条文</button>
            </div>
            
            <div class="quick-jump">
                <input type="number" id="quickJump" class="jump-input" placeholder="1-91" min="1" max="91">
                <button class="jump-btn" onclick="quickJump()">快速跳转</button>
            </div>
            
            <div class="search-tips">
                <strong>输入提示：</strong>
                <span>编号支持：1、01、001 等格式</span> | 
                <span>关键词如：应该、不要、必须</span> | 
                <span>分类如：基本原则、行为准则</span>
            </div>
        </div>
    </header>
    
    <!-- 修订说明 -->
    <div class="revision-info">
        <h3>📋 修订说明</h3>
        <p>本修订版在原马烨主义基础上进行了合理化调整，主要修订原则包括：</p>
        <ul style="margin-top: 10px; padding-left: 20px;">
            <li>将极端要求调整为合理建议</li>
            <li>强调文明礼貌和社会规范</li>
            <li>修正不合理或矛盾的内容</li>
            <li>增加实用性和可操作性</li>
            <li>保持马烨主义的核心精神</li>
        </ul>
        <p style="margin-top: 15px;">修订日期：2026年1月14日 | 页面命名：无前导零数字 (1.html, 2.html, ...)</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">91</div>
            <div class="stat-label">条文总数</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{category_count}</div>
            <div class="stat-label">分类数量</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">2026</div>
            <div class="stat-label">修订年份</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{special_count}</div>
            <div class="stat-label">重点条文</div>
        </div>
    </div>
    
    <!-- 版本切换 -->
    <div class="version-switch">
        <p>查看：<a href="index.html">原始马烨主义版本</a> | <strong>当前：修订版</strong> | 页面文件：detail/1.html ~ detail/91.html</p>
    </div>
    
    <!-- 分类统计 -->
    <div class="category-stats">
        <h2>条文分类统计</h2>
        <div class="category-badges">
            {category_badges}
        </div>
    </div>
    
    <!-- 条文列表 -->
    <section class="articles-section">
        <h2>条文列表（共91条）</h2>
        <div class="article-list">
            <div class="article-header">
                <div>编号</div>
                <div>概览</div>
                <div>分类</div>
            </div>
            
            {full_list_html}
        </div>
    </section>
    
    <!-- 底部 -->
    <footer>
        <p>马烨主义（修订版）汇总 © 2026 | 最后更新: 2026年1月14日 | 共收录91条核心条文</p>
        <p style="margin-top: 5px;">页面文件命名：1.html, 2.html, ..., 91.html | 支持 1、01、001 格式输入</p>
        <p style="margin-top: 5px;">全世界的马烨主义者联合起来</p>
    </footer>
    
    <script>
        // 快速跳转功能
        function quickJump() {{
            const input = document.getElementById('quickJump');
            let num = parseInt(input.value);
            
            if (isNaN(num) || num < 1 || num > 91) {{
                alert('请输入有效的条文编号 (1-91)');
                input.focus();
                return;
            }}
            
            // 跳转到对应条文
            window.location.href = `./detail/${{num}}.html`;
        }}
        
        // 监听快速跳转输入框回车键
        document.getElementById('quickJump').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                quickJump();
            }}
        }});
        
        // 搜索功能
        function searchArticle() {{
            const input = document.getElementById('searchInput').value.trim();
            if (!input) {{
                alert('请输入搜索内容');
                return;
            }}
            
            // 检查是否是编号搜索（1、01、001 等格式）
            const numMatch = input.match(/^0*(\\d{{1,3}})$/);
            if (numMatch) {{
                const num = parseInt(numMatch[1]);
                if (num >= 1 && num <= 91) {{
                    // 直接跳转，不需要前导零
                    window.location.href = `./detail/${{num}}.html`;
                    return;
                }}
            }}
            
            // 关键词搜索
            const searchTerm = input.toLowerCase();
            const articles = document.querySelectorAll('.article-row');
            let found = false;
            let firstMatch = null;
            
            articles.forEach(article => {{
                const title = article.querySelector('.article-title').textContent.toLowerCase();
                const number = article.querySelector('.article-number').textContent.toLowerCase();
                const category = article.querySelector('.article-category').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || number.includes(searchTerm) || category.includes(searchTerm)) {{
                    // 高亮显示匹配项
                    article.style.backgroundColor = '#e8f5e9';
                    article.style.borderLeft = '4px solid #4CAF50';
                    found = true;
                    
                    // 记录第一个匹配项
                    if (!firstMatch) {{
                        firstMatch = article;
                    }}
                }} else {{
                    article.style.backgroundColor = '';
                    article.style.borderLeft = '';
                }}
            }});
            
            if (found && firstMatch) {{
                // 滚动到第一个匹配项
                firstMatch.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }} else {{
                alert('未找到包含 "' + input + '" 的条文\\n\\n可以尝试：\\n1. 输入编号如 "1"、"01" 或 "001"\\n2. 输入关键词如 "应该"、"不要"\\n3. 输入分类如 "基本原则"\\n4. 输入内容关键词');
            }}
        }}
        
        // 监听搜索框回车键
        document.getElementById('searchInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                searchArticle();
            }}
        }});
        
        // 页面加载后聚焦搜索框
        window.onload = function() {{
            document.getElementById('searchInput').focus();
            
            // 标记特殊条文
            const specialArticles = [{special_articles_str}];
            specialArticles.forEach(num => {{
                const article = document.querySelector('[href="./detail/' + num + '.html"]');
                if (article) {{
                    article.classList.add('special');
                }}
            }});
            
            // 分类筛选功能
            const categoryBadges = document.querySelectorAll('.category-badge');
            categoryBadges.forEach(badge => {{
                badge.addEventListener('click', function() {{
                    const categoryText = this.textContent;
                    const category = categoryText.split(' ')[0];
                    const articles = document.querySelectorAll('.article-row');
                    
                    articles.forEach(article => {{
                        const articleCategory = article.querySelector('.article-category').textContent;
                        if (articleCategory === category) {{
                            article.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            article.style.backgroundColor = '#fff3cd';
                            article.style.transition = 'background-color 2s';
                            
                            setTimeout(() => {{
                                article.style.backgroundColor = '';
                            }}, 2000);
                        }}
                    }});
                }});
            }});
            
            // 添加点击清除高亮功能
            document.addEventListener('click', function(e) {{
                if (!e.target.closest('.search-container') && !e.target.closest('.category-badges')) {{
                    const articles = document.querySelectorAll('.article-row');
                    articles.forEach(article => {{
                        article.style.backgroundColor = '';
                        article.style.borderLeft = '';
                    }});
                }}
            }});
        }};
    </script>
</body>
</html>'''

# 7. 统计分类信息
categories = {}
special_articles = [26, 35, 36, 40]

for article in articles:
    category = article['category']
    if category in categories:
        categories[category] += 1
    else:
        categories[category] = 1

# 生成分类徽章
category_badges = []
for category, count in sorted(categories.items()):
    badge = f'<span class="category-badge" title="点击跳转到{category}分类">{category} ({count}条)</span>'
    category_badges.append(badge)

category_badges_html = '\n'.join(category_badges)

# 生成首页内容 - 修复了模板变量名
index_content = index_template.format(
    category_count=len(categories),
    special_count=len(special_articles),
    category_badges=category_badges_html,
    full_list_html=full_list_html,
    special_articles_str=','.join(map(str, special_articles))
)

# 写入首页文件
with open('index_revised.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print("✅ 修订版首页生成完成！")

print(f"""
🎉 生成完成！项目结构：
├── index_revised.html       # 修订版首页
├── articles_revised.json    # 修订版数据
├── detail/                  # 详情页目录（使用 1.html 格式）
│   ├── 1.html
│   ├── 2.html
│   ├── 3.html
│   ├── ...
│   └── 91.html
├── generate_revised_data_final.py   # 修订版数据生成
├── create_all_revised_final_fixed.py      # 完整生成脚本（修复版）
└── index.html               # 原始版本（保留）

📁 详细信息：
- 总条文数：91条
- 分类数量：{len(categories)}类
- 特殊条文：{len(special_articles)}条
- 页面命名：1.html, 2.html, ..., 91.html
- 支持输入：1、01、001 等格式

🔗 使用说明：
1. 双击打开 index_revised.html 查看修订版
2. 输入 1、01、001 都能跳转到第1条
3. 首页有快速跳转功能
4. 详情页支持键盘导航（左右箭头）
5. 可以按分类筛选条文

✨ 特色功能：
- ✅ 支持多种编号格式输入
- ✅ 快速跳转输入框
- ✅ 分类筛选高亮
- ✅ 键盘导航支持
- ✅ 修订说明自动识别
- ✅ 响应式设计
- ✅ 无前导零文件名
""")