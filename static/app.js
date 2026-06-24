function addProcessRow(containerId, type) {
  const container = document.getElementById(containerId);
  const row = document.createElement('div');
  row.className = 'process-item';
  row.innerHTML = `
    <input name="pid[]" placeholder="Process ID" required />
    <input name="arrival[]" type="number" placeholder="Arrival Time" min="0" required />
    <input name="burst[]" type="number" placeholder="Burst Time" min="1" required />
    <input name="priority[]" type="number" placeholder="Priority" min="0" value="0" />
    ${type === 'memory' ? '<input name="memory[]" type="number" placeholder="Memory" min="1" required />' : ''}
    <button type="button" class="button secondary remove-process">Remove</button>
  `;
  container.appendChild(row);
}

document.addEventListener('DOMContentLoaded', () => {
  const splash = document.getElementById('splash');
  const siteBackground = document.getElementById('site-background');
  const slideshowImages = ['/static/img/1.jpg', '/static/img/2.jpg', '/static/img/3.jpg'];
  const isHome = document.body.classList.contains('home-screen');
  let slideshowIndex = 0;

  function showNextBackground() {
    if (!siteBackground) return;
    siteBackground.classList.remove('visible');
    setTimeout(() => {
      siteBackground.style.backgroundImage = `url(${slideshowImages[slideshowIndex]})`;
      siteBackground.classList.add('visible');
      slideshowIndex = (slideshowIndex + 1) % slideshowImages.length;
    }, 600);
  }

  if (isHome && siteBackground) {
    siteBackground.style.backgroundImage = `url(${slideshowImages[0]})`;
    requestAnimationFrame(() => siteBackground.classList.add('visible'));
    setInterval(showNextBackground, 5000);
  } else if (splash) {
    splash.remove();
  }

  if (isHome && splash) {
    requestAnimationFrame(() => splash.classList.add('show'));
    setTimeout(() => {
      splash.classList.remove('show');
      const removeSplash = () => splash.remove();
      splash.addEventListener('transitionend', removeSplash, { once: true });
      setTimeout(removeSplash, 900);
    }, 2600);
  }
  const addCpuBtn = document.getElementById('add-cpu-process');
  const addMemoryBtn = document.getElementById('add-memory-process');
  const algorithmSelect = document.getElementById('algorithm');
  const memoryAlgorithmSelect = document.getElementById('algorithm');
  const quantumRow = document.getElementById('quantum-row');
  const memoryQuantumRow = document.getElementById('memory-quantum-row');

  if (addCpuBtn) {
    addCpuBtn.addEventListener('click', () => addProcessRow('cpu-process-list', 'cpu'));
    addProcessRow('cpu-process-list', 'cpu');
  }
  if (addMemoryBtn) {
    addMemoryBtn.addEventListener('click', () => addProcessRow('memory-process-list', 'memory'));
    addProcessRow('memory-process-list', 'memory');
  }

  if (algorithmSelect) {
    algorithmSelect.addEventListener('change', function () {
      quantumRow.style.display = this.value === '6' ? 'flex' : 'none';
    });
  }
  if (memoryAlgorithmSelect) {
    memoryAlgorithmSelect.addEventListener('change', function () {
      memoryQuantumRow.style.display = this.value === '6' ? 'flex' : 'none';
    });
  }

  document.body.addEventListener('click', (event) => {
    if (event.target.matches('.remove-process')) {
      event.target.closest('.process-item').remove();
    }
  });

  // Menu + modal logic
  const menuBtn = document.getElementById('menu-button');
  const siteMenu = document.getElementById('site-menu');
  const modalOverlay = document.getElementById('modal-overlay');
  const modalContent = document.getElementById('modal-content');
  const modalClose = document.getElementById('modal-close');

  if (menuBtn && siteMenu) {
    menuBtn.addEventListener('click', () => {
      const open = siteMenu.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      siteMenu.setAttribute('aria-hidden', open ? 'false' : 'true');
    });
    // close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!siteMenu.contains(e.target) && !menuBtn.contains(e.target)) {
        siteMenu.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
        siteMenu.setAttribute('aria-hidden', 'true');
      }
    });
  }

  function showModal(title, html) {
    modalContent.innerHTML = `<h2>${title}</h2>` + html;
    modalOverlay.classList.add('show');
    modalOverlay.setAttribute('aria-hidden', 'false');
  }

  function hideModal(){
    modalOverlay.classList.remove('show');
    modalOverlay.setAttribute('aria-hidden', 'true');
    const video = modalContent.querySelector('video');
    if (video) { video.pause(); video.currentTime = 0; }
  }

  const tutorialBtn = document.getElementById('menu-tutorial');
  const collabBtn = document.getElementById('menu-collaborators');
  const aboutBtn = document.getElementById('menu-about');

  if (tutorialBtn) {
    tutorialBtn.addEventListener('click', () => {
      siteMenu.classList.remove('open');
      showModal('Tutorial', `<div class="video-placeholder"><video id="tutorial-video" controls style="width:100%"><source id="tutorial-source" src="" type="video/mp4">Your browser does not support the video tag.</video></div>`);
    });
  }
  if (collabBtn) {
    collabBtn.addEventListener('click', () => {
      siteMenu.classList.remove('open');
      showModal('Collaborators', `<ul><li>Renser Ivahn Gutierrez</li><li>Rafael Almanza</li><li>Matthew Tonogbanua</li><li>Marlon Copino</li></ul>`);
    });
  }
  if (aboutBtn) {
    aboutBtn.addEventListener('click', () => {
      siteMenu.classList.remove('open');
      showModal('About', `<p>A program built by 4 Computer Engineering Students in Polytechnic University of the Philippines that shows the different concepts in Operating Systems</p>`);
    });
  }

  if (modalClose) modalClose.addEventListener('click', hideModal);
  if (modalOverlay) modalOverlay.addEventListener('click', (e)=>{ if (e.target === modalOverlay) hideModal(); });
});
