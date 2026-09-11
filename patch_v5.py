import re

with open('/root/.openclaw/workspace/杏林街市/v5-preview.html','r',encoding='utf-8') as f:
    html = f.read()

# 1. 删除首页"杏林学堂"推广卡片
# 找到饮子铺/老妪下方的那个card并删除
old_promo = '''    <!-- Course Promo -->
    <div class="card" style="margin:16px;margin-top:20px;text-align:center;">
      <div style="font-size:16px;font-weight:700;color:#c62828;margin-bottom:10px;">📚 杏林学堂</div>
      <div style="font-size:13px;color:#5d4037;line-height:1.7;margin-bottom:12px;">
        120剂传世名方深度解析<br>
        古籍溯源 · 君臣佐使 · 临床应用
      </div>
      <div style="font-size:24px;font-weight:900;color:#c62828;margin-bottom:4px;">¥19.9</div>
      <div style="font-size:11px;color:#8d6e63;margin-bottom:12px;">系列课程 · 永久有效</div>
      <button class="btn-primary" onclick="buyCourse()" style="width:auto;display:inline-block;padding:12px 28px;font-size:14px;">
        📖 了解课程
      </button>
    </div>

    <button class="enter-btn" onclick="enterStreet()" style="margin-top:8px;">'''

new_promo = '''    <button class="enter-btn" onclick="enterStreet()" style="margin-top:16px;">'''

html = html.replace(old_promo, new_promo)

# 2. 全局替换"大夫" → 根据语境替换
# "大夫已研习" → "您已研习"
# "有患者前来求诊，请四诊合参" → 不用改"大夫"
# "大夫留步" → "君子留步"
html = html.replace('大夫已研习', '您已研习')
html = html.replace('大夫留步', '君子留步')
html = html.replace('观大夫在杏林街市', '观您在杏林街市')
html = html.replace('大夫医术初成', '您医术初成')
html = html.replace('正缺一位悬壶济世的大夫', '正缺一位悬壶济世的杏林学子')
html = html.replace('大夫可愿接过', '您可愿接过')
html = html.replace('为苍生解忧', '为杏林传承尽力')
html = html.replace('大夫，有患者前来求诊', '有患者前来求诊')
html = html.replace('请大夫从典籍名方中', '请从典籍名方中')
html = html.replace('大夫妙手回春', '用药精准')
html = html.replace('大夫莫急', '莫急')
html = html.replace('大夫已接诊全部患者', '您已接诊全部患者')

# 3. 饮子铺图标🥤 → 🫖 (茶壶)
html = html.replace(
    '''<div class="building" onclick="enterShop('yinzipu')">
          <span class="building-icon">🥤</span>''',
    '''<div class="building" onclick="enterShop('yinzipu')">
          <span class="building-icon">🫖</span>'''
)

# 4. 老妪图标👵 → 🧣 (古风围巾/头巾意象)
html = html.replace(
    '''<div class="building" onclick="enterShop('oldwoman')">
          <span class="building-icon">🧓</span>''',
    '''<div class="building" onclick="enterShop('oldwoman')">
          <span class="building-icon">🧣</span>'''
)

# 5. 结果页seal-stamp上的🔒换成CSS古风锁
# 先添加CSS
old_seal_css = '''.seal-stamp span { line-height: 1.3; }'''
new_seal_css = '''.seal-stamp span { line-height: 1.3; }

/* 古风锁 */
.gufeng-lock {
  position: relative;
  width: 40px;
  height: 40px;
  margin: 0 auto 4px;
}
.gufeng-lock::before {
  content: '';
  position: absolute;
  top: 0; left: 50%;
  transform: translateX(-50%);
  width: 20px; height: 14px;
  border: 3px solid white;
  border-radius: 10px 10px 0 0;
  border-bottom: none;
}
.gufeng-lock::after {
  content: '';
  position: absolute;
  bottom: 0; left: 50%;
  transform: translateX(-50%);
  width: 28px; height: 22px;
  background: white;
  border-radius: 3px;
}
.gufeng-lock-keyhole {
  position: absolute;
  bottom: 6px; left: 50%;
  transform: translateX(-50%);
  width: 4px; height: 8px;
  background: #c62828;
  border-radius: 2px;
  z-index: 2;
}
.gufeng-lock-keyhole::before {
  content: '';
  position: absolute;
  top: -3px; left: 50%;
  transform: translateX(-50%);
  width: 6px; height: 6px;
  background: #c62828;
  border-radius: 50%;
}'''

html = html.replace(old_seal_css, new_seal_css)

# 替换seal-stamp内容
old_seal = '''    <div class="seal-stamp" id="seal-unlock" onclick="goToUnlockPage()" style="cursor:pointer;">
      <span>🔓</span>
      <span style="font-size:11px;">杏林百方</span>
    </div>'''

new_seal = '''    <div class="seal-stamp" id="seal-unlock" onclick="goToUnlockPage()" style="cursor:pointer;">
      <div class="gufeng-lock"><div class="gufeng-lock-keyhole"></div></div>
      <span style="font-size:10px;position:relative;z-index:2;">杏林百方</span>
    </div>'''

html = html.replace(old_seal, new_seal)

# 6. 优化"杏林百方"解锁页 - 加入NPC游戏规则和付费预览
old_unlock = '''<!-- ==================== SCREEN: UNLOCK 杏林百方 ==================== -->
<div class="screen" id="screen-unlock-bai">
  <div class="header-bar">
    <button class="back-btn" onclick="goBack('screen-result')">←</button>
    <h1>📜 杏林百方</h1>
    <p>悬壶济世 · 典籍传承</p>
  </div>

  <div style="text-align:center;padding:24px 20px 16px;">
    <div style="font-size:72px;margin-bottom:12px;animation:float 3s ease-in-out infinite;">👨‍🦳</div>
    <div style="font-size:18px;font-weight:700;color:#3e2723;margin-bottom:4px;">老馆主</div>
    <div style="font-size:12px;color:#8d6e63;">杏林藏书阁守阁人</div>
  </div>

  <div class="card" style="margin-top:0;">
    <div style="font-size:14px;color:#5d4037;line-height:2;margin-bottom:16px;">
      <p style="margin-bottom:12px;">🏮 <em>"君子留步！老朽观您在杏林街市已习得二十余剂名方，医术初成，可喜可贺。"</em></p>
      <p style="margin-bottom:12px;">📜 <em>"然杏林之道，博大精深。近日又有百位疑难杂症患者前来求诊，或外感风寒，或内伤七情，或虚实夹杂……小老儿这厢藏有百剂传世名方正缺一位悬壶济世的杏林学子。"</em></p>
      <p style="margin-bottom:12px;">🎋 <em>"您可愿接过这《杏林百方》典籍，以四诊合参之法，望闻问切、辨证论治，为杏林传承尽力？"</em></p>
    </div>

    <div style="background:linear-gradient(145deg,#fff8e1,#fdf8e8);border-radius:14px;padding:18px;margin:16px 0;border:2px dashed #c62828;">
      <div style="font-size:16px;font-weight:700;color:#c62828;margin-bottom:10px;text-align:center;">📚 《杏林百方》典籍</div>
      <div style="font-size:13px;color:#5d4037;line-height:1.9;">
        ✅ 百剂传世名方 · 古籍原文记载<br>
        ✅ 四诊合参 · 悬壶济世进阶挑战<br>
        ✅ 望闻问切 · 辨证论治实战<br>
        ✅ 君臣佐使 · 配伍精深度解析
      </div>
    </div>

    <div style="text-align:center;margin:20px 0;">
      <div style="font-size:32px;font-weight:900;color:#c62828;margin-bottom:4px;">¥9.9</div>
      <div style="font-size:12px;color:#8d6e63;margin-bottom:16px;">一次解锁 · 永久研习 · 百方尽收</div>
      <button class="btn-primary" onclick="buyBaiFang()">
        🏮 接典济世
      </button>
      <button class="btn-primary btn-secondary" onclick="goBack('screen-result')" style="margin-top:10px;">
        ← 容后再议
      </button>
    </div>
  </div>

  <div style="height:80px;"></div>
</div>'''

new_unlock = '''<!-- ==================== SCREEN: UNLOCK 杏林百方 ==================== -->
<div class="screen" id="screen-unlock-bai">
  <div class="header-bar">
    <button class="back-btn" onclick="goBack('screen-result')">←</button>
    <h1>📜 杏林百方</h1>
    <p>典籍传承 · 杏林深处</p>
  </div>

  <!-- NPC Intro -->
  <div style="text-align:center;padding:24px 20px 16px;">
    <div style="font-size:72px;margin-bottom:12px;animation:float 3s ease-in-out infinite;">👨‍🦳</div>
    <div style="font-size:18px;font-weight:700;color:#3e2723;margin-bottom:4px;">老馆主</div>
    <div style="font-size:12px;color:#8d6e63;">杏林藏书阁守阁人</div>
  </div>

  <div class="card" style="margin-top:0;">
    <!-- NPC Dialogue -->
    <div style="font-size:14px;color:#5d4037;line-height:2;margin-bottom:16px;">
      <p style="margin-bottom:12px;">🏮 <em>"君子留步！老朽观您在杏林街市已习得二十余剂名方，医术初成，可喜可贺。"</em></p>
      <p style="margin-bottom:12px;">📜 <em>"然杏林之道，博大精深。近日又有百位疑难杂症患者前来求诊，或外感风寒，或内伤七情，或虚实夹杂……小老儿这厢藏有百剂传世名方正缺一位悬壶济世的杏林学子。"</em></p>
      <p style="margin-bottom:12px;">🎋 <em>"您可愿接过这《杏林百方》典籍，以四诊合参之法，望闻问切、辨证论治，为杏林传承尽力？"</em></p>
    </div>

    <!-- Game Rules -->
    <div style="background:linear-gradient(145deg,#fff8e1,#fdf8e8);border-radius:14px;padding:18px;margin:16px 0;border:1px solid rgba(198,40,40,0.15);">
      <div style="font-size:15px;font-weight:700;color:#c62828;margin-bottom:12px;text-align:center;">🎮 四诊合参 · 进阶挑战</div>
      <div style="font-size:13px;color:#5d4037;line-height:2;">
        <div style="margin-bottom:8px;">📜 <strong>玩法：</strong>患者前来求诊，您需通过<strong>望闻问切</strong>四诊信息，从典籍名方中择一方剂施以救治。</div>
        <div style="margin-bottom:8px;">👁️ <strong>望诊：</strong>观其面色、舌苔、形态</div>
        <div style="margin-bottom:8px;">👂 <strong>闻诊：</strong>听其声息、嗅其气味</div>
        <div style="margin-bottom:8px;">💬 <strong>问诊：</strong>询其症状、病程、起居</div>
        <div style="margin-bottom:8px;">🫳 <strong>切诊：</strong>探其脉象、虚实寒热</div>
        <div>🏮 <strong>辨证：</strong>四诊合参，明辨证型，施以良方</div>
      </div>
    </div>

    <!-- Preview Content -->
    <div style="background:linear-gradient(145deg,#e8f5e9,#f1f8e9);border-radius:14px;padding:18px;margin:16px 0;border:1px solid rgba(74,124,89,0.2);">
      <div style="font-size:15px;font-weight:700;color:#2e7d32;margin-bottom:12px;text-align:center;">📚 解锁内容预览</div>
      <div style="font-size:13px;color:#5d4037;line-height:1.9;">
        ✅ 百剂传世名方 · 古籍原文记载<br>
        ✅ 四诊合参 · 悬壶济世进阶挑战<br>
        ✅ 望闻问切 · 辨证论治实战演练<br>
        ✅ 君臣佐使 · 配伍精深度解析<br>
        ✅ 药材实拍 · 辨识真伪古今对照
      </div>
    </div>

    <!-- Pricing -->
    <div style="text-align:center;margin:20px 0;">
      <div style="font-size:32px;font-weight:900;color:#c62828;margin-bottom:4px;">¥9.9</div>
      <div style="font-size:12px;color:#8d6e63;margin-bottom:16px;">一次解锁 · 永久研习 · 百方尽收</div>
      <button class="btn-primary" onclick="buyBaiFang()">
        🏮 接典济世
      </button>
      <button class="btn-primary btn-secondary" onclick="goBack('screen-result')" style="margin-top:10px;">
        ← 容后再议
      </button>
    </div>
  </div>

  <div style="height:80px;"></div>
</div>'''

html = html.replace(old_unlock, new_unlock)

# 7. 也修正四诊合参页面中的"大夫"
html = html.replace('请从典籍名方中择一方剂', '请从典籍名方中择一方剂')
html = html.replace('用药精准，杏林声望', '用药精准，杏林声望')

with open('/root/.openclaw/workspace/杏林街市/v5-preview.html','w',encoding='utf-8') as f:
    f.write(html)

print("v5 done:")
print("- 删除首页学堂推广卡片")
print("- 替换'大夫'称呼")
print("- 饮子铺🥤→🫖, 老妪🧓→🧣")
print("- 古风锁CSS图标")
print("- 优化杏林百方解锁页，加入游戏规则和预览")
