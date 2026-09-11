import re

with open('/root/.openclaw/workspace/杏林街市/v4-preview.html','r',encoding='utf-8') as f:
    html = f.read()

# Add CSS for sizhen options before </style>
old_style_end = '/* ===== Responsive tweaks ===== */\n@media (max-width: 430px) {\n  .app-container { max-width: 100%; }\n}\n</style>'
new_style_end = '''/* ===== 四诊合参 Options ===== */
.sizhen-option {
  background: linear-gradient(145deg, #fdf8e8, #f0e6d0);
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 2px 6px rgba(62,39,35,0.06);
  display: flex;
  align-items: center;
  gap: 12px;
}
.sizhen-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(62,39,35,0.1);
  border-color: rgba(198,40,40,0.2);
}
.sizhen-option.correct {
  border-color: #2e7d32;
  background: linear-gradient(145deg, #e8f5e9, #fdf8e8);
  box-shadow: 0 4px 12px rgba(46,125,50,0.15);
}
.sizhen-option.wrong {
  border-color: #c62828;
  background: rgba(198,40,40,0.06);
  opacity: 0.55;
}
.sizhen-option .opt-num {
  width: 28px; height: 28px;
  border-radius: 50%;
  background: linear-gradient(145deg, #c62828, #b71c1c);
  color: white;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.sizhen-option .opt-name {
  font-size: 15px;
  font-weight: 700;
  color: #3e2723;
}
.sizhen-option .opt-source {
  font-size: 11px;
  color: #8d6e63;
}
.sizhen-option .opt-info { flex: 1; }

/* ===== NPC Speech Bubble ===== */
.npc-speech {
  background: linear-gradient(145deg, #fdf8e8, #f5edd8);
  border-radius: 16px;
  padding: 18px;
  margin: 12px 16px;
  position: relative;
  box-shadow: 0 2px 8px rgba(62,39,35,0.08);
  border: 1px solid rgba(139,110,99,0.1);
  font-size: 14px;
  color: #5d4037;
  line-height: 1.9;
}
.npc-speech::before {
  content: '';
  position: absolute;
  top: -8px; left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid #fdf8e8;
}
.npc-speech em {
  font-style: normal;
  color: #3e2723;
}

/* ===== Responsive tweaks ===== */
@media (max-width: 430px) {
  .app-container { max-width: 100%; }
}
</style>'''

html = html.replace(old_style_end, new_style_end)

# Now add JS logic before the closing </script> tag
# Find the last </script> before </body>
old_script_end = '''// Init
updateCollectionDisplay();
</script>'''

new_script_end = '''// ============================================
// 杏林百方 UNLOCK PAGE
// ============================================
function goToUnlockPage() {
  showScreen('screen-unlock-bai');
}

function buyBaiFang() {
  showToast('🏮 《杏林百方》即将上线，敬请期待！');
}

// ============================================
// 四诊合参 GAME DATA
// ============================================
const PATIENTS = [
  {
    id: 1,
    name: '风寒客',
    avatar: '🤒',
    desc: '恶寒发热三日',
    wang: '面色微白，舌苔薄白',
    wen: '鼻鸣声重，呼吸微促',
    wen2: '恶寒发热，汗出恶风，头身疼痛，鼻鸣干呕',
    qie: '脉浮缓，一息四至',
    correct: 'guizhi',
    correctName: '桂枝汤',
    explanation: '患者外感风寒，营卫不和，桂枝汤解肌发表、调和营卫，正合此证。',
    options: [
      { id: 'guizhi', name: '桂枝汤', source: '《伤寒论》' },
      { id: 'xiaochaihu', name: '小柴胡汤', source: '《伤寒论》' },
      { id: 'liuwei', name: '六味地黄丸', source: '《小儿药证直诀》' },
      { id: 'sijunzi', name: '四君子汤', source: '《太平惠民和剂局方》' }
    ]
  },
  {
    id: 2,
    name: '少阳客',
    avatar: '🥶',
    desc: '寒热往来已五日',
    wang: '面色微黄，舌苔薄白',
    wen: '口苦咽干，气息平和',
    wen2: '往来寒热，胸胁苦满，默默不欲饮食，心烦喜呕',
    qie: '脉弦，两关不调',
    correct: 'xiaochaihu',
    correctName: '小柴胡汤',
    explanation: '邪在少阳，半表半里，小柴胡汤和解少阳，使枢机得利，则寒热除、胁满消。',
    options: [
      { id: 'guizhi', name: '桂枝汤', source: '《伤寒论》' },
      { id: 'xiaochaihu', name: '小柴胡汤', source: '《伤寒论》' },
      { id: 'baidu', name: '败毒散', source: '《太平惠民和剂局方》' },
      { id: 'lizhong', name: '理中丸', source: '《伤寒论》' }
    ]
  },
  {
    id: 3,
    name: '肾阴虚',
    avatar: '😫',
    desc: '腰膝酸软半年余',
    wang: '面色潮红，舌红少苔',
    wen: '口干咽燥，声低气短',
    wen2: '腰膝酸软，头晕目眩，耳鸣耳聋，盗汗遗精，手足心热',
    qie: '脉细数，尺部尤甚',
    correct: 'liuwei',
    correctName: '六味地黄丸',
    explanation: '肾阴亏虚，虚火内扰，六味地黄丸滋阴补肾、三补三泻，使阴复火降。',
    options: [
      { id: 'sijunzi', name: '四君子汤', source: '《太平惠民和剂局方》' },
      { id: 'guipi', name: '归脾汤', source: '《正体类要》' },
      { id: 'liuwei', name: '六味地黄丸', source: '《小儿药证直诀》' },
      { id: 'lizhong', name: '理中丸', source: '《伤寒论》' }
    ]
  },
  {
    id: 4,
    name: '肝郁客',
    avatar: '😤',
    desc: '情志不畅二月余',
    wang: '面色萎黄，舌淡红',
    wen: '叹息频频，语声低微',
    wen2: '两胁作痛，头痛目眩，口燥咽干，神疲食少，月经不调',
    qie: '脉弦而虚，左关尤甚',
    correct: 'xiaoyao',
    correctName: '逍遥散',
    explanation: '肝郁血虚脾弱，逍遥散疏肝、养血、健脾三者并行，使肝郁得疏、血虚得养。',
    options: [
      { id: 'xiaoyao', name: '逍遥散', source: '《太平惠民和剂局方》' },
      { id: 'siwu', name: '四物汤', source: '《太平惠民和剂局方》' },
      { id: 'suanzaoren', name: '酸枣仁汤', source: '《金匮要略》' },
      { id: 'guizhi', name: '桂枝汤', source: '《伤寒论》' }
    ]
  }
];

let sizhenState = {
  currentIndex: 0,
  score: 0,
  answered: false
};

function startSizhen() {
  sizhenState.currentIndex = 0;
  sizhenState.score = 0;
  sizhenState.answered = false;
  loadPatient(0);
  showScreen('screen-sizhen');
}

function loadPatient(idx) {
  const p = PATIENTS[idx];
  if (!p) {
    showToast('🏮 大夫已接诊全部患者，杏林声望 +' + sizhenState.score);
    goToStreet();
    return;
  }
  sizhenState.answered = false;
  document.getElementById('sizhen-level').textContent = idx + 1;
  document.getElementById('sizhen-score').textContent = '声望 ' + sizhenState.score;
  document.getElementById('patient-avatar').textContent = p.avatar;
  document.getElementById('patient-name').textContent = p.name;
  document.getElementById('patient-desc').textContent = p.desc;

  const symptomsHtml = `
    <div style="margin-bottom:6px;"><strong>👁️ 望诊：</strong>${p.wang}</div>
    <div style="margin-bottom:6px;"><strong>👂 闻诊：</strong>${p.wen}</div>
    <div style="margin-bottom:6px;"><strong>💬 问诊：</strong>${p.wen2}</div>
    <div><strong>🫳 切诊：</strong>${p.qie}</div>
  `;
  document.getElementById('patient-symptoms').innerHTML = symptomsHtml;

  const optsEl = document.getElementById('sizhen-options');
  optsEl.innerHTML = '';
  p.options.forEach((opt, i) => {
    const div = document.createElement('div');
    div.className = 'sizhen-option';
    div.dataset.id = opt.id;
    div.onclick = () => selectSizhenOption(div, opt.id, p);
    div.innerHTML = `
      <div class="opt-num">${String.fromCharCode(65 + i)}</div>
      <div class="opt-info">
        <div class="opt-name">${opt.name}</div>
        <div class="opt-source">${opt.source}</div>
      </div>
    `;
    optsEl.appendChild(div);
  });
}

function selectSizhenOption(el, optId, patient) {
  if (sizhenState.answered) return;
  sizhenState.answered = true;

  const isCorrect = optId === patient.correct;
  const options = document.querySelectorAll('.sizhen-option');

  options.forEach(opt => {
    if (opt.dataset.id === patient.correct) {
      opt.classList.add('correct');
    } else if (opt.dataset.id === optId && !isCorrect) {
      opt.classList.add('wrong');
    }
  });

  if (isCorrect) {
    sizhenState.score += 10;
    showSizhenResult(true, patient);
  } else {
    showSizhenResult(false, patient);
  }
}

function showSizhenResult(isCorrect, patient) {
  const title = document.getElementById('sizhen-result-title');
  const sub = document.getElementById('sizhen-result-sub');
  const emoji = document.getElementById('sizhen-result-emoji');
  const text = document.getElementById('sizhen-result-text');
  const detail = document.getElementById('sizhen-result-detail');
  const btn = document.getElementById('btn-next-sizhen');

  if (isCorrect) {
    title.textContent = '🎉 辨证正确';
    sub.textContent = '大夫妙手回春';
    emoji.textContent = '🎊';
    text.textContent = '辨证精准，用药如神！';
    detail.innerHTML = `
      <div style="margin-bottom:10px;"><strong>📜 处方：</strong>${patient.correctName}</div>
      <div style="margin-bottom:10px;"><strong>💡 方解：</strong>${patient.explanation}</div>
      <div style="color:#8d6e63;font-size:12px;">🏮 杏林声望 +10</div>
    `;
    btn.textContent = '🩺 接诊下一位';
  } else {
    title.textContent = '😔 辨证有误';
    sub.textContent = '还需勤加研习';
    emoji.textContent = '📖';
    text.textContent = '此证当用「' + patient.correctName + '」';
    detail.innerHTML = `
      <div style="margin-bottom:10px;"><strong>📜 正解：</strong>${patient.correctName}</div>
      <div style="margin-bottom:10px;"><strong>💡 方解：</strong>${patient.explanation}</div>
      <div style="color:#8d6e63;font-size:12px;">🏮 大夫莫急，杏林之道贵在积累</div>
    `;
    btn.textContent = '🩺 继续研习';
  }

  showScreen('screen-sizhen-result');
}

function nextSizhen() {
  sizhenState.currentIndex++;
  if (sizhenState.currentIndex >= PATIENTS.length) {
    showToast('🏮 大夫已接诊全部患者，杏林声望 ' + sizhenState.score);
    goToStreet();
  } else {
    loadPatient(sizhenState.currentIndex);
    showScreen('screen-sizhen');
  }
}

// ============================================
// RESULT PAGE PROGRESS
// ============================================
function updateResultProgress() {
  const el = document.getElementById('result-progress-count');
  if (el) el.textContent = gameState.collected.length;
}

// Hook into existing goToResult
const originalGoToResult = goToResult;
goToResult = function() {
  originalGoToResult();
  updateResultProgress();
};

// Init
updateCollectionDisplay();
</script>'''

html = html.replace(old_script_end, new_script_end)

with open('/root/.openclaw/workspace/杏林街市/v4-preview.html','w',encoding='utf-8') as f:
    f.write(html)

print("v4 patched with game logic")
