/**
 * PharmaPulse 3D - Main Application Logic
 * PubChem PUG-REST Integration, 3D Molecular Renderer, and QSAR Lipinski Evaluator
 */

// Global State
let currentCompoundData = null;
let viewer3D = null;
let isSpinning = true;
let currentRenderStyle = 'ballAndStick';
let radarChartInstance = null;

// DOM Elements
const searchInput = document.getElementById('compound-search-input');
const btnSearch = document.getElementById('btn-search');
const loadingOverlay = document.getElementById('loading-overlay');
const loadingText = document.getElementById('loading-text');

// Preset Buttons
const presetBtns = document.querySelectorAll('.pill-btn');

// Tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

// View Containers
const singleViewContainer = document.getElementById('single-view-container');
const compareViewContainer = document.getElementById('compare-view-container');
const btnCompareMode = document.getElementById('btn-compare-mode');
const btnCloseCompare = document.getElementById('btn-close-compare');

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  initViewer3D();
  setupEventListeners();
  // Load default compound: Atorvastatin
  fetchCompoundData('Atorvastatin');
});

// Setup 3Dmol Viewer
function initViewer3D() {
  const container = document.getElementById('mol3d-viewport');
  if (!container) return;
  container.innerHTML = '';
  
  // Config 3Dmol Viewer
  const config = { backgroundColor: '#060911' };
  viewer3D = $3Dmol.createViewer(container, config);
}

// Event Listeners
function setupEventListeners() {
  // Search Button & Enter Key
  btnSearch.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (query) fetchCompoundData(query);
  });

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const query = searchInput.value.trim();
      if (query) fetchCompoundData(query);
    }
  });

  // Presets
  presetBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      presetBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const compoundName = btn.getAttribute('data-compound');
      searchInput.value = compoundName;
      fetchCompoundData(compoundName);
    });
  });

  // Tab Switching
  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      tabBtns.forEach((b) => b.classList.remove('active'));
      tabPanes.forEach((p) => p.classList.remove('active'));

      btn.classList.add('active');
      const activePane = document.getElementById(targetTab);
      if (activePane) activePane.classList.add('active');

      // Refresh 3D viewer size when tab becomes visible
      if (targetTab === 'tab-3d-overview' && viewer3D) {
        setTimeout(() => viewer3D.resize(), 100);
      }
    });
  });

  // 3D Controls
  document.getElementById('render-style-select')?.addEventListener('change', (e) => {
    currentRenderStyle = e.target.value;
    apply3DRenderStyle();
  });

  document.getElementById('btn-spin-toggle')?.addEventListener('click', () => {
    isSpinning = !isSpinning;
    if (viewer3D) {
      viewer3D.spin(isSpinning ? 'y' : false, 1);
    }
  });

  document.getElementById('btn-reset-view')?.addEventListener('click', () => {
    if (viewer3D) {
      viewer3D.zoomTo();
    }
  });

  // Compare Mode Toggle
  btnCompareMode.addEventListener('click', () => {
    singleViewContainer.classList.add('hidden');
    compareViewContainer.classList.remove('hidden');
    runMultiDrugComparison();
  });

  btnCloseCompare.addEventListener('click', () => {
    compareViewContainer.classList.add('hidden');
    singleViewContainer.classList.remove('hidden');
  });

  document.getElementById('btn-run-compare')?.addEventListener('click', () => {
    runMultiDrugComparison();
  });

  // Print/Export Report
  document.getElementById('btn-export-pdf')?.addEventListener('click', () => {
    window.print();
  });
}

// Fetch Compound Data from PubChem PUG-REST API
async function fetchCompoundData(query) {
  showLoading(`Menghubungi PubChem API untuk: "${query}"...`);
  try {
    // Step 1: Search CID
    let cid = query;
    const isNum = /^\d+$/.test(query);

    if (!isNum) {
      const searchUrl = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${encodeURIComponent(query)}/cids/JSON`;
      const res = await fetch(searchUrl);
      if (!res.ok) throw new Error('Senyawa tidak ditemukan di basis data PubChem.');
      const data = await res.json();
      if (!data.IdentifierList || !data.IdentifierList.CID || data.IdentifierList.CID.length === 0) {
        throw new Error('Senyawa tidak ditemukan.');
      }
      cid = data.IdentifierList.CID[0];
    }

    // Step 2: Fetch Compound Properties with robust fallback for XLogP / XLogP3
    let props = null;
    const baseFields = [
      'Title',
      'MolecularWeight',
      'MolecularFormula',
      'CanonicalSMILES',
      'IsomericSMILES',
      'InChI',
      'InChIKey',
      'IUPACName',
      'ExactMass',
      'MonoisotopicMass',
      'TPSA',
      'Complexity',
      'Charge',
      'HBondDonorCount',
      'HBondAcceptorCount',
      'RotatableBondCount',
      'HeavyAtomCount'
    ];

    // Attempt 1: with XLogP
    try {
      const fields1 = [...baseFields, 'XLogP'].join(',');
      const res1 = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/property/${fields1}/JSON`);
      if (res1.ok) {
        const data1 = await res1.json();
        props = data1.PropertyTable.Properties[0];
      }
    } catch (err) {
      console.warn('Query XLogP failed, trying XLogP3...');
    }

    // Attempt 2: with XLogP3 if Attempt 1 failed
    if (!props) {
      try {
        const fields2 = [...baseFields, 'XLogP3'].join(',');
        const res2 = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/property/${fields2}/JSON`);
        if (res2.ok) {
          const data2 = await res2.json();
          props = data2.PropertyTable.Properties[0];
        }
      } catch (err) {
        console.warn('Query XLogP3 failed, trying base properties...');
      }
    }

    // Attempt 3: Safe fallback without LogP in batch request
    if (!props) {
      const safeFields = baseFields.join(',');
      const res3 = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/property/${safeFields}/JSON`);
      if (!res3.ok) throw new Error('Gagal mengambil deskriptor sifat molekul.');
      const data3 = await res3.json();
      props = data3.PropertyTable.Properties[0];
    }

    currentCompoundData = {
      cid,
      props,
      sdfData,
      ghsData
    };

    // Render interface with fetched data
    renderSingleCompoundView(currentCompoundData);

  } catch (error) {
    alert(`Error: ${error.message}`);
  } finally {
    hideLoading();
  }
}

// Helper to safely extract LogP (PubChem stores either XLogP or XLogP3 depending on compound)
function extractLogP(props) {
  if (!props) return undefined;
  if (props.XLogP !== undefined) return props.XLogP;
  if (props.XLogP3 !== undefined) return props.XLogP3;
  return undefined;
}

// Render Single Compound View
function renderSingleCompoundView(data) {
  const p = data.props;
  const cid = data.cid;
  const logpVal = extractLogP(p);

  // Title Card
  document.getElementById('compound-name').textContent = p.Title || `PubChem CID: ${cid}`;
  document.getElementById('compound-cid-badge').textContent = `PubChem CID: ${cid}`;
  document.getElementById('compound-iupac').textContent = p.IUPACName || 'Nama IUPAC tidak tersedia';
  document.getElementById('formula-tag').innerHTML = `<i class="fa-solid fa-flask"></i> ${p.MolecularFormula || '-'}`;
  document.getElementById('mw-tag').innerHTML = `<i class="fa-solid fa-weight-hanging"></i> ${p.MolecularWeight ? p.MolecularWeight + ' g/mol' : '-'}`;
  document.getElementById('logp-tag').innerHTML = `<i class="fa-solid fa-droplet"></i> LogP: ${logpVal !== undefined ? logpVal : 'N/A'}`;
  document.getElementById('tpsa-tag').innerHTML = `<i class="fa-solid fa-layer-group"></i> TPSA: ${p.TPSA ? p.TPSA + ' Å²' : 'N/A'}`;

  // 2D Image & Identifiers
  const img2d = document.getElementById('img-2d-structure');
  img2d.src = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/PNG?image_size=400x400`;

  document.getElementById('val-cid').textContent = cid;
  document.getElementById('val-formula').textContent = p.MolecularFormula || '-';
  document.getElementById('val-inchikey').textContent = p.InChIKey || '-';
  document.getElementById('val-smiles').textContent = p.CanonicalSMILES || p.IsomericSMILES || '-';

  // Perform Druglikeness & Lipinski RO5 Evaluation
  const ro5 = evaluateLipinskiRO5(p);
  renderVerdictBanner(ro5);
  renderLipinskiChecklist(ro5, p);
  renderAdditionalFilters(p);
  renderRadarChart(p);

  // Render Detailed Descriptors Grid
  renderDescriptorsGrid(p);

  // Render GHS Safety
  renderGHSSafety(data.ghsData);

  // Load 3D Molecular Conformer into Viewer
  load3DConformer(data.sdfData);
}

// Evaluate Lipinski Rule of 5
function evaluateLipinskiRO5(props) {
  const mw = props.MolecularWeight || 0;
  const rawLogP = extractLogP(props);
  const logp = rawLogP !== undefined ? rawLogP : 0;
  const hbd = props.HBondDonorCount || 0;
  const hba = props.HBondAcceptorCount || 0;

  const mwPassed = mw <= 500;
  const logpPassed = logp <= 5;
  const hbdPassed = hbd <= 5;
  const hbaPassed = hba <= 10;

  let violations = 0;
  if (!mwPassed) violations++;
  if (!logpPassed) violations++;
  if (!hbdPassed) violations++;
  if (!hbaPassed) violations++;

  const score = 4 - violations;

  return {
    mwPassed,
    logpPassed,
    hbdPassed,
    hbaPassed,
    violations,
    score
  };
}

// Render Verdict Banner
function renderVerdictBanner(ro5) {
  const verdictCard = document.getElementById('verdict-card');
  const scoreNum = document.getElementById('verdict-score-num');
  const statusTitle = document.getElementById('verdict-status-title');
  const statusDesc = document.getElementById('verdict-status-desc');

  scoreNum.textContent = `${ro5.score}/4`;

  verdictCard.className = 'druglikeness-verdict-card';

  if (ro5.violations === 0) {
    statusTitle.textContent = 'Memenuhi Lipinski RO5';
    statusDesc.textContent = 'Sangat potensial sebagai kandidat sediaan obat oral (0 Pelanggaran).';
  } else if (ro5.violations === 1) {
    verdictCard.classList.add('warning');
    statusTitle.textContent = 'Peringatan Druglikeness';
    statusDesc.textContent = `Melanggar 1 aturan Lipinski RO5 (Sifat permeabilitas oral dapat berkurang).`;
  } else {
    verdictCard.classList.add('danger');
    statusTitle.textContent = 'Kurang Memenuhi (Non-Drug-like)';
    statusDesc.textContent = `Melanggar ${ro5.violations} aturan Lipinski RO5 (Kurang ideal untuk formulasi oral).`;
  }
}

// Render Lipinski Checklist Items & Progress Bars
function renderLipinskiChecklist(ro5, p) {
  // MW
  const ruleMW = document.getElementById('rule-mw');
  const valMW = document.getElementById('val-rule-mw');
  const barMW = document.getElementById('bar-rule-mw');
  valMW.textContent = `${p.MolecularWeight ? p.MolecularWeight + ' g/mol' : 'N/A'}`;
  const mwPct = Math.min(100, ((p.MolecularWeight || 0) / 500) * 100);
  barMW.style.width = `${mwPct}%`;
  setRuleItemStatus(ruleMW, ro5.mwPassed);

  // LogP
  const ruleLogP = document.getElementById('rule-logp');
  const valLogP = document.getElementById('val-rule-logp');
  const barLogP = document.getElementById('bar-rule-logp');
  const rawLogP = extractLogP(p);
  const logpVal = rawLogP !== undefined ? rawLogP : 0;
  valLogP.textContent = `${rawLogP !== undefined ? rawLogP : 'N/A'}`;
  const logpPct = Math.min(100, Math.max(0, (logpVal / 5) * 100));
  barLogP.style.width = `${logpPct}%`;
  setRuleItemStatus(ruleLogP, ro5.logpPassed);

  // HBD
  const ruleHBD = document.getElementById('rule-hbd');
  const valHBD = document.getElementById('val-rule-hbd');
  const barHBD = document.getElementById('bar-rule-hbd');
  const hbdVal = p.HBondDonorCount || 0;
  valHBD.textContent = `${hbdVal}`;
  const hbdPct = Math.min(100, (hbdVal / 5) * 100);
  barHBD.style.width = `${hbdPct}%`;
  setRuleItemStatus(ruleHBD, ro5.hbdPassed);

  // HBA
  const ruleHBA = document.getElementById('rule-hba');
  const valHBA = document.getElementById('val-rule-hba');
  const barHBA = document.getElementById('bar-rule-hba');
  const hbaVal = p.HBondAcceptorCount || 0;
  valHBA.textContent = `${hbaVal}`;
  const hbaPct = Math.min(100, (hbaVal / 10) * 100);
  barHBA.style.width = `${hbaPct}%`;
  setRuleItemStatus(ruleHBA, ro5.hbaPassed);
}

function setRuleItemStatus(element, passed) {
  if (!element) return;
  if (passed) {
    element.className = 'rule-item passed';
    element.querySelector('.rule-icon').innerHTML = '<i class="fa-solid fa-circle-check"></i>';
  } else {
    element.className = 'rule-item violated';
    element.querySelector('.rule-icon').innerHTML = '<i class="fa-solid fa-circle-xmark"></i>';
  }
}

// Render Additional Filters (Veber, Ghose, Pfizer 3/75)
function renderAdditionalFilters(p) {
  const rotb = p.RotatableBondCount || 0;
  const tpsa = p.TPSA || 0;
  const mw = p.MolecularWeight || 0;
  const rawLogP = extractLogP(p);
  const logp = rawLogP !== undefined ? rawLogP : 0;
  const heavyAtoms = p.HeavyAtomCount || 0;

  // Veber Rule (RotB <= 10 & TPSA <= 140)
  const veberPassed = rotb <= 10 && tpsa <= 140;
  document.getElementById('val-veber-rotb').textContent = rotb;
  document.getElementById('val-veber-tpsa').textContent = `${tpsa} Å²`;
  const veberBadge = document.getElementById('veber-status');
  veberBadge.textContent = veberPassed ? 'Lolos (Optimal Bioavailability)' : 'Peringatan (Bioavailability Terbatas)';
  veberBadge.className = `badge ${veberPassed ? 'badge-outline' : 'badge-warning'}`;

  // Ghose Filter (MW 160-480, LogP -0.4 to 5.6, Atoms 20 to 70)
  const ghosePassed = mw >= 160 && mw <= 480 && logp >= -0.4 && logp <= 5.6 && heavyAtoms >= 15 && heavyAtoms <= 70;
  const ghoseBadge = document.getElementById('ghose-status');
  ghoseBadge.textContent = ghosePassed ? 'Lolos Ghose Filter' : 'Tidak Memenuhi Saringan Ghose';
  ghoseBadge.className = `badge ${ghosePassed ? 'badge-outline' : 'badge-warning'}`;

  // Pfizer 3/75 Rule (LogP > 3 && TPSA < 75 -> Higher toxicity)
  const pfizerHighRisk = logp > 3 && tpsa < 75;
  const pfizerBadge = document.getElementById('pfizer-status');
  pfizerBadge.textContent = pfizerHighRisk ? 'Risiko Toksisitas Tinggi (Pfizer 3/75)' : 'Risiko Toksisitas Rendah';
  pfizerBadge.className = `badge ${pfizerHighRisk ? 'badge-danger' : 'badge-outline'}`;
}

// Render Radar Chart
function renderRadarChart(p) {
  const ctx = document.getElementById('druglikeness-radar-chart');
  if (!ctx) return;

  if (radarChartInstance) {
    radarChartInstance.destroy();
  }

  // Normalize parameters to 100% scale against Lipinski limits
  const mwNorm = Math.min(120, ((p.MolecularWeight || 0) / 500) * 100);
  const rawLogP = extractLogP(p);
  const logpVal = rawLogP !== undefined ? rawLogP : 0;
  const logpNorm = Math.min(120, Math.max(0, (logpVal / 5) * 100));
  const hbdNorm = Math.min(120, ((p.HBondDonorCount || 0) / 5) * 100);
  const hbaNorm = Math.min(120, ((p.HBondAcceptorCount || 0) / 10) * 100);
  const tpsaNorm = Math.min(120, ((p.TPSA || 0) / 140) * 100);
  const rotbNorm = Math.min(120, ((p.RotatableBondCount || 0) / 10) * 100);

  radarChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['MW (Max 500)', 'LogP (Max 5)', 'HBD (Max 5)', 'HBA (Max 10)', 'TPSA (Max 140)', 'RotB (Max 10)'],
      datasets: [
        {
          label: p.Title || 'Molekul Target',
          data: [mwNorm, logpNorm, hbdNorm, hbaNorm, tpsaNorm, rotbNorm],
          backgroundColor: 'rgba(6, 182, 212, 0.25)',
          borderColor: '#06b6d4',
          pointBackgroundColor: '#06b6d4',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#06b6d4'
        },
        {
          label: 'Batas Lipinski / Veber (100%)',
          data: [100, 100, 100, 100, 100, 100],
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
          borderColor: 'rgba(255, 255, 255, 0.3)',
          borderDash: [5, 5],
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
          grid: { color: 'rgba(255, 255, 255, 0.1)' },
          pointLabels: {
            color: '#94a3b8',
            font: { size: 10, family: 'Inter' }
          },
          ticks: {
            color: '#64748b',
            backdropColor: 'transparent',
            stepSize: 25
          },
          suggestedMin: 0,
          suggestedMax: 120
        }
      },
      plugins: {
        legend: {
          labels: { color: '#f8fafc', font: { family: 'Inter', size: 11 } }
        }
      }
    }
  });
}

// Render Descriptors Grid
function renderDescriptorsGrid(p) {
  const rawLogP = extractLogP(p);
  document.getElementById('d-mw').textContent = p.MolecularWeight ? p.MolecularWeight : '-';
  document.getElementById('d-logp').textContent = rawLogP !== undefined ? rawLogP : '-';
  document.getElementById('d-tpsa').textContent = p.TPSA !== undefined ? p.TPSA : '-';
  document.getElementById('d-hbd').textContent = p.HBondDonorCount !== undefined ? p.HBondDonorCount : '-';
  document.getElementById('d-hba').textContent = p.HBondAcceptorCount !== undefined ? p.HBondAcceptorCount : '-';
  document.getElementById('d-rotb').textContent = p.RotatableBondCount !== undefined ? p.RotatableBondCount : '-';
  document.getElementById('d-complexity').textContent = p.Complexity !== undefined ? p.Complexity : '-';
  document.getElementById('d-charge').textContent = p.Charge !== undefined ? p.Charge : '0';
  document.getElementById('d-heavyatoms').textContent = p.HeavyAtomCount !== undefined ? p.HeavyAtomCount : '-';
  document.getElementById('d-exactmass').textContent = p.ExactMass ? p.ExactMass : '-';
  document.getElementById('d-monoiso').textContent = p.MonoisotopicMass ? p.MonoisotopicMass : '-';
  document.getElementById('d-stereocenters').textContent = p.AtomStereoCount !== undefined ? p.AtomStereoCount : '0';
}

// Render GHS Safety
function renderGHSSafety(ghsData) {
  const signalWordElem = document.getElementById('ghs-signal');
  const descElem = document.getElementById('ghs-description');
  const listElem = document.getElementById('ghs-statements-list');

  listElem.innerHTML = '';

  if (!ghsData) {
    signalWordElem.textContent = 'INFORMASI GHS TERBATAS';
    descElem.textContent = 'Data piktogram GHS resmi PubChem tidak tersedia untuk senyawa ini. Selalu konsultasikan MSDS laboratorium.';
    return;
  }

  try {
    // Extract GHS hazard statements from PubChem JSON hierarchy
    signalWordElem.textContent = 'KLASIFIKASI BAHAYA KESELAMATAN (GHS)';
    descElem.textContent = 'Data bahaya kimia diambil dari PubChem Laboratory Chemical Safety Summary (LCSS):';

    const statements = [];
    const findHazards = (obj) => {
      if (!obj) return;
      if (obj.TOCHeading === 'GHS Hazard Statements' && obj.Information) {
        obj.Information.forEach((info) => {
          if (info.Value && info.Value.StringWithMarkup) {
            info.Value.StringWithMarkup.forEach((str) => {
              statements.push(str.String);
            });
          }
        });
      }
      if (obj.Section) {
        obj.Section.forEach(findHazards);
      }
    };

    if (ghsData.Record && ghsData.Record.Section) {
      ghsData.Record.Section.forEach(findHazards);
    }

    if (statements.length > 0) {
      const uniqueHazards = [...new Set(statements)].slice(0, 8);
      uniqueHazards.forEach((hazardText) => {
        const item = document.createElement('div');
        item.className = 'ghs-statement-item';
        item.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${hazardText}`;
        listElem.appendChild(item);
      });
    } else {
      listElem.innerHTML = '<div class="ghs-statement-item">Tidak ditemukan pernyataan bahaya khusus.</div>';
    }

  } catch (err) {
    console.warn('GHS parse error:', err);
    signalWordElem.textContent = 'GHS DATA UNAVAILABLE';
  }
}

// Load 3D Conformer into 3Dmol.js
function load3DConformer(sdfString) {
  if (!viewer3D) return;

  viewer3D.clear();

  if (sdfString && sdfString.trim().length > 0) {
    viewer3D.addModel(sdfString, 'sdf');
  } else if (currentCompoundData && currentCompoundData.props.CanonicalSMILES) {
    // Fallback: load SMILES if SDF 3D conformer not available
    viewer3D.addModel(currentCompoundData.props.CanonicalSMILES, 'smiles');
  }

  apply3DRenderStyle();
  viewer3D.zoomTo();
  if (isSpinning) {
    viewer3D.spin('y', 1);
  }
}

// Apply Selected 3D Style
function apply3DRenderStyle() {
  if (!viewer3D) return;

  switch (currentRenderStyle) {
    case 'stick':
      viewer3D.setStyle({}, { stick: { radius: 0.15 } });
      break;
    case 'sphere':
      viewer3D.setStyle({}, { sphere: { scale: 0.9 } });
      break;
    case 'wireframe':
      viewer3D.setStyle({}, { line: {} });
      break;
    case 'ballAndStick':
    default:
      viewer3D.setStyle({}, { stick: { radius: 0.14 }, sphere: { scale: 0.28 } });
      break;
  }
  viewer3D.render();
}

// Multi-Drug Comparison Engine
async function runMultiDrugComparison() {
  const name1 = document.getElementById('cmp-input-1').value.trim() || 'Paracetamol';
  const name2 = document.getElementById('cmp-input-2').value.trim() || 'Ibuprofen';
  const name3 = document.getElementById('cmp-input-3').value.trim();

  const queries = [name1, name2];
  if (name3) queries.push(name3);

  showLoading('Mengambil data komparasi senyawa...');

  try {
    const results = await Promise.all(queries.map((q) => fetchDrugPropsSimple(q)));

    renderComparisonTable(results);
  } catch (err) {
    alert(`Gagal memuat data komparasi: ${err.message}`);
  } finally {
    hideLoading();
  }
}

async function fetchDrugPropsSimple(name) {
  // Search CID
  const searchUrl = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${encodeURIComponent(name)}/cids/JSON`;
  const res = await fetch(searchUrl);
  if (!res.ok) throw new Error(`Senyawa "${name}" tidak ditemukan.`);
  const data = await res.json();
  const cid = data.IdentifierList.CID[0];

  // Fetch Props with fallback
  let props = null;
  try {
    const res1 = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/property/Title,MolecularWeight,MolecularFormula,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount/JSON`);
    if (res1.ok) {
      const data1 = await res1.json();
      props = data1.PropertyTable.Properties[0];
    }
  } catch(e) {}

  if (!props) {
    try {
      const res2 = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/property/Title,MolecularWeight,MolecularFormula,XLogP3,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount/JSON`);
      if (res2.ok) {
        const data2 = await res2.json();
        props = data2.PropertyTable.Properties[0];
      }
    } catch(e) {}
  }

  if (!props) {
    const res3 = await fetch(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/property/Title,MolecularWeight,MolecularFormula,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount/JSON`);
    const data3 = await res3.json();
    props = data3.PropertyTable.Properties[0];
  }

  return { cid, name, props };
}

function renderComparisonTable(drugs) {
  const headerRow = document.getElementById('cmp-header-row');
  const bodyRows = document.getElementById('cmp-body-rows');

  headerRow.innerHTML = '<th>Parameter / Deskriptor</th>';
  drugs.forEach((d) => {
    headerRow.innerHTML += `
      <th>
        <div style="font-size:16px; font-weight:800; color:var(--text-main);">${d.props.Title || d.name}</div>
        <div style="font-size:11px; color:var(--color-primary);">CID: ${d.cid}</div>
        <img src="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${d.cid}/PNG?image_size=150x150" style="width:100px; height:100px; background:#fff; border-radius:8px; margin-top:8px; object-fit:contain;" />
      </th>
    `;
  });

  const rowSpecs = [
    { label: 'Formula Molekul', key: (p) => p.MolecularFormula || '-' },
    { label: 'Bobot Molekul (MW) [<=500]', key: (p) => `${p.MolecularWeight} g/mol` },
    { label: 'Partition Coeff (LogP) [<=5]', key: (p) => { const lp = extractLogP(p); return lp !== undefined ? lp : 'N/A'; } },
    { label: 'H-Bond Donors (HBD) [<=5]', key: (p) => p.HBondDonorCount !== undefined ? p.HBondDonorCount : '-' },
    { label: 'H-Bond Acceptors (HBA) [<=10]', key: (p) => p.HBondAcceptorCount !== undefined ? p.HBondAcceptorCount : '-' },
    { label: 'TPSA [<=140 Å²]', key: (p) => `${p.TPSA || 0} Å²` },
    { label: 'Rotatable Bonds [<=10]', key: (p) => p.RotatableBondCount !== undefined ? p.RotatableBondCount : '-' },
    {
      label: 'Skor Lipinski RO5 (Kelayakan)',
      key: (p) => {
        const ro5 = evaluateLipinskiRO5(p);
        const color = ro5.violations === 0 ? 'var(--color-success)' : (ro5.violations === 1 ? 'var(--color-warning)' : 'var(--color-danger)');
        return `<strong style="color:${color}; font-size:15px;">${ro5.score}/4 (${ro5.violations} Violations)</strong>`;
      }
    }
  ];

  bodyRows.innerHTML = '';
  rowSpecs.forEach((spec) => {
    let trHtml = `<tr><td style="font-weight:600; color:var(--text-muted);">${spec.label}</td>`;
    drugs.forEach((d) => {
      trHtml += `<td>${spec.key(d.props)}</td>`;
    });
    trHtml += '</tr>';
    bodyRows.innerHTML += trHtml;
  });
}

// Helpers
function showLoading(msg = 'Memproses data...') {
  loadingText.textContent = msg;
  loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
  loadingOverlay.classList.add('hidden');
}
