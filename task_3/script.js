const form = document.querySelector('#uploadForm');
const fileInput = document.querySelector('#audioFile');
const fileLabel = document.querySelector('#fileLabel');
const fileHint = document.querySelector('#fileHint');
const dropZone = document.querySelector('#dropZone');
const results = document.querySelector('#results');
const metricsGrid = document.querySelector('#metricsGrid');
const metricTemplate = document.querySelector('#metricTemplate');
const submissions = [];


function displayMetrics(metrics) {

  metricsGrid.innerHTML = '';

  Object.entries(metrics).forEach(([label, value]) => {
    const item = metricTemplate.content.cloneNode(true);
    item.querySelector('.metric-label').textContent = label;
    item.querySelector('.metric-value').textContent = value;
    metricsGrid.append(item);
  });

}

async function loadSubmissions() {
  try {
    const response = await fetch(
      'http://127.0.0.1:8000/api/audio'
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || 'Failed to load submissions'
      );
    }

    submissions.length = 0;

    data.submissions.forEach(item => {

      submissions.push({
        id: item.submission_id,

        name: item.name || 'Unknown',
        phone: item.phone || 'N/A',

        fileName: item.file_name || 'Audio recording',

        url: item.audio_url,

        metrics: {
          'Duration':
            item.duration_seconds != null
              ? `${Number(item.duration_seconds).toFixed(2)} sec`
              : 'N/A',

          'Sample rate':
            item.sample_rate_khz != null
              ? `${item.sample_rate_khz} kHz`
              : 'N/A',

          'Bitrate':
            item.bitrate_kbps != null
              ? `${item.bitrate_kbps} kbps`
              : 'N/A',

          'Loudness':
            item.loudness_db != null
              ? `${item.loudness_db} LUFS`
              : 'N/A'
        }
      });

    });

    renderSubmissions();

  } catch (error) {

    console.error(
      'Failed to load submissions:',
      error
    );

    alert(error.message);
  }
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



form.addEventListener('submit', async event => {
  event.preventDefault();

  const file = fileInput.files[0];
  const name = document.querySelector('#name').value.trim();
  const phone = document.querySelector('#phone').value.trim();

  if (!name) {
    alert('Please enter your name.');
    return;
  }

  if (!phone) {
    alert('Please enter your phone number.');
    return;
  }

  if (!file) {
    alert('Please select an audio file.');
    return;
  }

  const formData = new FormData();

  formData.append('name', name);
  formData.append('phone', phone);
  formData.append('audio', file);

  try {

    const response = await fetch(
      'http://127.0.0.1:8000/api/audio/submissions',
      {
        method: 'POST',
        body: formData
      }
    );

    const data = await response.json();

     console.log("API response:", data);

    if (!response.ok) {
      throw new Error(data.detail || 'Upload failed');
    }

    console.log('Submission created:', data);

    const submission = {
      name: data.person.name,
      phone: data.person.phone,
      fileName: file.name,
      url: data.submission.audio_url,

      metrics: {
        'Duration': `${data.submission.duration_seconds.toFixed(2)} sec`,
        'Sample rate': `${data.submission.sample_rate_khz} kHz`,
        'Bitrate': `${data.submission.bitrate_kbps} kbps`,
        'Loudness': `${data.submission.loudness_db} LUFS`
      }
    };

    displayMetrics(submission.metrics);

    document.querySelector('#resultFile').textContent = file.name;

    results.classList.add('visible');

    form.reset();

    fileLabel.textContent = 'Choose an audio file';
    fileHint.textContent = 'MP3, WAV, M4A or other supported audio';

  } catch (error) {

    console.error('Upload error:', error);

    alert(error.message);
  }
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
    row.querySelector('.submission-file').textContent = item.fileName;

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

// document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => {

//   document.querySelectorAll('.tab,.view').forEach(el => el.classList.remove('active'));
//   tab.classList.add('active');
//   document.querySelector(`#${tab.dataset.view}View`).classList.add('active');
// }));



document.querySelectorAll('.tab').forEach(tab => {

  tab.addEventListener('click', async () => {

    document
      .querySelectorAll('.tab,.view')
      .forEach(el => el.classList.remove('active'));

    tab.classList.add('active');

    document
      .querySelector(`#${tab.dataset.view}View`)
      .classList.add('active');

    // Fetch latest submissions when
    // "All submissions" is clicked
    if (tab.dataset.view === 'submissions') {
      await loadSubmissions();
    }

  });

});
