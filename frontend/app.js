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

function showLoading() {
  loading.classList.remove('hidden');
  errorEl.classList.add('hidden');
  resultEl.classList.add('hidden');
  submitBtn.disabled = true;
}

function hideLoading() {
  loading.classList.add('hidden');
  submitBtn.disabled = false;
}

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.classList.remove('hidden');
  resultEl.classList.add('hidden');
}

function showResult(plan) {
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
      const items = [];
      if (slot.transport) items.push('<strong>交通：</strong>' + escapeHtml(slot.transport));
      if (slot.sights) items.push('<strong>景点：</strong>' + escapeHtml(slot.sights));
      if (slot.activities) items.push('<strong>活动：</strong>' + escapeHtml(slot.activities));
      if (slot.accommodation) items.push('<strong>住宿：</strong>' + escapeHtml(slot.accommodation));
      if (items.length) html += '<div class="slot"><span class="slot-label ' + slotClass + '">' + label + '</span>' + items.join('；') + '</div>';
      else html += '<div class="slot"><span class="slot-label ' + slotClass + '">' + label + '</span>无安排</div>';
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

form.addEventListener('submit', async function (e) {
  e.preventDefault();
  const data = collectFormData();
  showLoading();

  try {
    const res = await fetch(API_BASE + '/api/generate-plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await res.json();

    if (!res.ok) {
      showError(json.error || '请求失败');
      return;
    }
    showResult(json);
  } catch (err) {
    showError('网络错误：' + (err.message || '请检查 API 是否已启动'));
  } finally {
    hideLoading();
  }
});
