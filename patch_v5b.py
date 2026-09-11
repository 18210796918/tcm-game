import re

with open('/root/.openclaw/workspace/杏林街市/v5-preview.html','r',encoding='utf-8') as f:
    html = f.read()

# 1. Fix 饮子铺 HTML icon
html = html.replace(
    "onclick=\"enterShop('yinzipu')\">\n          <span class=\"building-icon\">🫖</span>",
    "onclick=\"enterShop('yinzipu')\">\n          <span class=\"building-icon\">🍵</span>"
)

# 2. Fix 老妪 HTML icon
html = html.replace(
    "onclick=\"enterShop('oldwoman')\">\n          <span class=\"building-icon\">🧣</span>",
    "onclick=\"enterShop('oldwoman')\">\n          <span class=\"building-icon\">👵</span>"
)

# 3. Fix 老妪 JS shopkeeper emoji
html = html.replace(
    "oldwoman: {\n    name: '老妪',\n    emoji: '🧣'",
    "oldwoman: {\n    name: '老妪',\n    emoji: '👵'"
)

# 4. Replace CSS lock seal with 🗝️ emoji + add arrow hint
old_seal = '''    <div class="seal-stamp" id="seal-unlock" onclick="goToUnlockPage()" style="cursor:pointer;">
      <div class="gufeng-lock"><div class="gufeng-lock-keyhole"></div></div>
      <span style="font-size:10px;position:relative;z-index:2;">杏林百方</span>
    </div>'''

new_seal = '''    <div style="position:relative;">
      <!-- Arrow hint -->
      <div style="position:absolute;right:75px;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:6px;animation:float 2s ease-in-out infinite;">
        <span style="font-size:12px;color:#c62828;font-weight:700;white-space:nowrap;">解锁进阶 ➜</span>
      </div>
      <div class="seal-stamp" id="seal-unlock" onclick="goToUnlockPage()" style="cursor:pointer;">
        <span style="font-size:22px;">🗝️</span>
        <span style="font-size:10px;">杏林百方</span>
      </div>
    </div>'''

html = html.replace(old_seal, new_seal)

# 5. Add missing goToUnlockPage and buyBaiFang functions
# Find a good insertion point - after goToStreet function
old_func = '''function goToStreet() {
  updateCollectionDisplay();
  showScreen('screen-welcome');
}

function enterStreet() {
  updateCollectionDisplay();
  showScreen('screen-welcome');
}'''

new_func = '''function goToStreet() {
  updateCollectionDisplay();
  showScreen('screen-welcome');
}

function enterStreet() {
  updateCollectionDisplay();
  showScreen('screen-welcome');
}

function goToUnlockPage() {
  showScreen('screen-unlock-bai');
}

function buyBaiFang() {
  showToast('🏮 《杏林百方》即将上线，敬请期待！');
}

function buyCourse() {
  showToast('📚 课程即将上线，敬请期待！');
}'''

html = html.replace(old_func, new_func)

# 6. Also fix the result progress hook if missing
if 'updateResultProgress' not in html:
    # Add it inside goToResult
    old_gtr = '''function goToResult() {
  const fid = gameState.currentFormula;
  const f = FORMULAS[fid];
  collectFormula(fid);
  updateCollectionDisplay();'''
    new_gtr = '''function goToResult() {
  const fid = gameState.currentFormula;
  const f = FORMULAS[fid];
  collectFormula(fid);
  updateCollectionDisplay();
  updateResultProgress();'''
    html = html.replace(old_gtr, new_gtr)
    
    # Add updateResultProgress function
    old_init = '''// Init
updateCollectionDisplay();'''
    new_init = '''function updateResultProgress() {
  const el = document.getElementById('result-progress-count');
  if (el) el.textContent = gameState.collected.length;
}

// Init
updateCollectionDisplay();'''
    html = html.replace(old_init, new_init)

with open('/root/.openclaw/workspace/杏林街市/v5-preview.html','w',encoding='utf-8') as f:
    f.write(html)

print("All v5 fixes applied")
