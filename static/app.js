let appData = null;
let activePeriods = ["Diagnóstica", "I Bimestre"];
let chartInstance = null;
let uploadStatus = {}; // tracks per-bimester upload state
let selectedYear = "2026";

document.addEventListener("DOMContentLoaded", () => {
  fetchData();
});

function changeAcademicYear() {
  const yrSelect = document.getElementById("academic-year-select");
  if (yrSelect) {
    selectedYear = yrSelect.value;
    const titleEl = document.getElementById("app-nav-title");
    if (titleEl) titleEl.innerText = `Agente Estadistico EPT ${selectedYear}`;
    fetchData();
  }
}

function sortActivePeriods() {
  const canonical = appData && appData.meta && appData.meta.periodos_totales 
    ? appData.meta.periodos_totales 
    : ["Diagnóstica", "Diagnostica", "I Bimestre", "II Bimestre", "III Bimestre", "IV Bimestre"];
  activePeriods.sort((a, b) => {
    let idxA = canonical.indexOf(a);
    let idxB = canonical.indexOf(b);
    if (idxA === -1) idxA = canonical.findIndex(p => p.toLowerCase() === a.toLowerCase());
    if (idxB === -1) idxB = canonical.findIndex(p => p.toLowerCase() === b.toLowerCase());
    if (idxA === -1) idxA = 99;
    if (idxB === -1) idxB = 99;
    return idxA - idxB;
  });
}

async function fetchData() {
  try {
    const res = await fetch(`/api/data?year=${selectedYear}`);
    const json = await res.json();
    if (json.success) {
      appData = json.data;
      const available = appData.meta.periodos_disponibles || [];
      activePeriods = [...available];
      sortActivePeriods();
      initPeriodSelector();
      renderAll();
    }
  } catch (err) {
    console.error("Error fetching data:", err);
  }
}

function initPeriodSelector() {
  const container = document.getElementById("period-selector");
  container.innerHTML = "";
  
  const allPeriods = appData.meta.periodos_totales || ["Diagnóstica", "I Bimestre", "II Bimestre", "III Bimestre", "IV Bimestre"];
  const available = appData.meta.periodos_disponibles || ["Diagnóstica", "I Bimestre"];

  sortActivePeriods();

  allPeriods.forEach(period => {
    const isAvailable = available.includes(period);
    const isActive = activePeriods.includes(period);

    const chip = document.createElement("div");
    chip.className = `period-chip ${isActive ? "active" : ""} ${!isAvailable ? "disabled" : ""}`;
    chip.innerHTML = `
      <i class="fa-solid ${isActive ? 'fa-square-check' : 'fa-square'}"></i>
      <span>${period}</span>
      ${!isAvailable ? '<small>(Pendiente)</small>' : ''}
    `;

    if (isAvailable) {
      chip.onclick = () => togglePeriod(period);
    }
    container.appendChild(chip);
  });
}

function togglePeriod(period) {
  if (activePeriods.includes(period)) {
    if (activePeriods.length > 1) {
      activePeriods = activePeriods.filter(p => p !== period);
    }
  } else {
    activePeriods.push(period);
  }
  sortActivePeriods();
  initPeriodSelector();
  renderAll();
}

function renderAll() {
  sortActivePeriods();
  renderKPIs();
  renderChart();
  renderGradesTable();
  renderSectionsTable();
}

function renderKPIs() {
  sortActivePeriods();
  const p1 = activePeriods[0];
  const p2 = activePeriods[activePeriods.length - 1];

  const promGen = appData.grados["Promedio General"] || {};
  const d2 = promGen[p2] || {};
  const d1 = promGen[p1] || {};

  document.getElementById("kpi-total").innerText = d2.evaluados || 0;

  const ada_val = d2.pct_AD_A || 0;
  const b_val = d2.pct_B || 0;
  const c_val = d2.pct_C || 0;

  document.getElementById("kpi-ada").innerText = `${ada_val.toFixed(1)}%`;
  document.getElementById("kpi-b").innerText = `${b_val.toFixed(1)}%`;
  document.getElementById("kpi-c").innerText = `${c_val.toFixed(1)}%`;

  if (p1 !== p2) {
    const var_ada = ada_val - (d1.pct_AD_A || 0);
    const var_b = b_val - (d1.pct_B || 0);
    const var_c = c_val - (d1.pct_C || 0);

    document.getElementById("kpi-ada-var").innerHTML = `<i class="fa-solid fa-arrow-trend-${var_ada >= 0 ? 'up':'down'}"></i> ${var_ada >= 0 ? '+':''}${var_ada.toFixed(1)}% vs ${p1}`;
    document.getElementById("kpi-b-var").innerHTML = `<i class="fa-solid fa-arrow-trend-${var_b >= 0 ? 'up':'down'}"></i> ${var_b >= 0 ? '+':''}${var_b.toFixed(1)}% vs ${p1}`;
    document.getElementById("kpi-c-var").innerHTML = `<i class="fa-solid fa-arrow-trend-${var_c <= 0 ? 'down':'up'}"></i> ${var_c >= 0 ? '+':''}${var_c.toFixed(1)}% vs ${p1}`;
  } else {
    document.getElementById("kpi-ada-var").innerHTML = `<i class="fa-solid fa-check"></i> ${p1}`;
    document.getElementById("kpi-b-var").innerHTML = `<i class="fa-solid fa-check"></i> ${p1}`;
    document.getElementById("kpi-c-var").innerHTML = `<i class="fa-solid fa-check"></i> ${p1}`;
  }
}

function renderChart() {
  const ctx = document.getElementById("comparisonChart").getContext("2d");
  const grades = ["1\u00b0 Grado", "2\u00b0 Grado", "3\u00b0 Grado", "4\u00b0 Grado", "5\u00b0 Grado", "Promedio General"];

  const gradeFilter = document.getElementById("grade-filter").value;
  const filteredGrades = gradeFilter === "ALL" ? grades : [gradeFilter];

  const colors = {
    "Diagnóstica": "rgba(148, 163, 184, 0.85)",
    "Diagnostica": "rgba(148, 163, 184, 0.85)",
    "I Bimestre": "rgba(59, 130, 246, 0.85)",
    "II Bimestre": "rgba(20, 184, 166, 0.85)",
    "III Bimestre": "rgba(245, 158, 11, 0.85)",
    "IV Bimestre": "rgba(16, 185, 129, 0.85)"
  };

  const datasets = [];
  sortActivePeriods();

  activePeriods.forEach(p => {
    const dataADA = filteredGrades.map(g => {
      const gData = appData.grados[g];
      return gData && gData[p] ? gData[p].pct_AD_A || 0 : 0;
    });
    datasets.push({
      label: `${p} (Logro AD/A)`,
      data: dataADA,
      backgroundColor: colors[p] || "rgba(99, 102, 241, 0.8)",
      borderRadius: 6
    });
  });

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: { labels: filteredGrades, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#94a3b8', font: { family: 'Inter', size: 12 } } },
        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%` } }
      },
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: '#94a3b8', callback: v => v + '%' }, grid: { color: 'rgba(255,255,255,0.08)' }, max: 100 }
      }
    }
  });
}

function renderGradesTable() {
  const h1 = document.getElementById("table-grades-header-1");
  const h2 = document.getElementById("table-grades-header-2");
  const body = document.getElementById("table-grades-body");

  sortActivePeriods();
  const periodsCount = activePeriods.length;
  const showVar = periodsCount > 1;
  const colSpanCategory = showVar ? periodsCount + 1 : periodsCount;

  h1.innerHTML = `
    <th rowspan="2">GRADO</th>
    <th colspan="${colSpanCategory}">LOGRO SATISFACTORIO (AD/A)</th>
    <th colspan="${colSpanCategory}">EN PROCESO (B)</th>
    <th colspan="${colSpanCategory}">EN INICIO (C)</th>
  `;

  let subHeaderHtml = "";

  // Logro Satisfactorio headers
  activePeriods.forEach(p => { subHeaderHtml += `<th>${p.toUpperCase()}</th>`; });
  if (showVar) subHeaderHtml += `<th>VAR. %</th>`;

  // En Proceso headers
  activePeriods.forEach(p => { subHeaderHtml += `<th>${p.toUpperCase()}</th>`; });
  if (showVar) subHeaderHtml += `<th>VAR. %</th>`;

  // En Inicio headers
  activePeriods.forEach(p => { subHeaderHtml += `<th>${p.toUpperCase()}</th>`; });
  if (showVar) subHeaderHtml += `<th>VAR. %</th>`;

  h2.innerHTML = subHeaderHtml;

  body.innerHTML = "";
  const grades = ["1\u00b0 Grado", "2\u00b0 Grado", "3\u00b0 Grado", "4\u00b0 Grado", "5\u00b0 Grado", "Promedio General"];
  const filter = document.getElementById("grade-filter").value;

  const initialPeriod = activePeriods[0];
  const latestPeriod = activePeriods[activePeriods.length - 1];

  grades.forEach(g => {
    if (filter !== "ALL" && filter !== g) return;
    const gData = appData.grados[g] || {};
    const isTotal = g === "Promedio General";
    const tr = document.createElement("tr");

    let rowHtml = `<td class="${isTotal ? 'total-row font-bold':''}">${g}</td>`;

    // 1. Logro Satisfactorio (AD/A)
    activePeriods.forEach(p => {
      const pStats = gData[p] || {};
      const val = (pStats.pct_AD_A || 0).toFixed(1);
      rowHtml += `<td>${val}%</td>`;
    });
    if (showVar) {
      const initVal = (gData[initialPeriod] || {}).pct_AD_A || 0;
      const latVal = (gData[latestPeriod] || {}).pct_AD_A || 0;
      const varADA = latVal - initVal;
      const varClass = varADA > 0 ? 'text-green font-bold' : (varADA < 0 ? 'text-red font-bold' : '');
      rowHtml += `<td class="${varClass}">${varADA >= 0 ? '+' : ''}${varADA.toFixed(1)}%</td>`;
    }

    // 2. En Proceso (B)
    activePeriods.forEach(p => {
      const pStats = gData[p] || {};
      const val = (pStats.pct_B || 0).toFixed(1);
      rowHtml += `<td>${val}%</td>`;
    });
    if (showVar) {
      const initVal = (gData[initialPeriod] || {}).pct_B || 0;
      const latVal = (gData[latestPeriod] || {}).pct_B || 0;
      const varB = latVal - initVal;
      const varClass = varB < 0 ? 'text-green font-bold' : (varB > 0 ? 'text-amber font-bold' : '');
      rowHtml += `<td class="${varClass}">${varB >= 0 ? '+' : ''}${varB.toFixed(1)}%</td>`;
    }

    // 3. En Inicio (C)
    activePeriods.forEach(p => {
      const pStats = gData[p] || {};
      const val = (pStats.pct_C || 0).toFixed(1);
      const isRed = (pStats.pct_C || 0) > 0;
      rowHtml += `<td class="${isRed ? 'text-red font-bold' : ''}">${val}%</td>`;
    });
    if (showVar) {
      const initVal = (gData[initialPeriod] || {}).pct_C || 0;
      const latVal = (gData[latestPeriod] || {}).pct_C || 0;
      const varC = latVal - initVal;
      // Decreasing C level is GREEN improvement! Increasing C level is RED alert!
      const varClass = varC < 0 ? 'text-green font-bold' : (varC > 0 ? 'text-red font-bold' : '');
      rowHtml += `<td class="${varClass}">${varC >= 0 ? '+' : ''}${varC.toFixed(1)}%</td>`;
    }

    tr.innerHTML = rowHtml;
    body.appendChild(tr);
  });
}

function renderSectionsTable() {
  const body = document.getElementById("table-sections-body");
  body.innerHTML = "";

  const lastPeriod = activePeriods[activePeriods.length - 1];
  let sections = {};

  if (appData.secciones_bimestres && appData.secciones_bimestres[lastPeriod]) {
    sections = appData.secciones_bimestres[lastPeriod];
  } else {
    sections = appData.secciones || {};
  }

  Object.entries(sections).forEach(([sec, d]) => {
    const tr = document.createElement("tr");
    
    let secData = d;
    if (typeof d === 'object' && !('evaluados' in d)) {
      secData = d[lastPeriod] || d[Object.keys(d).pop()] || {};
    }
    
    const evaluados = secData.evaluados || 0;
    const matriculados = secData.matriculados || evaluados;
    const adA = secData.AD_A || 0;
    const bCount = secData.B || 0;
    const cCount = secData.C || 0;
    const pctAdA = secData.pct_AD_A || 0;
    const pctB = secData.pct_B || 0;
    const pctC = secData.pct_C || 0;
    
    const isPriority = pctC > 5.0;

    tr.innerHTML = `
      <td class="font-bold">${sec}</td>
      <td>${matriculados}</td>
      <td>${evaluados}</td>
      <td>${adA} (${pctAdA.toFixed(1)}%)</td>
      <td>${bCount} (${pctB.toFixed(1)}%)</td>
      <td class="${cCount > 0 ? 'text-red font-bold' : ''}">${cCount} (${pctC.toFixed(1)}%)</td>
      <td>
        ${isPriority ? '<span class="badge badge-danger">Atencion Prioritaria</span>' : '<span class="badge badge-success">Estable</span>'}
      </td>
    `;
    body.appendChild(tr);
  });
}

function filterData() {
  renderChart();
  renderGradesTable();
}

function toggleChartView(view) {
  document.getElementById("btn-chart-js").classList.toggle("active", view === 'chartjs');
  document.getElementById("btn-chart-img").classList.toggle("active", view === 'img');
  document.getElementById("chart-js-wrapper").classList.toggle("hidden", view !== 'chartjs');
  document.getElementById("chart-img-wrapper").classList.toggle("hidden", view !== 'img');
}

// ============================================================
// PDF DOWNLOAD
// ============================================================
async function downloadPDF() {
  try {
    const res = await fetch(`/api/generate-pdf?year=${selectedYear}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ periods: activePeriods })
    });
    
    if (res.ok) {
      const blobData = await res.blob();
      const pdfBlob = new Blob([blobData], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = `Reporte_Comparativo_Estadisticas_EPT_${selectedYear}.pdf`;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => { window.URL.revokeObjectURL(url); a.remove(); }, 1000);
    } else {
      alert("Error al generar el reporte PDF.");
    }
  } catch (err) {
    alert("Error al comunicarse con el servidor PDF.");
  }
}

function previewPDF() {
  const pStr = encodeURIComponent(activePeriods.join(","));
  window.open(`/api/generate-pdf?periods=${pStr}&view=preview&year=${selectedYear}`, '_blank');
}

// ============================================================
// SECTION UPLOAD MODAL
// ============================================================
let sectionFiles = new Map(); // key: "1-A", value: File

function openSectionUploadModal() {
  document.getElementById("upload-modal").classList.remove("hidden");
  sectionFiles.clear();
  document.getElementById("upload-results-panel").classList.add("hidden");
  document.getElementById("upload-alerts-container").innerHTML = "";
  
  // Detect the next bimester to upload
  const available = appData.meta.periodos_disponibles || [];
  const allBims = ["I Bimestre", "II Bimestre", "III Bimestre", "IV Bimestre"];
  let defaultBim = "II Bimestre";
  for (const b of allBims) {
    if (!available.includes(b)) { defaultBim = b; break; }
  }
  document.getElementById("section_bimester_name").value = defaultBim;
  
  resetAllDropZones();
  updateFileCounter();
  initDropZones();
  loadUploadStatus();
}

function closeSectionUploadModal() {
  document.getElementById("upload-modal").classList.add("hidden");
}

function resetAllDropZones() {
  document.querySelectorAll('.drop-zone').forEach(zone => {
    const g = zone.getAttribute('data-grado');
    const s = zone.getAttribute('data-seccion');
    zone.className = 'drop-zone';
    zone.innerHTML = `
      <input type="file" class="hidden-file" accept=".xlsx,.xls">
      <i class="fa-solid fa-file-excel"></i>
      <span>${g}ro ${s}</span>
      <small class="drop-hint">Clic o arrastre archivo</small>
    `;
  });
  
  // Reset submit button
  const btnSubmit = document.getElementById('btn-submit-sections');
  btnSubmit.disabled = true;
  btnSubmit.className = 'btn btn-primary';
  btnSubmit.innerHTML = '<i class="fa-solid fa-gears"></i> Consolidar e Importar';
}

async function loadUploadStatus() {
  try {
    const res = await fetch(`/api/upload-status?year=${selectedYear}`);
    const json = await res.json();
    if (json.success) {
      uploadStatus = json.status;
      applyUploadStatusToUI();
    }
  } catch (err) {
    console.error("Error loading upload status:", err);
  }
}

function applyUploadStatusToUI() {
  const bimName = document.getElementById("section_bimester_name").value;
  const bimStatus = uploadStatus[bimName];
  
  // Update progress bar
  let uploadedCount = 0;
  
  if (bimStatus) {
    uploadedCount = bimStatus.count || 0;
    const uploaded = bimStatus.uploaded || [];
    
    // Mark previously uploaded sections
    uploaded.forEach(secName => {
      // Parse section name like "1\u00b0 A" -> grade=1, section=A
      const match = secName.match(/(\d+)/);
      const letterMatch = secName.match(/[A-Z]$/);
      if (match && letterMatch) {
        const gradeNum = match[1];
        const secLetter = letterMatch[0];
        const zone = document.getElementById(`drop-${gradeNum}-${secLetter}`);
        if (zone && !zone.classList.contains('loaded')) {
          zone.className = 'drop-zone previously-uploaded';
          zone.innerHTML = `
            <input type="file" class="hidden-file" accept=".xlsx,.xls">
            <i class="fa-solid fa-circle-check"></i>
            <span>${secName}</span>
            <small class="drop-hint">Ya cargado (reemplazar)</small>
          `;
        }
      }
    });
  }
  
  const totalSections = 10;
  const pct = Math.round((uploadedCount / totalSections) * 100);
  document.getElementById("upload-progress-fill").style.width = `${pct}%`;
  document.getElementById("upload-progress-label").innerText = `${uploadedCount} de ${totalSections} secciones cargadas`;
}

function initDropZones() {
  const dropZones = document.querySelectorAll('.drop-zone');
  
  dropZones.forEach(zone => {
    const gradeNum = zone.getAttribute('data-grado');
    const sectionLetter = zone.getAttribute('data-seccion');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => {
      zone.addEventListener(evt, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(evt => {
      zone.addEventListener(evt, () => zone.classList.add('dragover'), false);
    });
    
    ['dragleave', 'drop'].forEach(evt => {
      zone.addEventListener(evt, () => zone.classList.remove('dragover'), false);
    });
    
    zone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files.length) handleSectionFile(gradeNum, sectionLetter, files[0], zone);
    }, false);
    
    zone.addEventListener('click', (e) => {
      if (e.target.tagName !== 'BUTTON' && !e.target.closest('.btn-remove')) {
        const input = zone.querySelector('.hidden-file');
        if (input) input.click();
      }
    });
    
    const fileInput = zone.querySelector('.hidden-file');
    if (fileInput) {
      fileInput.addEventListener('change', function() {
        if (this.files.length) {
          handleSectionFile(gradeNum, sectionLetter, this.files[0], zone);
        }
      });
    }
  });
}

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function handleSectionFile(gradeNum, sectionLetter, file, zoneElement) {
  if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
    alert('Por favor, suba un archivo Excel (.xlsx o .xls)');
    return;
  }
  
  const key = `${gradeNum}-${sectionLetter}`;
  sectionFiles.set(key, file);
  
  zoneElement.className = 'drop-zone loaded';
  zoneElement.innerHTML = `
    <i class="fa-solid fa-circle-check" style="color: var(--emerald-accent);"></i>
    <span class="file-name" title="${file.name}">${file.name}</span>
    <button type="button" class="btn-remove" onclick="removeSectionFile('${gradeNum}', '${sectionLetter}', event)">
      <i class="fa-solid fa-xmark"></i>
    </button>
  `;
  
  updateFileCounter();
}

function removeSectionFile(gradeNum, sectionLetter, event) {
  event.stopPropagation();
  const key = `${gradeNum}-${sectionLetter}`;
  sectionFiles.delete(key);
  
  const zone = document.getElementById(`drop-${gradeNum}-${sectionLetter}`);
  zone.className = 'drop-zone';
  zone.innerHTML = `
    <input type="file" class="hidden-file" accept=".xlsx,.xls">
    <i class="fa-solid fa-file-excel"></i>
    <span>${gradeNum}ro ${sectionLetter}</span>
    <small class="drop-hint">Clic o arrastre archivo</small>
  `;
  
  // Re-attach event listeners
  const newInput = zone.querySelector('.hidden-file');
  newInput.addEventListener('change', function() {
    if (this.files.length) handleSectionFile(gradeNum, sectionLetter, this.files[0], zone);
  });
  
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => {
    zone.addEventListener(evt, preventDefaults, false);
  });
  ['dragenter', 'dragover'].forEach(evt => {
    zone.addEventListener(evt, () => zone.classList.add('dragover'), false);
  });
  ['dragleave', 'drop'].forEach(evt => {
    zone.addEventListener(evt, () => zone.classList.remove('dragover'), false);
  });
  zone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length) handleSectionFile(gradeNum, sectionLetter, files[0], zone);
  }, false);
  zone.addEventListener('click', (e) => {
    if (e.target.tagName !== 'BUTTON' && !e.target.closest('.btn-remove')) {
      const input = zone.querySelector('.hidden-file');
      if (input) input.click();
    }
  });
  
  updateFileCounter();
}

function updateFileCounter() {
  const count = sectionFiles.size;
  document.getElementById('upload-counter').innerText = count;
  document.getElementById('btn-submit-sections').disabled = count === 0;
}

async function handleSectionsUpload() {
  if (sectionFiles.size === 0) return;
  
  const bimesterName = document.getElementById('section_bimester_name').value;
  const formData = new FormData();
  formData.append('bimester_name', bimesterName);
  formData.append('year', selectedYear);
  
  // Set all zones to processing state and append files
  sectionFiles.forEach((file, key) => {
    const [grade, section] = key.split('-');
    formData.append(`file_${grade}_${section}`, file);
    
    const zone = document.getElementById(`drop-${grade}-${section}`);
    if (zone) {
      zone.className = 'drop-zone processing';
      zone.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i><span>Procesando...</span>';
    }
  });
  
  const btnSubmit = document.getElementById('btn-submit-sections');
  btnSubmit.disabled = true;
  btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Consolidando...';
  
  try {
    const res = await fetch('/api/upload-sections', {
      method: 'POST',
      body: formData
    });
    const json = await res.json();
    
    if (json.success) {
      // Update global app data
      appData = json.data;
      if (!activePeriods.includes(bimesterName)) {
        activePeriods.push(bimesterName);
      }
      initPeriodSelector();
      renderAll();
      
      // Update upload status
      if (json.upload_status) {
        uploadStatus = json.upload_status;
      }
      
      // Mark zones as completed
      sectionFiles.forEach((file, key) => {
        const [grade, section] = key.split('-');
        const zone = document.getElementById(`drop-${grade}-${section}`);
        if (zone) {
          zone.className = 'drop-zone loaded';
          zone.innerHTML = '<i class="fa-solid fa-circle-check" style="color: var(--emerald-accent);"></i><span>Completado</span>';
        }
      });
      
      // Update progress bar from consolidation details
      if (json.consolidation_details) {
        const totalAcc = json.consolidation_details.total_sections_accumulated || 0;
        const pct = Math.round((totalAcc / 10) * 100);
        document.getElementById("upload-progress-fill").style.width = `${pct}%`;
        document.getElementById("upload-progress-label").innerText = `${totalAcc} de 10 secciones cargadas`;
      }
      
      // Show results panel
      if (json.consolidation_details && json.consolidation_details.per_section_summaries) {
        showConsolidationResults(json.consolidation_details);
      }
      
      btnSubmit.innerHTML = '<i class="fa-solid fa-check"></i> Consolidacion Exitosa!';
      btnSubmit.classList.remove('btn-primary');
      btnSubmit.classList.add('btn-emerald');
    } else {
      alert('Error: ' + json.error);
      btnSubmit.disabled = false;
      btnSubmit.innerHTML = '<i class="fa-solid fa-gears"></i> Consolidar e Importar';
    }
  } catch (err) {
    console.error(err);
    alert('Error de conexion al cargar archivos.');
    btnSubmit.disabled = false;
    btnSubmit.innerHTML = '<i class="fa-solid fa-gears"></i> Consolidar e Importar';
  }
}

function showConsolidationResults(details) {
  const panel = document.getElementById('upload-results-panel');
  const tbody = document.getElementById('table-upload-results-body');
  const alertsContainer = document.getElementById('upload-alerts-container');
  
  panel.classList.remove('hidden');
  panel.classList.add('slide-in');
  tbody.innerHTML = '';
  alertsContainer.innerHTML = '';
  
  // Show alerts
  const alerts = details.alerts || [];
  if (alerts.length > 0) {
    alerts.forEach(a => {
      alertsContainer.innerHTML += `<div class="alert-box alert-warning"><i class="fa-solid fa-triangle-exclamation"></i> ${a}</div>`;
    });
  } else {
    alertsContainer.innerHTML = `<div class="alert-box alert-success"><i class="fa-solid fa-circle-check"></i> Todas las secciones procesadas sin alertas criticas.</div>`;
  }
  
  // Per-section results table
  const sections = details.per_section_summaries || [];
  
  sections.forEach(sec => {
    if (!sec) return;
    const tr = document.createElement('tr');
    let alertHtml = '<span class="badge badge-success">OK</span>';
    
    if (sec.pct_C > 20) {
      alertHtml = '<span class="badge badge-danger">Critico (>20% C)</span>';
    } else if (sec.pct_C > 10) {
      alertHtml = '<span class="badge badge-warning">Atencion (>10% C)</span>';
    } else if (sec.pct_C > 5) {
      alertHtml = '<span class="badge badge-warning">Monitorear (>5% C)</span>';
    }
    
    tr.innerHTML = `
      <td class="font-bold">${sec.seccion}</td>
      <td>${sec.evaluados}</td>
      <td>${sec.AD_A} (${sec.pct_AD_A.toFixed(1)}%)</td>
      <td>${sec.B} (${sec.pct_B.toFixed(1)}%)</td>
      <td class="${sec.C > 0 ? 'text-red font-bold' : ''}">${sec.C} (${sec.pct_C.toFixed(1)}%)</td>
      <td>${alertHtml}</td>
    `;
    tbody.appendChild(tr);
  });
  
  // Totals row
  if (details.total_evaluados) {
    const trTotal = document.createElement('tr');
    trTotal.style.background = 'rgba(59, 130, 246, 0.15)';
    trTotal.innerHTML = `
      <td class="font-bold">TOTAL</td>
      <td class="font-bold">${details.total_evaluados}</td>
      <td colspan="3" class="font-bold">${details.total_sections_now || 0} secciones procesadas (${details.total_sections_accumulated || 0}/10 acumuladas)</td>
      <td>${alerts.length > 0 ? '<span class="badge badge-warning">' + alerts.length + ' alertas</span>' : '<span class="badge badge-success">Sin alertas</span>'}</td>
    `;
    tbody.appendChild(trTotal);
  }
}
