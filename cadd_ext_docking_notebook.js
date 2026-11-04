/**
 * PharmaPulse 3D - CADD Suite: Docking Exporters & Lab Research Notebook
 * Upgraded with Iterative Gasteiger-Marsili (PEOE) Partial Charges & AutoDock Vina Atom Typing
 */

// 1. CADD Docking File Exporter (.PDBQT, .MOL2, .SDF)
window.CADD_Docking = (function() {
  'use strict';

  function init() {
    const btnPdbqt = document.getElementById('btn-export-pdbqt');
    const btnMol2 = document.getElementById('btn-export-mol2');
    const btnSdf = document.getElementById('btn-export-sdf');

    if (btnPdbqt) btnPdbqt.addEventListener('click', () => downloadPDBQT());
    if (btnMol2) btnMol2.addEventListener('click', () => downloadMOL2());
    if (btnSdf) btnSdf.addEventListener('click', () => downloadSDF());
  }

  function downloadPDBQT() {
    if (!window.currentCompoundData || !window.currentCompoundData.sdfData) {
      alert('Struktur konformer 3D belum tersedia.');
      return;
    }
    const data = window.currentCompoundData;
    const name = (data.props.Title || ('CID_' + data.cid)).replace(/[^a-zA-Z0-9_-]/g, '_');
    const pdbqtContent = convertSDFtoPDBQT(data.sdfData, name);
    triggerDownload(name + '_autodock_vina.pdbqt', pdbqtContent, 'text/plain');
  }

  function downloadMOL2() {
    if (!window.currentCompoundData || !window.currentCompoundData.sdfData) {
      alert('Struktur konformer 3D belum tersedia.');
      return;
    }
    const data = window.currentCompoundData;
    const name = (data.props.Title || ('CID_' + data.cid)).replace(/[^a-zA-Z0-9_-]/g, '_');
    const mol2Content = convertSDFtoMOL2(data.sdfData, name);
    triggerDownload(name + '_tripos.mol2', mol2Content, 'chemical/x-mol2');
  }

  function downloadSDF() {
    if (!window.currentCompoundData || !window.currentCompoundData.sdfData) {
      alert('Struktur konformer 3D belum tersedia.');
      return;
    }
    const data = window.currentCompoundData;
    const name = (data.props.Title || ('CID_' + data.cid)).replace(/[^a-zA-Z0-9_-]/g, '_');
    triggerDownload(name + '_3D_conformer.sdf', data.sdfData, 'chemical/x-mdl-sdfile');
  }

  function computeGasteigerAndTypes(sdf) {
    const lines = sdf.split(/\r?\n/);
    let numAtoms = 0, numBonds = 0;
    if (lines.length > 3) {
      numAtoms = parseInt(lines[3].substring(0, 3).trim(), 10) || 0;
      numBonds = parseInt(lines[3].substring(3, 6).trim(), 10) || 0;
    }

    const parsedAtoms = [];
    for (let i = 4; i < 4 + numAtoms && i < lines.length; i++) {
      const line = lines[i];
      if (line.length < 31) continue;
      const x = parseFloat(line.substring(0, 10).trim()) || 0;
      const y = parseFloat(line.substring(10, 20).trim()) || 0;
      const z = parseFloat(line.substring(20, 30).trim()) || 0;
      const element = line.substring(31, 34).trim() || 'C';
      parsedAtoms.push({ idx: parsedAtoms.length, x, y, z, element, charge: 0.0, neighbors: [], bondOrders: [] });
    }

    const parsedBonds = [];
    for (let i = 4 + numAtoms; i < 4 + numAtoms + numBonds && i < lines.length; i++) {
      const line = lines[i];
      if (!line || line.length < 6) continue;
      const a1 = (parseInt(line.substring(0, 3).trim(), 10) || 1) - 1;
      const a2 = (parseInt(line.substring(3, 6).trim(), 10) || 1) - 1;
      const bType = parseInt(line.substring(6, 9).trim(), 10) || 1;
      if (parsedAtoms[a1] && parsedAtoms[a2]) {
        parsedAtoms[a1].neighbors.push(a2);
        parsedAtoms[a1].bondOrders.push(bType);
        parsedAtoms[a2].neighbors.push(a1);
        parsedAtoms[a2].bondOrders.push(bType);
        parsedBonds.push({ a1, a2, bType });
      }
    }

    // Gasteiger-Marsili Orbital Electronegativity Parameters: chi = a + b*q + c*q^2
    // Reference: Gasteiger & Marsili, Tetrahedron 1980, 36, 3219-3228
    const gmParams = {
      'H':    { a: 7.17,  b: 6.24,  c: -0.56, dPlus: 20.02 },
      'C.3':  { a: 7.98,  b: 9.18,  c: 1.88,  dPlus: 19.04 },
      'C.2':  { a: 8.79,  b: 9.32,  c: 1.51,  dPlus: 19.62 },
      'C.1':  { a: 10.39, b: 9.45,  c: 0.73,  dPlus: 20.57 },
      'N.3':  { a: 11.54, b: 10.82, c: 1.36,  dPlus: 23.72 },
      'N.2':  { a: 12.87, b: 11.15, c: 0.85,  dPlus: 24.87 },
      'O.3':  { a: 14.18, b: 12.92, c: 1.39,  dPlus: 28.49 },
      'O.2':  { a: 17.07, b: 13.79, c: 0.47,  dPlus: 31.33 },
      'F':    { a: 14.66, b: 13.85, c: 2.31,  dPlus: 30.82 },
      'Cl':   { a: 11.00, b: 9.69,  c: 1.35,  dPlus: 22.04 },
      'Br':   { a: 10.08, b: 8.47,  c: 1.16,  dPlus: 19.71 },
      'S':    { a: 10.14, b: 9.13,  c: 1.38,  dPlus: 20.65 },
      'P':    { a: 8.90,  b: 8.24,  c: 0.96,  dPlus: 18.10 }
    };

    parsedAtoms.forEach(a => {
      const maxBond = a.bondOrders.length ? Math.max(...a.bondOrders) : 1;
      const isArom = a.bondOrders.includes(4) || (maxBond === 2 && a.neighbors.length === 3);
      let stateKey = a.element;
      if (a.element === 'C') {
        stateKey = maxBond === 3 ? 'C.1' : (maxBond === 2 || isArom ? 'C.2' : 'C.3');
      } else if (a.element === 'N') {
        stateKey = (maxBond === 2 || isArom) ? 'N.2' : 'N.3';
      } else if (a.element === 'O') {
        stateKey = maxBond === 2 ? 'O.2' : 'O.3';
      }
      a.gm = gmParams[stateKey] || gmParams['C.3'];
      a.isAromatic = isArom;
      a.maxBond = maxBond;

      // AutoDock 4 / Vina Atom Typing & Sybyl MOL2 Typing
      if (a.element === 'C') {
        a.adType = isArom ? 'A' : 'C';
        a.sybylType = isArom ? 'C.ar' : (maxBond === 2 ? 'C.2' : (maxBond === 3 ? 'C.1' : 'C.3'));
      } else if (a.element === 'O') {
        a.adType = 'OA';
        a.sybylType = maxBond === 2 ? 'O.2' : 'O.3';
      } else if (a.element === 'N') {
        const hasCarbonylNeighbor = a.neighbors.some(nIdx => {
          const nb = parsedAtoms[nIdx];
          return nb && nb.element === 'C' && nb.bondOrders.includes(2);
        });
        const hasH = a.neighbors.some(nIdx => parsedAtoms[nIdx] && parsedAtoms[nIdx].element === 'H');
        a.adType = (hasH || hasCarbonylNeighbor) ? 'N' : 'NA';
        a.sybylType = hasCarbonylNeighbor ? 'N.am' : (isArom ? 'N.ar' : (maxBond === 2 ? 'N.2' : 'N.3'));
      } else if (a.element === 'S') {
        a.adType = maxBond >= 2 ? 'SA' : 'S';
        a.sybylType = maxBond >= 2 ? 'S.o2' : 'S.3';
      } else if (a.element === 'H') {
        const attachedToPolar = a.neighbors.some(nIdx => {
          const nb = parsedAtoms[nIdx];
          return nb && (nb.element === 'O' || nb.element === 'N' || nb.element === 'S');
        });
        a.adType = attachedToPolar ? 'HD' : 'H';
        a.isPolarH = attachedToPolar;
        a.sybylType = 'H';
      } else {
        a.adType = a.element;
        a.sybylType = a.element;
      }
    });

    // 6-Iteration Damped PEOE (Partial Equalization of Orbital Electronegativity)
    for (let iter = 1; iter <= 6; iter++) {
      const damping = Math.pow(0.5, iter);
      const chi = parsedAtoms.map(a => a.gm.a + a.gm.b * a.charge + a.gm.c * a.charge * a.charge);
      const deltaQ = new Array(parsedAtoms.length).fill(0.0);

      parsedBonds.forEach(b => {
        const i = b.a1, j = b.a2;
        const chiI = chi[i], chiJ = chi[j];
        const denom = chiI > chiJ ? parsedAtoms[j].gm.dPlus : parsedAtoms[i].gm.dPlus;
        const dq = ((chiJ - chiI) / denom) * damping;
        deltaQ[i] += dq;
        deltaQ[j] -= dq;
      });

      for (let k = 0; k < parsedAtoms.length; k++) {
        parsedAtoms[k].charge += deltaQ[k];
      }
    }

    let rotatableBonds = 0;
    parsedBonds.forEach(b => {
      const a1 = parsedAtoms[b.a1], a2 = parsedAtoms[b.a2];
      if (b.bType === 1 && a1.element !== 'H' && a2.element !== 'H' && a1.neighbors.length > 1 && a2.neighbors.length > 1 && !(a1.isAromatic && a2.isAromatic)) {
        rotatableBonds++;
      }
    });

    return { parsedAtoms, parsedBonds, rotatableBonds };
  }

  function convertSDFtoPDBQT(sdf, title) {
    const { parsedAtoms, rotatableBonds } = computeGasteigerAndTypes(sdf);

    // Accumulate non-polar H charge into attached carbon for United-Atom PDBQT
    const pdbqtAtoms = [];
    parsedAtoms.forEach(a => {
      if (a.element === 'H' && !a.isPolarH) {
        const parentIdx = a.neighbors[0];
        if (parentIdx !== undefined && parsedAtoms[parentIdx]) {
          parsedAtoms[parentIdx].charge += a.charge;
        }
      }
    });

    parsedAtoms.forEach(a => {
      if (a.element === 'H' && !a.isPolarH) return; // merged non-polar H
      pdbqtAtoms.push(a);
    });

    let out = [];
    out.push('REMARK  GENERATED BY PHARMAPULSE 3D - CADD AUTODOCK VINA CONVERTER');
    out.push('REMARK  COMPLEX: ' + title);
    out.push('REMARK  GASTEIGER-MARSILI (PEOE 6-ITER) PARTIAL CHARGES & NON-POLAR H MERGED');
    out.push('ROOT');

    pdbqtAtoms.forEach((a, idx) => {
      const atomIdx = (idx + 1).toString().padStart(5, ' ');
      const atomName = (a.element + (idx + 1)).substring(0, 4).padEnd(4, ' ');
      const resName = 'LIG A   1';
      const xStr = a.x.toFixed(3).padStart(8, ' ');
      const yStr = a.y.toFixed(3).padStart(8, ' ');
      const zStr = a.z.toFixed(3).padStart(8, ' ');
      const occ = '  1.00';
      const bFactor = '  0.00';
      const qStr = a.charge.toFixed(3).padStart(8, ' ');
      const typeStr = a.adType.padEnd(2, ' ').padStart(3, ' ');

      out.push('HETATM' + atomIdx + ' ' + atomName + ' ' + resName + '    ' + xStr + yStr + zStr + occ + bFactor + '    ' + qStr + ' ' + typeStr);
    });

    out.push('ENDROOT');
    out.push('TORSDOF ' + Math.min(16, Math.max(0, rotatableBonds)));

    return out.join('\n');
  }

  function convertSDFtoMOL2(sdf, title) {
    const { parsedAtoms, parsedBonds } = computeGasteigerAndTypes(sdf);

    let out = [];
    out.push('@<TRIPOS>MOLECULE');
    out.push(title);
    out.push(parsedAtoms.length + ' ' + parsedBonds.length + ' 0 0 0');
    out.push('SMALL');
    out.push('GASTEIGER');
    out.push('');
    out.push('@<TRIPOS>ATOM');

    parsedAtoms.forEach((a, i) => {
      const idx = i + 1;
      const x = a.x.toFixed(4).padStart(10, ' ');
      const y = a.y.toFixed(4).padStart(10, ' ');
      const z = a.z.toFixed(4).padStart(4).padStart(10, ' ');
      const q = a.charge.toFixed(4).padStart(8, ' ');
      out.push(idx.toString().padStart(4, ' ') + ' ' + (a.element + idx).padEnd(5, ' ') + ' ' + x + ' ' + y + ' ' + z + ' ' + a.sybylType.padEnd(5, ' ') + ' 1 LIG ' + q);
    });

    out.push('@<TRIPOS>BOND');
    parsedBonds.forEach((b, i) => {
      const bIdx = i + 1;
      const bTypeStr = b.bType === 4 ? 'ar' : b.bType.toString();
      out.push(bIdx.toString().padStart(4, ' ') + ' ' + (b.a1 + 1).toString().padStart(4, ' ') + ' ' + (b.a2 + 1).toString().padStart(4, ' ') + ' ' + bTypeStr);
    });

    return out.join('\n');
  }

  function triggerDownload(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  return { init: init };
})();

// 2. Lab Research Notebook & Project Session Library
window.CADD_Notebook = (function() {
  'use strict';

  const storageKey = 'pharmapulse_lab_notebook_v1';
  let items = [];

  function init() {
    loadFromStorage();
    setupEvents();
    updateBadge();
  }

  function setupEvents() {
    const btnOpen = document.getElementById('btn-open-notebook');
    const modal = document.getElementById('notebook-modal');
    const btnClose = document.getElementById('btn-close-notebook');

    if (btnOpen && modal) {
      btnOpen.addEventListener('click', () => {
        renderList();
        modal.classList.remove('hidden');
      });
    }

    if (btnClose && modal) {
      btnClose.addEventListener('click', () => {
        modal.classList.add('hidden');
      });
    }

    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
      });
    }

    const btnSave = document.getElementById('btn-save-compound-notebook');
    if (btnSave) {
      btnSave.addEventListener('click', () => saveCurrentCompound());
    }

    const btnExport = document.getElementById('btn-notebook-export-json');
    if (btnExport) {
      btnExport.addEventListener('click', () => exportSessionJSON());
    }

    const inputImport = document.getElementById('notebook-import-input');
    if (inputImport) {
      inputImport.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) importSessionJSON(file);
      });
    }

    const btnClear = document.getElementById('btn-notebook-clear-all');
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        if (confirm('Apakah Anda yakin ingin menghapus seluruh catatan Lab Notebook?')) {
          items = [];
          saveToStorage();
          renderList();
          updateBadge();
        }
      });
    }
  }

  function saveCurrentCompound() {
    if (!window.currentCompoundData || !window.currentCompoundData.props) {
      alert('Belum ada senyawa yang dimuat untuk disimpan.');
      return;
    }
    const p = window.currentCompoundData.props;
    const cid = window.currentCompoundData.cid;

    const exists = items.find(item => item.cid === cid);
    if (exists) {
      alert('Senyawa "' + (p.Title || cid) + '" sudah ada di Lab Notebook.');
      return;
    }

    const item = {
      cid: cid,
      title: p.Title || ('CID ' + cid),
      formula: p.MolecularFormula || '-',
      mw: p.MolecularWeight || '-',
      logp: p.XLogP || p.LogP || '-',
      tpsa: p.TPSA || '-',
      smiles: p.CanonicalSMILES || p.IsomericSMILES || '-',
      date: new Date().toLocaleString('id-ID'),
      notes: 'Kandidat molekul aktif ditambahkan untuk optimasi struktur dan analisis in silico.'
    };

    items.unshift(item);
    saveToStorage();
    updateBadge();

    const btnSave = document.getElementById('btn-save-compound-notebook');
    if (btnSave) {
      const origText = btnSave.innerHTML;
      btnSave.innerHTML = '<i class="fa-solid fa-check"></i> Tersimpan di Notebook';
      btnSave.classList.add('btn-success');
      setTimeout(() => {
        btnSave.innerHTML = origText;
        btnSave.classList.remove('btn-success');
      }, 2000);
    }
  }

  function loadFromStorage() {
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) items = JSON.parse(raw);
    } catch (e) {
      items = [];
    }
  }

  function saveToStorage() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(items));
    } catch (e) {}
  }

  function updateBadge() {
    const badge = document.getElementById('notebook-badge-count');
    if (badge) badge.textContent = items.length;
  }

  function renderList() {
    const container = document.getElementById('notebook-list-container');
    const emptyState = document.getElementById('notebook-empty-state');
    if (!container) return;

    if (items.length === 0) {
      container.innerHTML = '';
      if (emptyState) emptyState.classList.remove('hidden');
      return;
    }

    if (emptyState) emptyState.classList.add('hidden');

    container.innerHTML = items.map((item, idx) => `
      <div class="notebook-item-card">
        <div class="nb-card-header">
          <div>
            <h4 class="nb-drug-title">${item.title}</h4>
            <span class="badge badge-outline">CID: ${item.cid}</span>
            <span class="nb-date"><i class="fa-regular fa-clock"></i> ${item.date}</span>
          </div>
          <div class="nb-actions">
            <button class="btn btn-sm btn-accent nb-load-btn" data-cid="${item.cid}" title="Muat ke layar utama">
              <i class="fa-solid fa-arrow-up-right-from-square"></i> Muat
            </button>
            <button class="btn btn-sm btn-outline text-danger nb-del-btn" data-idx="${idx}" title="Hapus dari notebook">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          </div>
        </div>
        <div class="nb-props-row">
          <span><strong>Rumus:</strong> ${item.formula}</span>
          <span><strong>MW:</strong> ${item.mw} g/mol</span>
          <span><strong>LogP:</strong> ${item.logp}</span>
          <span><strong>TPSA:</strong> ${item.tpsa} Å²</span>
        </div>
        <div class="nb-notes-wrapper">
          <label><i class="fa-solid fa-pencil"></i> Catatan Riset & Hipotesis:</label>
          <textarea class="nb-notes-textarea" data-idx="${idx}" placeholder="Ketik hipotesis modifikasi struktur, target reseptor, atau catatan laboratorium...">${item.notes || ''}</textarea>
        </div>
      </div>
    `).join('');

    container.querySelectorAll('.nb-del-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-idx'), 10);
        items.splice(idx, 1);
        saveToStorage();
        renderList();
        updateBadge();
      });
    });

    container.querySelectorAll('.nb-load-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const cid = btn.getAttribute('data-cid');
        const modal = document.getElementById('notebook-modal');
        if (modal) modal.classList.add('hidden');

        const searchInput = document.getElementById('compound-search-input');
        const btnSearch = document.getElementById('btn-search');
        if (searchInput && btnSearch) {
          searchInput.value = cid;
          btnSearch.click();
        }
      });
    });

    container.querySelectorAll('.nb-notes-textarea').forEach(ta => {
      ta.addEventListener('change', (e) => {
        const idx = parseInt(ta.getAttribute('data-idx'), 10);
        if (items[idx]) {
          items[idx].notes = e.target.value;
          saveToStorage();
        }
      });
    });
  }

  function exportSessionJSON() {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify({
      project: 'PharmaPulse 3D Research Session',
      exportedAt: new Date().toISOString(),
      compoundsCount: items.length,
      compounds: items
    }, null, 2));

    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute('href', dataStr);
    dlAnchor.setAttribute('download', 'PharmaPulse_Research_Session_' + Date.now() + '.json');
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
  }

  function importSessionJSON(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const parsed = JSON.parse(e.target.result);
        if (parsed && Array.isArray(parsed.compounds)) {
          parsed.compounds.forEach(c => {
            if (!items.some(it => it.cid === c.cid)) {
              items.push(c);
            }
          });
          saveToStorage();
          renderList();
          updateBadge();
          alert('Berhasil mengimpor ' + parsed.compounds.length + ' senyawa ke Lab Notebook.');
        } else {
          alert('Format file JSON tidak sesuai dengan sesi PharmaPulse 3D.');
        }
      } catch (err) {
        alert('Gagal membaca file JSON: ' + err.message);
      }
    };
    reader.readAsText(file);
  }

  return { init: init };
})();
