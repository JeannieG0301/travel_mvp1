/**
 * 新西兰行程规划 - 前端逻辑
 * API 地址：默认为同源，可通过 window.API_BASE 或 <script> 前定义覆盖
 */
const API_BASE = typeof window !== 'undefined' && window.API_BASE !== undefined ? window.API_BASE : '';

const form = document.getElementById('plan-form');
const submitBtn = document.getElementById('submit-btn');
const loading = document.getElementById('loading');
const errorEl = document.getElementById('error');
const resultEl = document.getElementById('result');

var STAGES = ['正在规划路线…', '正在安排每日行程…', '正在整理注意事项…'];

function showLoading() {
  loading.classList.remove('hidden');
  errorEl.classList.add('hidden');
  resultEl.classList.add('hidden');
  submitBtn.disabled = true;
  var stageEl = document.getElementById('loading-stage');
  stageEl.textContent = '';
  var idx = 0;
  stageEl.dataset.intervalId = setInterval(function () {
    stageEl.textContent = STAGES[idx % STAGES.length];
    idx += 1;
  }, 4000).toString();
}

function hideLoading() {
  var stageEl = document.getElementById('loading-stage');
  if (stageEl && stageEl.dataset.intervalId) {
    clearInterval(parseInt(stageEl.dataset.intervalId, 10));
    stageEl.dataset.intervalId = '';
  }
  stageEl.textContent = '';
  loading.classList.add('hidden');
  submitBtn.disabled = false;
}


function showError(msg, code) {
  var html = '<span class="error-msg">' + escapeHtml(msg) + '</span>';
  if (window.lastSubmitData) {
    html += ' <button type="button" id="btn-retry" class="btn-retry">重试</button>';
  }
  errorEl.innerHTML = html;
  errorEl.classList.remove('hidden');
  resultEl.classList.add('hidden');
  if (window.lastSubmitData) {
    document.getElementById('btn-retry').addEventListener('click', function () {
      doSubmit(window.lastSubmitData);
    });
  }
}

window.currentPlan = null;

function showResult(plan) {
  window.currentPlan = plan;
  errorEl.classList.add('hidden');
  document.getElementById('result-title').textContent = plan.title || '行程';
  document.getElementById('result-plan').innerHTML = '<h3><svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>行程总览</h3><p>' + escapeHtml(plan.plan || '') + '</p>';

  const daysHtml = [];
  (plan.days || []).forEach(function (d) {
    let html = '<div class="day-card"><h4>第 ' + d.day + ' 天</h4>';
    ['morning', 'afternoon', 'evening'].forEach(function (slotName) {
      const label = { morning: '上午', afternoon: '下午', evening: '晚上' }[slotName];
      const slotClass = { morning: 'slot-am', afternoon: 'slot-pm', evening: 'slot-eve' }[slotName];
      const slot = d[slotName] || {};
      const lines = [];
      if (slot.transport) lines.push('<span class="slot-line"><strong>交通：</strong>' + escapeHtml(slot.transport) + '</span>');
      if (slot.sights) lines.push('<span class="slot-line"><strong>景点：</strong>' + escapeHtml(slot.sights) + '</span>');
      if (slot.activities) lines.push('<span class="slot-line"><strong>活动：</strong>' + escapeHtml(slot.activities) + '</span>');
      if (slot.accommodation) lines.push('<span class="slot-line"><strong>住宿：</strong>' + escapeHtml(slot.accommodation) + '</span>');
      if (lines.length) html += '<div class="slot"><span class="slot-label ' + slotClass + '">' + label + '</span><div class="slot-body">' + lines.join('') + '</div></div>';
      else html += '<div class="slot"><span class="slot-label ' + slotClass + '">' + label + '</span><div class="slot-body">无安排</div></div>';
    });
    html += '</div>';
    daysHtml.push(html);
  });
  document.getElementById('result-days').innerHTML = '<h3><svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>按天行程</h3>' + daysHtml.join('');

  const tips = plan.tips || [];
  if (tips.length) {
    document.getElementById('result-tips').innerHTML = '<h3><svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>注意事项</h3><ul>' +
      tips.map(function (t) { return '<li>' + escapeHtml(t) + '</li>'; }).join('') + '</ul>';
    document.getElementById('result-tips').classList.remove('hidden');
  } else {
    document.getElementById('result-tips').innerHTML = '';
    document.getElementById('result-tips').classList.add('hidden');
  }

  var shareBtn = document.getElementById('btn-share-link');
  if (plan.share_id) {
    shareBtn.classList.remove('hidden');
    shareBtn.dataset.shareId = plan.share_id;
  } else {
    shareBtn.classList.add('hidden');
  }
  resultEl.classList.remove('hidden');
  resultEl.scrollIntoView({ behavior: 'smooth' });
}

function escapeHtml(s) {
  const div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}

function collectFormData() {
  const styles = [];
  document.querySelectorAll('#styles input[name="style"]:checked').forEach(function (cb) {
    styles.push(cb.value);
  });
  if (styles.length > 5) styles.length = 5;

  return {
    landing_city: document.getElementById('landing_city').value,
    region: document.getElementById('region').value,
    month: parseInt(document.getElementById('month').value, 10),
    days: parseInt(document.getElementById('days').value, 10),
    travelers: parseInt(document.getElementById('travelers').value, 10),
    landing_time: document.getElementById('landing_time').value || '',
    departure_time: document.getElementById('departure_time').value || '',
    styles: styles.length ? styles : null,
    budget_level: document.getElementById('budget_level').value || '',
    must_see: (document.getElementById('must_see').value || '').trim()
  };
}

function exportPdf() {
  var plan = window.currentPlan;
  var el = document.getElementById('result');
  if (!el || !plan) return;
  var clone = el.cloneNode(true);
  var actions = clone.querySelector('.result-actions');
  if (actions) actions.remove();
  var opt = {
    margin: 12,
    filename: (plan.title || '行程').replace(/[\\/:*?"<>|]/g, '_') + '.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };
  if (typeof html2pdf !== 'undefined') {
    html2pdf().set(opt).from(clone).save();
  }
}

function copyShareLink() {
  var btn = document.getElementById('btn-share-link');
  var id = btn && btn.dataset.shareId;
  if (!id) return;
  var path = (window.location.pathname || '/').replace(/\/?index\.html$/i, '') || '/';
  if (!path.endsWith('/')) path = path.replace(/\/?$/, '/');
  var url = (window.location.origin || '') + path + 'share.html?id=' + id;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(function () {
      btn.textContent = '已复制链接';
      setTimeout(function () { btn.textContent = '分享链接'; }, 2000);
    });
  } else {
    prompt('复制以下链接分享：', url);
  }
}

document.getElementById('btn-export-pdf').addEventListener('click', exportPdf);
document.getElementById('btn-share-link').addEventListener('click', copyShareLink);

async function doSubmit(data) {
  window.lastSubmitData = data;
  showLoading();
  try {
    const res = await fetch(API_BASE + '/api/generate-plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    var json;
    try {
      json = await res.json();
    } catch (parseErr) {
      // 502/503 等可能返回非 JSON（如 HTML），按超时/不可用处理，仍展示重试
      if (!res.ok && (res.status === 502 || res.status === 503 || res.status === 504)) {
        showError('生成超时或服务暂时不可用，请点击重试', 'TIMEOUT');
      } else {
        showError('服务返回异常，请点击重试', 'NETWORK_ERROR');
      }
      return;
    }
    if (!res.ok) {
      var code = json.code;
      var msg;
      if (code === 'TIMEOUT') {
        msg = '生成超时，请点击重试';
      } else if (code === 'NETWORK_ERROR') {
        msg = '网络或服务暂时不可用，可以稍后刷新页面再试。';
      } else if (code === 'DEEPSEEK_ERROR') {
        msg = '上游服务暂时不可用，请稍后再试。';
      } else if (code === 'JSON_DECODE_ERROR' || code === 'VALIDATION_ERROR') {
        msg = '生成行程结果异常，请稍后再试。';
      } else {
        msg = json.error || '请求失败，请稍后再试。';
      }
      console.error('API error', code, json.error);
      showError(msg, code);
      return;
    }
    showResult(json);
  } catch (err) {
    // 网络断开、CORS、或 res.json() 在 try 外抛错等
    showError('网络错误，请点击重试', 'NETWORK_ERROR');
  } finally {
    hideLoading();
  }
}

form.addEventListener('submit', function (e) {
  e.preventDefault();
  doSubmit(collectFormData());
});
