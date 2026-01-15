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
    <link rel="icon" href="./assets/logo.png" type="image/svg+xml">
    <title>马烨主义（修订） 第{display_id}条 - {title}</title>
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
            margin: 30;
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
        /*
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        */
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <header>
        <nav class="navbar">
            <a href="../index.html" class="nav-brand"><img src="/assets/logo.png" width=40px>  马烨主义</a>
            <p><strong>全世界的马烨主义者联合起来</strong></p>
            <div class="nav-links">
                <a href="../index.html">首页</a>
            </div>
        </nav>
        <!-- 面包屑导航 -->
        <div class="breadcrumb">
            <a href="../index.html">首页</a> &gt; 
            <span>第{display_id}条</span>
        </div>
    </header>
    
    
    
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
        window.onload = function() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }};
        // 快速跳转功能
        function jumpToArticle() {{
            const input = document.getElementById('jumpInput');
            let num = parseInt(input.value);
            
            if (isNaN(num) || num < 1 || num > 91) {{
                alert('请输入有效的编号 (1-91)');
                input.focus();
                return;
            }}
            
            // 跳转到对应条文
            if (num !== {id}) {{
                smoothNavigate(num + '.html');
            }} else {{
                alert('当前已经是第' + num + '条');
            }}
        }}

        function changeArticle(num) {{
            // 跳转到对应条文
            if (num !== {id}) {{
                smoothNavigate(num + '.html');
            }} else {{
                alert('当前已经是第' + num + '条');
            }}
        }}

        function smoothNavigate(url) {{
            // 先添加淡出效果
            //document.body.style.opacity = '0';
            //document.body.style.transition = 'opacity 0.2s ease';
            
            setTimeout(() => {{
                window.location.href = url;
            }}, 200);
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
    
    prev_btn = f'<button class="nav-btn" onclick="changeArticle({article_num-1})">←上一条</button>' if has_prev else '<button class="nav-btn disabled">← 上一条</button>'
    next_btn = f'<button class="nav-btn" onclick="changeArticle({article_num+1})">下一条→</button>' if has_next else '<button class="nav-btn disabled">下一条→</button>'
    
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

print("✅ 修订版首页生成完成！")