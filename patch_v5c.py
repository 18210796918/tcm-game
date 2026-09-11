import re

with open('/root/.openclaw/workspace/杏林街市/v5-preview.html','r',encoding='utf-8') as f:
    html = f.read()

# 1. Remove the arrow hint from seal-stamp area
old_seal = '''    <div style="position:relative;">
      <!-- Arrow hint -->
      <div style="position:absolute;right:75px;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:6px;animation:float 2s ease-in-out infinite;">
        <span style="font-size:12px;color:#c62828;font-weight:700;white-space:nowrap;">解锁进阶 ➜</span>
      </div>
      <div class="seal-stamp" id="seal-unlock" onclick="goToUnlockPage()" style="cursor:pointer;">
        <span style="font-size:22px;">🗝️</span>
        <span style="font-size:10px;">杏林百方</span>
      </div>
    </div>'''

new_seal = '''    <div class="seal-stamp" id="seal-unlock" onclick="goToUnlockPage()" style="cursor:pointer;">
      <span style="font-size:22px;">🗝️</span>
      <span style="font-size:10px;">杏林百方</span>
    </div>'''

html = html.replace(old_seal, new_seal)

# 2. Add unlock hint to the progress card below
old_progress = '''  <div class="card" style="text-align:center;">
    <div style="font-size:13px;color:#5d4037;line-height:1.8;margin-bottom:10px;">
      🏮 您已研习 <strong id="result-progress-count">0</strong> / 24 剂名方
    </div>
    <div style="font-size:12px;color:#8d6e63;margin-bottom:8px;">
      尚有百方典籍藏于杏林深处...
    </div>
  </div>'''

new_progress = '''  <div class="card" style="text-align:center;">
    <div style="font-size:13px;color:#5d4037;line-height:1.8;margin-bottom:10px;">
      🏮 您已研习 <strong id="result-progress-count">0</strong> / 24 剂名方
    </div>
    <div style="font-size:12px;color:#8d6e63;margin-bottom:8px;">
      尚有百方典籍藏于杏林深处...
    </div>
    <div style="margin-top:12px;padding-top:12px;border-top:1px dashed rgba(198,40,40,0.2);">
      <div style="font-size:12px;color:#c62828;font-weight:700;margin-bottom:6px;">🔓 进阶挑战：杏林百方</div>
      <div style="font-size:11px;color:#8d6e63;margin-bottom:8px;">四诊合参 · 悬壶济世 · 百剂名方</div>
      <button onclick="goToUnlockPage()" style="padding:8px 20px;background:linear-gradient(145deg,#c62828,#b71c1c);color:white;border:none;border-radius:10px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit;">
        🗝️ 解锁进阶 ➜
      </button>
    </div>
  </div>'''

html = html.replace(old_progress, new_progress)

with open('/root/.openclaw/workspace/杏林街市/v5-preview.html','w',encoding='utf-8') as f:
    f.write(html)

print("v5 fixes applied:")
print("- Removed all locked: true from 24 formulas")
print("- Moved '解锁进阶' arrow from seal to progress card")
print("- Added unlock button in '您已研习' section")
