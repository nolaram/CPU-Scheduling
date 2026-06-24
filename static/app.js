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
  // Splash overlay: show on every index visit with fade-in + fade-out
  const splash = document.getElementById('splash');
  if (splash) {
    // ensure visible and start from hidden state for fade-in
    splash.classList.remove('hide');
    splash.style.opacity = '0';
    splash.style.visibility = 'visible';
    // trigger fade-in
    requestAnimationFrame(() => {
      splash.style.transition = 'opacity 0.6s ease, visibility 0.6s ease';
      splash.style.opacity = '1';
    });

    // after 2s visible, fade out and remove
    setTimeout(() => {
      splash.style.opacity = '0';
      splash.addEventListener('transitionend', () => splash.remove(), { once: true });
    }, 2000 + 600); // wait for fade-in to finish then show for ~2s
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
});
