import re

# Read v3
with open('/root/.openclaw/workspace/杏林街市/v3-preview.html','r',encoding='utf-8') as f:
    html = f.read()

# 1. Change seal-stamp to unlock stamp in result page
html = html.replace(
    '<div class="seal-stamp">\n      <span>杏林</span>\n      <span>妙手</span>\n    </div>',
    '<div class="seal-stamp" id="seal-unlock" onclick="goToUnlockPage()" style="cursor:pointer;">\n      <span>🔓</span>\n      <span style="font-size:11px;">杏林百方</span>\n    </div>'
)

# 2. Add progress card before share card in result page
old_share = '''  <div class="card" style="text-align:center;">
    <div style="font-size:15px;font-weight:700;color:#5d4037;margin-bottom:12px;">📤 分享药方笺</div>'''
new_share = '''  <div class="card" style="text-align:center;">
    <div style="font-size:13px;color:#5d4037;line-height:1.8;margin-bottom:10px;">
      🏮 大夫已研习 <strong id="result-progress-count">0</strong> / 24 剂名方
    </div>
    <div style="font-size:12px;color:#8d6e63;margin-bottom:8px;">
      尚有百方典籍藏于杏林深处...
    </div>
  </div>

  <div class="card" style="text-align:center;">
    <div style="font-size:15px;font-weight:700;color:#5d4037;margin-bottom:12px;">📤 分享药方笺</div>'''
html = html.replace(old_share, new_share, 1)

# 3. Replace old course lock page with new古风NPC unlock page
old_course_lock = '''<!-- ==================== SCREEN: COURSE LOCK ==================== -->
<div class="screen" id="screen-course-lock">
  <div class="header-bar">
    <button class="back-btn" onclick="goBack('screen-shop')">←</button>
    <h1>🔒 课程锁定</h1>
    <p>杏林学堂 · 深度解析</p>
  </div>

  <div style="text-align:center;padding:40px 20px;">
    <div style="font-size:80px;margin-bottom:16px;">🔐</div>
    <div style="font-size:22px;font-weight:700;color:#3e2723;margin-bottom:8px;">
      <span id="lock-formula-name">温经汤</span>
    </div>
    <div style="font-size:13px;color:#8d6e63;margin-bottom:24px;">
      <span id="lock-formula-source">《金匮要略》</span>
    </div>
  </div>

  <div class="card" style="text-align:center;">
    <div style="font-size:15px;font-weight:700;color:#c62828;margin-bottom:12px;">📚 杏林学堂课程</div>
    <div style="font-size:14px;color:#5d4037;line-height:1.8;margin-bottom:16px;">
      此方收录于杏林学堂深度解析课程，包含：<br>
      📖 古籍原文逐句解读<br>
      🌿 君臣佐使配伍精讲<br>
      📐 方义原理深度剖析<br>
      💊 药材辨识与煎服要点
    </div>
    <div style="font-size:28px;font-weight:900;color:#c62828;margin-bottom:8px;">
      ¥19.9
    </div>
    <div style="font-size:12px;color:#8d6e63;margin-bottom:16px;">
      解锁全部120剂名方深度课程
    </div>
    <button class="btn-primary" onclick="buyCourse()">
      🔓 立即解锁课程
    </button>
    <button class="btn-primary btn-secondary" onclick="goBack('screen-shop')" style="margin-top:10px;">
      ← 返回街市
    </button>
  </div>

  <div style="height:80px;"></div>
</div>'''

new_unlock_page = '''<!-- ==================== SCREEN: UNLOCK 杏林百方 ==================== -->
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
      <p style="margin-bottom:12px;">🏮 <em>"大夫留步！老朽观大夫在杏林街市已习得二十余剂名方，医术初成，可喜可贺。"</em></p>
      <p style="margin-bottom:12px;">📜 <em>"然杏林之道，博大精深。近日又有百位疑难杂症患者前来求诊，或外感风寒，或内伤七情，或虚实夹杂……小老儿这厢藏有百剂传世名方正缺一位悬壶济世的大夫。"</em></p>
      <p style="margin-bottom:12px;">🎋 <em>"大夫可愿接过这《杏林百方》典籍，以四诊合参之法，望闻问切、辨证论治，为苍生解忧？"</em></p>
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
</div>

<!-- ==================== SCREEN: 四诊合参 ==================== -->
<div class="screen" id="screen-sizhen">
  <div class="header-bar">
    <button class="back-btn" onclick="goToStreet()">←</button>
    <h1>🩺 四诊合参</h1>
    <p>望闻问切 · 辨证论治</p>
    <span class="collection-mini" id="sizhen-score">声望 0</span>
  </div>

  <div class="card" style="margin-top:12px;text-align:center;">
    <div style="font-size:14px;font-weight:700;color:#c62828;margin-bottom:8px;">
      🏥 杏林诊堂 · 第 <span id="sizhen-level">1</span> 位患者
    </div>
    <div style="font-size:13px;color:#8d6e63;">
      大夫，有患者前来求诊，请四诊合参，施以良方
    </div>
  </div>

  <!-- Patient Card -->
  <div class="card" style="margin-top:12px;background:linear-gradient(145deg,#fdf8e8,#f5edd8);">
    <div style="text-align:center;margin-bottom:12px;">
      <div style="font-size:60px;margin-bottom:4px;" id="patient-avatar">🤒</div>
      <div style="font-size:16px;font-weight:700;color:#3e2723;" id="patient-name">风寒客</div>
      <div style="font-size:12px;color:#8d6e63;" id="patient-desc">恶寒发热三日</div>
    </div>

    <div style="font-size:14px;color:#5d4037;line-height:1.9;margin-bottom:12px;" id="patient-symptoms">
      <div style="margin-bottom:6px;"><strong>👁️ 望诊：</strong>面色微白，舌苔薄白</div>
      <div style="margin-bottom:6px;"><strong>👂 闻诊：</strong>鼻鸣声重，呼吸微促</div>
      <div style="margin-bottom:6px;"><strong>💬 问诊：</strong>恶寒发热，汗出恶风，头身疼痛，鼻鸣干呕</div>
      <div><strong>🫳 切诊：</strong>脉浮缓，一息四至</div>
    </div>
  </div>

  <div style="font-size:13px;font-weight:700;color:#c62828;margin:16px 16px 10px;">
    📜 请大夫从典籍名方中择一方剂：
  </div>

  <div id="sizhen-options" style="padding:0 16px;">
    <!-- Options injected by JS -->
  </div>

  <div style="height:80px;"></div>
</div>

<!-- ==================== SCREEN: 四诊结果 ==================== -->
<div class="screen" id="screen-sizhen-result">
  <div class="header-bar">
    <button class="back-btn" onclick="nextSizhen()">←</button>
    <h1 id="sizhen-result-title">🎉 辨证正确</h1>
    <p id="sizhen-result-sub">大夫妙手回春</p>
  </div>

  <div style="text-align:center;padding:32px 20px 20px;">
    <div style="font-size:80px;margin-bottom:12px;" id="sizhen-result-emoji">🎊</div>
    <div style="font-size:20px;font-weight:700;color:#3e2723;margin-bottom:8px;" id="sizhen-result-text">
      辨证精准，用药如神！
    </div>
  </div>

  <div class="card">
    <div style="font-size:14px;color:#5d4037;line-height:1.9;" id="sizhen-result-detail">
      <!-- Detail injected by JS -->
    </div>
  </div>

  <button class="btn-primary" onclick="nextSizhen()" id="btn-next-sizhen">
    🩺 接诊下一位
  </button>
  <button class="btn-primary btn-secondary" onclick="goToStreet()">
    🏮 返回杏林街市
  </button>

  <div style="height:80px;"></div>
</div>'''

html = html.replace(old_course_lock, new_unlock_page)

# Write v4
with open('/root/.openclaw/workspace/杏林街市/v4-preview.html','w',encoding='utf-8') as f:
    f.write(html)

print("v4 template created with new screens")
