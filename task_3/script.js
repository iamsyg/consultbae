const form = document.querySelector('#uploadForm');
const fileInput = document.querySelector('#audioFile');
const fileLabel = document.querySelector('#fileLabel');
const fileHint = document.querySelector('#fileHint');
const dropZone = document.querySelector('#dropZone');
const results = document.querySelector('#results');
const metricsGrid = document.querySelector('#metricsGrid');
const metricTemplate = document.querySelector('#metricTemplate');
const submissions = [];

const makeMetrics = () => ({

  'Duration': `${Math.floor(Math.random() * 3) + 1}:${String(Math.floor(Math.random() * 59)).padStart(2, '0')}`,
  'Sample rate': [44.1, 48, 96][Math.floor(Math.random() * 3)] + ' kHz',
  'Bitrate': [128, 192, 256, 320][Math.floor(Math.random() * 4)] + ' kbps',
  'Loudness': '-' + (Math.random() * 7 + 10).toFixed(1) + ' dB'
});

function displayMetrics(metrics) {

  metricsGrid.innerHTML = '';

  Object.entries(metrics).forEach(([label, value]) => {
    const item = metricTemplate.content.cloneNode(true);
    item.querySelector('.metric-label').textContent = label;
    item.querySelector('.metric-value').textContent = value;
    metricsGrid.append(item);
  });
  
}

function chooseFile(file) {

  if (!file) return;
  fileLabel.textContent = file.name;
  fileHint.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB · ready to upload`;
}

fileInput.addEventListener('change', () => chooseFile(fileInput.files[0]));

['dragenter', 'dragover'].forEach(type => dropZone.addEventListener(type, event => { event.preventDefault(); dropZone.classList.add('dragging'); }));

['dragleave', 'drop'].forEach(type => dropZone.addEventListener(type, event => { event.preventDefault(); dropZone.classList.remove('dragging'); }));

dropZone.addEventListener('drop', event => {

  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('audio/')) { fileInput.files = event.dataTransfer.files; chooseFile(file); }
});

form.addEventListener('submit', event => {

  event.preventDefault();
  const file = fileInput.files[0];

  if (!file) return;
  
  const metrics = makeMetrics();
  const submission = { name: document.querySelector('#name').value, phone: document.querySelector('#phone').value, file, metrics, url: URL.createObjectURL(file) };

  submissions.unshift(submission);
  displayMetrics(metrics);
  document.querySelector('#resultFile').textContent = file.name;
  results.classList.add('visible');
  renderSubmissions();
});

function renderSubmissions() {

  const list = document.querySelector('#submissionList');
  const empty = document.querySelector('#emptyState');
  const badge = document.querySelector('#countBadge');
  const summary = document.querySelector('#submissionSummary');

  list.innerHTML = '';
  badge.textContent = submissions.length;
  summary.textContent = `${submissions.length} recording${submissions.length === 1 ? '' : 's'} received.`;
  empty.classList.toggle('hidden', submissions.length > 0);

  submissions.forEach(item => {

    const row = document.createElement('article');
    row.className = 'submission';

    row.innerHTML = `<div><h3 class="person-name"></h3><p class="phone"></p></div><div><p class="submission-file"></p><div class="submission-metrics"></div></div><button class="play-button" type="button" aria-label="Play audio">▶</button>`;

    row.querySelector('.person-name').textContent = item.name;
    row.querySelector('.phone').textContent = item.phone;
    row.querySelector('.submission-file').textContent = item.file.name;

    Object.entries(item.metrics).forEach(([key, value]) => { const tag = document.createElement('span'); tag.textContent = `${key}: ${value}`; row.querySelector('.submission-metrics').append(tag); });
    const audio = new Audio(item.url);
    const button = row.querySelector('.play-button');

    button.addEventListener('click', () => { if (audio.paused) audio.play(); else audio.pause(); });
    audio.addEventListener('play', () => { button.textContent = 'Ⅱ'; button.classList.add('playing'); });
    audio.addEventListener('pause', () => { button.textContent = '▶'; button.classList.remove('playing'); });
    audio.addEventListener('ended', () => { button.textContent = '▶'; button.classList.remove('playing'); });
    list.append(row);
  });
}

document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => {

  document.querySelectorAll('.tab,.view').forEach(el => el.classList.remove('active'));
  tab.classList.add('active');
  document.querySelector(`#${tab.dataset.view}View`).classList.add('active');
}));
