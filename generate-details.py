import os
import re
from datetime import datetime

# 创建detail目录
os.makedirs('detail', exist_ok=True)

# 马烨主义条文数据（从你的文档中提取）
articles = [
    {"id": "1", "title": "身上所有东西不可以正着带或正着穿", "category": "着装规范"},
    {"id": "2", "title": "内裤不能穿里面", "category": "着装规范"},
    {"id": "3", "title": "脖子长度不能少于总身高的99％", "category": "身体特征"},
    {"id": "4", "title": "每天必须新建一座度假区", "category": "日常行为"},
    {"id": "5", "title": "遇事先动手", "category": "行为准则"},
    {"id": "6", "title": "玩游戏没钱也氪金", "category": "娱乐活动"},
    {"id": "7", "title": "四肢不协调", "category": "身体特征"},
    {"id": "8", "title": "不能好好贴桌球", "category": "运动能力"},
    {"id": "9", "title": "毫无运动天赋", "category": "运动能力"},
    {"id": "10", "title": "作业字体不可以工整", "category": "学习要求"},
    {"id": "11", "title": "不能一个人单独放学", "category": "社交行为"},
    {"id": "12", "title": "必须整天和一名同姓泡在一起", "category": "社交行为"},
    {"id": "13", "title": "必须整天和一名异姓泡在一起", "category": "社交行为"},
    {"id": "14", "title": "遇事先狡辩", "category": "行为准则"},
    {"id": "15", "title": "每天必须说一句上海话", "category": "语言要求"},
    {"id": "16", "title": "每天必须用上海话骂一次人", "category": "语言要求"},
    {"id": "17", "title": "每天必须问候一次自己的主队", "category": "日常行为"},
    {"id": "18", "title": "每天必须问候一次别人的浮木", "category": "社交行为"},
    {"id": "19", "title": "必须长得像鲁迅", "category": "外貌特征"},
    {"id": "20", "title": "腰围不能长于1cm，胸围不能小于总身高的100％", "category": "身体特征"},
    {"id": "21", "title": "必须大眼睛，大鼻孔", "category": "外貌特征"},
    {"id": "22", "title": "每天必须听一遍Melody", "category": "娱乐活动"},
    {"id": "23", "title": "肌肉不可以长在正确的位置", "category": "身体特征"},
    {"id": "24", "title": "每天必须和一个人用上海话'册那'互骂", "category": "语言要求"},
    {"id": "25", "title": "每隔一段时间必须举行拳王争霸赛", "category": "娱乐活动"},
    {"id": "26", "title": "必须躺在别人怀里", "category": "社交行为"},
    {"id": "27", "title": "做操时不能拍前面", "category": "行为准则"},
    {"id": "28", "title": "必须喜欢一个人，且与ta做同一种运动", "category": "社交行为"},
    {"id": "29", "title": "遇事先问候对方浮木", "category": "语言要求"},
    {"id": "30", "title": "运动神经中枢必须瘫痪", "category": "身体特征"},
    {"id": "31", "title": "必须双逆足，双逆手，双逆头", "category": "身体特征"},
    {"id": "32", "title": "必须又高又帅", "category": "外貌特征"},
    {"id": "33", "title": "遇事必签条约", "category": "行为准则"},
    {"id": "34", "title": "唱歌必跑调", "category": "娱乐活动"},
    {"id": "35", "title": "必须坐摇摇椅", "category": "日常行为"},
    {"id": "36", "title": "必须吃对象的零食", "category": "社交行为"},
    {"id": "37", "title": "必须给对象抄答案", "category": "学习要求"},
    {"id": "38", "title": "被打必须说'让我还一下'", "category": "语言要求"},
    {"id": "39", "title": "马烨永远少女", "category": "基本原则"},
    {"id": "40", "title": "马烨尤思程简称'烨思'（yes）", "category": "基本原则"},
    {"id": "41", "title": "遇事先跳舞", "category": "行为准则"},
    {"id": "42", "title": "翻书包柜时必须留下好机会", "category": "日常行为"},
    {"id": "43", "title": "做数学题必须解出且正确且只能用手指比划几下", "category": "学习要求"},
    {"id": "44", "title": "包必须只有三个轮子", "category": "物品要求"},
    {"id": "45", "title": "洗澡时间不能超过两分钟", "category": "日常行为"},
    {"id": "46", "title": "上学必迟到", "category": "行为准则"},
    {"id": "47", "title": "每天起床时间不可早于7：39，上床时间不可早于上午7：38", "category": "日常行为"},
    {"id": "48", "title": "英语必须重默", "category": "学习要求"},
    {"id": "49", "title": "每天必须使用一次国际友好手势", "category": "行为准则"},
    {"id": "50", "title": "发际线必须高于头顶", "category": "外貌特征"},
    {"id": "51", "title": "跑圈必须压限速", "category": "运动能力"},
    {"id": "52", "title": "做操必须系鞋带", "category": "日常行为"},
    {"id": "53", "title": "臂展不能小于脖子长度的100％", "category": "身体特征"},
    {"id": "54", "title": "上课必须传纸条", "category": "学习要求"},
    {"id": "55", "title": "每天必须做七年级道法书P54正文第二段除去标点的第8，9个字至少两次", "category": "日常行为"},
    {"id": "56", "title": "马烨注意仪容仪表", "category": "基本原则"},
    {"id": "57", "title": "一次性必须戴4个口罩", "category": "着装规范"},
    {"id": "58", "title": "每个人必须过大于过，无任何用处", "category": "基本原则"},
    {"id": "59", "title": "出操和跑圈必须阅兵", "category": "行为准则"},
    {"id": "60", "title": "马烨肉汁鲜美", "category": "身体特征"},
    {"id": "61", "title": "马烨大月氏", "category": "基本原则"},
    {"id": "62", "title": "马烨没有yj", "category": "身体特征"},
    {"id": "63", "title": "马烨没有Diao", "category": "身体特征"},
    {"id": "64", "title": "马烨是格调", "category": "基本原则"},
    {"id": "65", "title": "马烨总是南征北战", "category": "行为准则"},
    {"id": "66", "title": "马烨一进教室就吵", "category": "行为准则"},
    {"id": "67", "title": "必须同时是gay和女同", "category": "社交行为"},
    {"id": "68", "title": "站着必须靠在别人肩上", "category": "社交行为"},
    {"id": "69", "title": "马烨必须跑不过女生", "category": "运动能力"},
    {"id": "70", "title": "马烨必须把口水喷别人包里", "category": "行为准则"},
    {"id": "71", "title": "必须被足球爆过头", "category": "运动能力"},
    {"id": "72", "title": "桌肚里必须有口罩", "category": "物品要求"},
    {"id": "73", "title": "马烨pg必须开花", "category": "身体特征"},
    {"id": "74", "title": "出操必须上厕所", "category": "行为准则"},
    {"id": "75", "title": "马烨随地大小便", "category": "行为准则"},
    {"id": "76", "title": "每年以一篇反思开头，一篇反思结尾", "category": "日常行为"},
    {"id": "77", "title": "人人皆为马烨", "category": "基本原则"},
    {"id": "78", "title": "马烨必须时时刻刻头顶鸡窝", "category": "外貌特征"},
    {"id": "79", "title": "马烨刚生下来就大小便失禁，连生活都不能自理", "category": "身体特征"},
    {"id": "80", "title": "必须是学校每位老师的媳妇", "category": "社交行为"},
    {"id": "81", "title": "人体器官必须和普通人长得镜像", "category": "身体特征"},
    {"id": "82", "title": "上课必须和别人眉目传情", "category": "学习要求"},
    {"id": "83", "title": "马烨可以是任何东西", "category": "基本原则"},
    {"id": "84", "title": "马烨是长颈漏斗的颈", "category": "身体特征"},
    {"id": "85", "title": "马烨头顶可选择顶一个富士山", "category": "外貌特征"},
    {"id": "86", "title": "百变马烨", "category": "基本原则"},
    {"id": "87", "title": "上课必须忘记坐下", "category": "学习要求"},
    {"id": "88", "title": "值周班长的名字必须被修改", "category": "行为准则"},
    {"id": "89", "title": "马烨属于外来入侵物种", "category": "基本原则"},
    {"id": "90", "title": "马烨是内卷迟到飞点漏球氪金大便", "category": "基本原则"},
    {"id": "91", "title": "马烨的未来考上一个好高中", "category": "基本原则"},
]

# 读取模板
with open('detail-template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 生成每个页面
for i, article in enumerate(articles):
    # 准备替换数据
    article_id = article["id"]
    article_num = int(article_id)
    
    # 确定导航链接
    prev_link = f"{article_num-1}.html" if article_num > 1 else "#"
    next_link = f"{article_num+1}.html" if article_num < 91 else "#"
    prev_disabled = "disabled" if article_num == 1 else ""
    next_disabled = "disabled" if article_num == 91 else ""
    
    # 构建内容
    content = f"<p><strong>内容：</strong>{article['title']}</p>"
    
    # 添加一些解释性内容
    if "必须" in article['title']:
        content += f"<p><strong>解读：</strong>本条为强制性要求，所有马烨主义者必须严格遵守。</p>"
    if "不能" in article['title'] or "不可以" in article['title']:
        content += f"<p><strong>解读：</strong>本条为禁止性规定，所有马烨主义者必须避免此类行为。</p>"
    
    # 特殊标记（根据你的文档）
    special_content = ""
    if article_num in [26, 35, 36, 40]:  # 你文档中标记的条目
        special_content = f"""
        <div class="highlight">
            <h4>✨ 特别说明</h4>
            <p>本条在马烨主义中具有特殊意义，建议重点关注。</p>
        </div>
        """
    
    # 生成页面内容
    page_content = template.replace("{编号}", article_id)
    page_content = page_content.replace("{标题}", article['title'])
    page_content = page_content.replace("{分类}", article['category'])
    page_content = page_content.replace("{内容正文}", content)
    page_content = page_content.replace("{特殊标记区域}", special_content)
    page_content = page_content.replace("{上一页链接}", prev_link)
    page_content = page_content.replace("{下一页链接}", next_link)
    page_content = page_content.replace("{上一页禁用}", prev_disabled)
    page_content = page_content.replace("{下一页禁用}", next_disabled)
    
    # 写入文件
    filename = f"detail/{article_id}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_content)
    
    print(f"已生成：{filename}")

print(f"\n✅ 完成！共生成91个详情页面。")