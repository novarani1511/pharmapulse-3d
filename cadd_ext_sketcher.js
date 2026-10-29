/**
 * PharmaPulse 3D - CADD Suite: 2D Molecular Canvas Sketcher & De Novo Lead Designer
 * Draw, modify scaffolds, calculate real-time RO5 properties, and push to main 3D analyzer.
 */
window.CADD_Sketcher = (function() {
  'use strict';

  let canvas = null;
  let ctx = null;
  let atoms = [];
  let bonds = [];
  let selectedTool = 'atom';
  let selectedElement = 'C';
  let selectedBondOrder = 1;
  let dragStartAtom = null;
  let mousePos = { x: 0, y: 0 };
  let nextAtomId = 1;
  let currentCalculated = null;

  const elementColors = {
    'C': '#94a3b8',
    'N': '#38bdf8',
    'O': '#f87171',
    'S': '#fbbf24',
    'P': '#fb923c',
    'F': '#4ade80',
    'Cl': '#34d399',
    'Br': '#a78bfa'
  };

  const atomicWeights = {
    'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'S': 32.06, 'P': 30.974,
    'F': 18.998, 'Cl': 35.45, 'Br': 79.904
  };

  function init() {
    canvas = document.getElementById('sketcher-canvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    setupEvents();
    loadScaffold('aspirin');
  }

  function setupEvents() {
    const toolBtns = document.querySelectorAll('.sketch-tool-btn');
    toolBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        toolBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tool = btn.getAttribute('data-tool');
        const val = btn.getAttribute('data-value');

        selectedTool = tool;
        if (tool === 'atom') selectedElement = val;
        if (tool === 'bond') selectedBondOrder = parseInt(val, 10);
        if (tool === 'ring') insertRing(val, 320, 210);
      });
    });

    const presetBtns = document.querySelectorAll('.sketch-preset-btn');
    presetBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const sc = btn.getAttribute('data-scaffold');
        loadScaffold(sc);
      });
    });

    const btnClear = document.getElementById('btn-sketcher-clear');
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        atoms = [];
        bonds = [];
        nextAtomId = 1;
        render();
        calculateProperties();
      });
    }

    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    const btnPush = document.getElementById('btn-sketcher-push');
    const btnPushLarge = document.getElementById('btn-sketcher-push-large');
    const handlerPush = () => pushToMainAnalyzer();
    if (btnPush) btnPush.addEventListener('click', handlerPush);
    if (btnPushLarge) btnPushLarge.addEventListener('click', handlerPush);
  }

  function getCanvasPos(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    };
  }

  function findAtomNear(pos, radius) {
    const r = radius || 18;
    return atoms.find(a => {
      const dx = a.x - pos.x;
      const dy = a.y - pos.y;
      return Math.sqrt(dx * dx + dy * dy) <= r;
    });
  }

  function findBondNear(pos, distThreshold) {
    const thresh = distThreshold || 10;
    for (let b of bonds) {
      const a1 = atoms.find(a => a.id === b.atom1Id);
      const a2 = atoms.find(a => a.id === b.atom2Id);
      if (!a1 || !a2) continue;

      const d = distToSegment(pos, a1, a2);
      if (d <= thresh) return b;
    }
    return null;
  }

  function distToSegment(p, v, w) {
    const l2 = (v.x - w.x) * (v.x - w.x) + (v.y - w.y) * (v.y - w.y);
    if (l2 === 0) return Math.hypot(p.x - v.x, p.y - v.y);
    let t = ((p.x - v.x) * (w.x - v.x) + (p.y - v.y) * (w.y - v.y)) / l2;
    t = Math.max(0, Math.min(1, t));
    return Math.hypot(p.x - (v.x + t * (w.x - v.x)), p.y - (v.y + t * (w.y - v.y)));
  }

  function handleMouseDown(e) {
    const pos = getCanvasPos(e);
    const clickedAtom = findAtomNear(pos);
    const clickedBond = findBondNear(pos);

    if (selectedTool === 'erase') {
      if (clickedAtom) {
        removeAtom(clickedAtom.id);
      } else if (clickedBond) {
        removeBond(clickedBond);
      }
      render();
      calculateProperties();
      return;
    }

    if (selectedTool === 'bond') {
      if (clickedAtom) {
        dragStartAtom = clickedAtom;
      } else if (clickedBond) {
        clickedBond.order = (clickedBond.order % 3) + 1;
        render();
        calculateProperties();
      }
      return;
    }

    if (selectedTool === 'atom') {
      if (clickedAtom) {
        clickedAtom.element = selectedElement;
      } else {
        const newAtom = {
          id: nextAtomId++,
          element: selectedElement,
          x: Math.round(pos.x),
          y: Math.round(pos.y)
        };
        atoms.push(newAtom);
      }
      render();
      calculateProperties();
    }
  }

  function handleMouseMove(e) {
    mousePos = getCanvasPos(e);
    if (dragStartAtom) {
      render();
      ctx.beginPath();
      ctx.moveTo(dragStartAtom.x, dragStartAtom.y);
      ctx.lineTo(mousePos.x, mousePos.y);
      ctx.strokeStyle = '#06b6d4';
      ctx.lineWidth = 2.5;
      ctx.setLineDash([4, 4]);
      ctx.stroke();
      ctx.setLineDash([]);
    }
  }

  function handleMouseUp(e) {
    if (dragStartAtom) {
      const pos = getCanvasPos(e);
      const targetAtom = findAtomNear(pos);

      if (targetAtom && targetAtom.id !== dragStartAtom.id) {
        const existingBond = bonds.find(b => 
          (b.atom1Id === dragStartAtom.id && b.atom2Id === targetAtom.id) ||
          (b.atom2Id === dragStartAtom.id && b.atom1Id === targetAtom.id)
        );
        if (existingBond) {
          existingBond.order = (existingBond.order % 3) + 1;
        } else {
          bonds.push({
            atom1Id: dragStartAtom.id,
            atom2Id: targetAtom.id,
            order: selectedBondOrder || 1
          });
        }
      } else if (!targetAtom) {
        const newAtom = {
          id: nextAtomId++,
          element: 'C',
          x: Math.round(pos.x),
          y: Math.round(pos.y)
        };
        atoms.push(newAtom);
        bonds.push({
          atom1Id: dragStartAtom.id,
          atom2Id: newAtom.id,
          order: selectedBondOrder || 1
        });
      }
      dragStartAtom = null;
      render();
      calculateProperties();
    }
  }

  function removeAtom(id) {
    atoms = atoms.filter(a => a.id !== id);
    bonds = bonds.filter(b => b.atom1Id !== id && b.atom2Id !== id);
  }

  function removeBond(bond) {
    bonds = bonds.filter(b => b !== bond);
  }

  function insertRing(type, cx, cy) {
    const radius = 45;
    if (type === 'benzene') {
      const ringAtoms = [];
      for (let i = 0; i < 6; i++) {
        const angle = (i * 60) * Math.PI / 180;
        const a = {
          id: nextAtomId++,
          element: 'C',
          x: Math.round(cx + radius * Math.cos(angle)),
          y: Math.round(cy + radius * Math.sin(angle))
        };
        atoms.push(a);
        ringAtoms.push(a);
      }
      for (let i = 0; i < 6; i++) {
        const next = (i + 1) % 6;
        bonds.push({
          atom1Id: ringAtoms[i].id,
          atom2Id: ringAtoms[next].id,
          order: (i % 2 === 0) ? 2 : 1
        });
      }
    } else if (type === 'cyclopentane') {
      const ringAtoms = [];
      for (let i = 0; i < 5; i++) {
        const angle = (i * 72 - 90) * Math.PI / 180;
        const a = {
          id: nextAtomId++,
          element: 'C',
          x: Math.round(cx + radius * Math.cos(angle)),
          y: Math.round(cy + radius * Math.sin(angle))
        };
        atoms.push(a);
        ringAtoms.push(a);
      }
      for (let i = 0; i < 5; i++) {
        const next = (i + 1) % 5;
        bonds.push({
          atom1Id: ringAtoms[i].id,
          atom2Id: ringAtoms[next].id,
          order: 1
        });
      }
    } else if (type === 'pyridine') {
      const ringAtoms = [];
      for (let i = 0; i < 6; i++) {
        const angle = (i * 60 - 90) * Math.PI / 180;
        const a = {
          id: nextAtomId++,
          element: (i === 0) ? 'N' : 'C',
          x: Math.round(cx + radius * Math.cos(angle)),
          y: Math.round(cy + radius * Math.sin(angle))
        };
        atoms.push(a);
        ringAtoms.push(a);
      }
      for (let i = 0; i < 6; i++) {
        const next = (i + 1) % 6;
        bonds.push({
          atom1Id: ringAtoms[i].id,
          atom2Id: ringAtoms[next].id,
          order: (i % 2 === 0) ? 2 : 1
        });
      }
    }

    render();
    calculateProperties();
  }

  function loadScaffold(name) {
    atoms = [];
    bonds = [];
    nextAtomId = 1;
    const cx = 320, cy = 200;

    if (name === 'aspirin') {
      insertRing('benzene', cx - 40, cy);
      const aC1 = atoms[0];
      const aCarboxylC = { id: nextAtomId++, element: 'C', x: aC1.x + 50, y: aC1.y - 25 };
      const aCarboxylO = { id: nextAtomId++, element: 'O', x: aCarboxylC.x + 35, y: aCarboxylC.y - 30 };
      const aCarboxylOH = { id: nextAtomId++, element: 'O', x: aCarboxylC.x + 40, y: aCarboxylC.y + 20 };
      atoms.push(aCarboxylC, aCarboxylO, aCarboxylOH);
      bonds.push(
        { atom1Id: aC1.id, atom2Id: aCarboxylC.id, order: 1 },
        { atom1Id: aCarboxylC.id, atom2Id: aCarboxylO.id, order: 2 },
        { atom1Id: aCarboxylC.id, atom2Id: aCarboxylOH.id, order: 1 }
      );
      const aC2 = atoms[1];
      const aEsterO = { id: nextAtomId++, element: 'O', x: aC2.x + 40, y: aC2.y + 40 };
      const aAcetylC = { id: nextAtomId++, element: 'C', x: aEsterO.x + 45, y: aEsterO.y + 10 };
      const aAcetylO = { id: nextAtomId++, element: 'O', x: aAcetylC.x, y: aAcetylC.y + 40 };
      const aMethylC = { id: nextAtomId++, element: 'C', x: aAcetylC.x + 45, y: aAcetylC.y - 15 };
      atoms.push(aEsterO, aAcetylC, aAcetylO, aMethylC);
      bonds.push(
        { atom1Id: aC2.id, atom2Id: aEsterO.id, order: 1 },
        { atom1Id: aEsterO.id, atom2Id: aAcetylC.id, order: 1 },
        { atom1Id: aAcetylC.id, atom2Id: aAcetylO.id, order: 2 },
        { atom1Id: aAcetylC.id, atom2Id: aMethylC.id, order: 1 }
      );
    } else if (name === 'paracetamol') {
      insertRing('benzene', cx, cy);
      const a1 = atoms[0];
      const a4 = atoms[3];
      const aOH = { id: nextAtomId++, element: 'O', x: a4.x, y: a4.y + 50 };
      const aN = { id: nextAtomId++, element: 'N', x: a1.x, y: a1.y - 45 };
      const aC = { id: nextAtomId++, element: 'C', x: aN.x + 45, y: aN.y - 20 };
      const aO = { id: nextAtomId++, element: 'O', x: aC.x, y: aC.y - 45 };
      const aMe = { id: nextAtomId++, element: 'C', x: aC.x + 45, y: aC.y };
      atoms.push(aOH, aN, aC, aO, aMe);
      bonds.push(
        { atom1Id: a4.id, atom2Id: aOH.id, order: 1 },
        { atom1Id: a1.id, atom2Id: aN.id, order: 1 },
        { atom1Id: aN.id, atom2Id: aC.id, order: 1 },
        { atom1Id: aC.id, atom2Id: aO.id, order: 2 },
        { atom1Id: aC.id, atom2Id: aMe.id, order: 1 }
      );
    } else if (name === 'benzoic') {
      insertRing('benzene', cx - 30, cy);
      const a1 = atoms[0];
      const aC = { id: nextAtomId++, element: 'C', x: a1.x + 50, y: a1.y };
      const aO1 = { id: nextAtomId++, element: 'O', x: aC.x + 35, y: aC.y - 30 };
      const aO2 = { id: nextAtomId++, element: 'O', x: aC.x + 35, y: aC.y + 30 };
      atoms.push(aC, aO1, aO2);
      bonds.push(
        { atom1Id: a1.id, atom2Id: aC.id, order: 1 },
        { atom1Id: aC.id, atom2Id: aO1.id, order: 2 },
        { atom1Id: aC.id, atom2Id: aO2.id, order: 1 }
      );
    } else if (name === 'ibuprofen') {
      insertRing('benzene', cx - 20, cy);
      const a1 = atoms[0];
      const a4 = atoms[3];
      const aIsoC1 = { id: nextAtomId++, element: 'C', x: a4.x - 45, y: a4.y };
      const aIsoCH = { id: nextAtomId++, element: 'C', x: aIsoC1.x - 40, y: aIsoC1.y };
      const aIsoM1 = { id: nextAtomId++, element: 'C', x: aIsoCH.x - 30, y: aIsoCH.y - 30 };
      const aIsoM2 = { id: nextAtomId++, element: 'C', x: aIsoCH.x - 30, y: aIsoCH.y + 30 };
      const aProC1 = { id: nextAtomId++, element: 'C', x: a1.x + 45, y: a1.y };
      const aProMe = { id: nextAtomId++, element: 'C', x: aProC1.x, y: aProC1.y - 40 };
      const aProCOOH = { id: nextAtomId++, element: 'C', x: aProC1.x + 45, y: aProC1.y };
      const aProO1 = { id: nextAtomId++, element: 'O', x: aProCOOH.x + 30, y: aProCOOH.y - 25 };
      const aProO2 = { id: nextAtomId++, element: 'O', x: aProCOOH.x + 30, y: aProCOOH.y + 25 };
      atoms.push(aIsoC1, aIsoCH, aIsoM1, aIsoM2, aProC1, aProMe, aProCOOH, aProO1, aProO2);
      bonds.push(
        { atom1Id: a4.id, atom2Id: aIsoC1.id, order: 1 },
        { atom1Id: aIsoC1.id, atom2Id: aIsoCH.id, order: 1 },
        { atom1Id: aIsoCH.id, atom2Id: aIsoM1.id, order: 1 },
        { atom1Id: aIsoCH.id, atom2Id: aIsoM2.id, order: 1 },
        { atom1Id: a1.id, atom2Id: aProC1.id, order: 1 },
        { atom1Id: aProC1.id, atom2Id: aProMe.id, order: 1 },
        { atom1Id: aProC1.id, atom2Id: aProCOOH.id, order: 1 },
        { atom1Id: aProCOOH.id, atom2Id: aProO1.id, order: 2 },
        { atom1Id: aProCOOH.id, atom2Id: aProO2.id, order: 1 }
      );
    }

    render();
    calculateProperties();
  }

  function render() {
    if (!ctx) return;
    const w = canvas.width;
    const h = canvas.height;

    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, w, h);

    ctx.fillStyle = '#1e293b';
    for (let x = 20; x < w; x += 25) {
      for (let y = 20; y < h; y += 25) {
        ctx.fillRect(x, y, 1.5, 1.5);
      }
    }

    for (let b of bonds) {
      const a1 = atoms.find(a => a.id === b.atom1Id);
      const a2 = atoms.find(a => a.id === b.atom2Id);
      if (!a1 || !a2) continue;
      drawBond(a1, a2, b.order);
    }

    for (let a of atoms) {
      drawAtom(a);
    }
  }

  function drawBond(a1, a2, order) {
    const dx = a2.x - a1.x;
    const dy = a2.y - a1.y;
    const len = Math.hypot(dx, dy);
    if (len === 0) return;

    const nx = -dy / len;
    const ny = dx / len;
    const offset = 3.5;

    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 2.4;
    ctx.lineCap = 'round';

    if (order === 1) {
      ctx.beginPath();
      ctx.moveTo(a1.x, a1.y);
      ctx.lineTo(a2.x, a2.y);
      ctx.stroke();
    } else if (order === 2) {
      ctx.beginPath();
      ctx.moveTo(a1.x + nx * offset, a1.y + ny * offset);
      ctx.lineTo(a2.x + nx * offset, a2.y + ny * offset);
      ctx.moveTo(a1.x - nx * offset, a1.y - ny * offset);
      ctx.lineTo(a2.x - nx * offset, a2.y - ny * offset);
      ctx.stroke();
    } else if (order === 3) {
      ctx.beginPath();
      ctx.moveTo(a1.x, a1.y);
      ctx.lineTo(a2.x, a2.y);
      ctx.moveTo(a1.x + nx * (offset * 1.5), a1.y + ny * (offset * 1.5));
      ctx.lineTo(a2.x + nx * (offset * 1.5), a2.y + ny * (offset * 1.5));
      ctx.moveTo(a1.x - nx * (offset * 1.5), a1.y - ny * (offset * 1.5));
      ctx.lineTo(a2.x - nx * (offset * 1.5), a2.y - ny * (offset * 1.5));
      ctx.stroke();
    }
  }

  function drawAtom(a) {
    const radius = 13;
    const col = elementColors[a.element] || '#cbd5e1';

    ctx.beginPath();
    ctx.arc(a.x, a.y, radius, 0, Math.PI * 2);
    ctx.fillStyle = '#1e293b';
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = col;
    ctx.stroke();

    ctx.fillStyle = col;
    ctx.font = 'bold 12px "Fira Code", monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(a.element, a.x, a.y);
  }

  function calculateProperties() {
    let counts = { C: 0, N: 0, O: 0, S: 0, P: 0, F: 0, Cl: 0, Br: 0, H: 0 };
    let hbd = 0;
    let hba = 0;
    let tpsa = 0;
    let logp = 0;

    for (let a of atoms) {
      if (counts[a.element] !== undefined) {
        counts[a.element]++;
      } else {
        counts[a.element] = 1;
      }

      let valence = 0;
      bonds.forEach(b => {
        if (b.atom1Id === a.id || b.atom2Id === a.id) {
          valence += b.order;
        }
      });

      let targetValence = (a.element === 'C') ? 4 : (a.element === 'N' ? 3 : (a.element === 'O' ? 2 : 1));
      let implicitH = Math.max(0, targetValence - valence);
      counts.H += implicitH;

      if (a.element === 'O') {
        hba++;
        if (implicitH > 0) {
          hbd++;
          tpsa += 20.23;
          logp -= 0.4;
        } else {
          tpsa += 9.23;
          logp -= 0.1;
        }
      } else if (a.element === 'N') {
        hba++;
        if (implicitH > 0) {
          hbd += implicitH;
          tpsa += (implicitH === 1) ? 12.03 : 26.02;
          logp -= 0.6;
        } else {
          tpsa += 3.24;
          logp += 0.2;
        }
      } else if (a.element === 'C') {
        logp += 0.35;
      } else if (a.element === 'F') {
        logp += 0.14;
      } else if (a.element === 'Cl') {
        logp += 0.70;
      } else if (a.element === 'Br') {
        logp += 0.90;
      } else if (a.element === 'S') {
        logp += 0.45;
        tpsa += 28.2;
      }
    }

    let formula = '';
    if (counts.C > 0) formula += 'C' + (counts.C > 1 ? counts.C : '');
    if (counts.H > 0) formula += 'H' + (counts.H > 1 ? counts.H : '');
    ['N', 'O', 'S', 'P', 'F', 'Cl', 'Br'].forEach(el => {
      if (counts[el] > 0) formula += el + (counts[el] > 1 ? counts[el] : '');
    });
    if (!formula) formula = '-';

    let mw = 0;
    for (let el in counts) {
      if (atomicWeights[el]) {
        mw += counts[el] * atomicWeights[el];
      }
    }

    let smiles = generateSmiles();

    let violations = 0;
    if (mw > 500) violations++;
    if (logp > 5) violations++;
    if (hbd > 5) violations++;
    if (hba > 10) violations++;
    let ro5Score = 4 - violations;

    const elFormula = document.getElementById('sketch-formula-val');
    const elMw = document.getElementById('sketch-mw-val');
    const elLogp = document.getElementById('sketch-logp-val');
    const elTpsa = document.getElementById('sketch-tpsa-val');
    const elHbd = document.getElementById('sketch-hbd-val');
    const elHba = document.getElementById('sketch-hba-val');
    const elSmiles = document.getElementById('sketch-smiles-val');
    const elRo5Title = document.getElementById('sketch-ro5-title');
    const elRo5Desc = document.getElementById('sketch-ro5-desc');
    const elRo5Box = document.getElementById('sketch-ro5-verdict');

    if (elFormula) elFormula.textContent = formula;
    if (elMw) elMw.textContent = mw.toFixed(2) + ' g/mol';
    if (elLogp) elLogp.textContent = logp.toFixed(2);
    if (elTpsa) elTpsa.textContent = tpsa.toFixed(2) + ' Å²';
    if (elHbd) elHbd.textContent = hbd;
    if (elHba) elHba.textContent = hba;
    if (elSmiles) elSmiles.textContent = smiles || 'Gambarkan molekul...';

    if (elRo5Title && elRo5Box) {
      if (atoms.length === 0) {
        elRo5Title.textContent = 'Kanvas Kosong';
        if (elRo5Desc) elRo5Desc.textContent = 'Tempatkan atom untuk menghitung deskriptor.';
        elRo5Box.className = 'sketch-ro5-verdict-box';
      } else if (violations === 0) {
        elRo5Title.textContent = 'Lolos Lipinski RO5 (' + ro5Score + '/4)';
        if (elRo5Desc) elRo5Desc.textContent = 'Molekul memenuhi seluruh kriteria kelayakan bioavailabilitas oral.';
        elRo5Box.className = 'sketch-ro5-verdict-box pass';
      } else {
        elRo5Title.textContent = 'Peringatan RO5 (' + ro5Score + '/4)';
        if (elRo5Desc) elRo5Desc.textContent = 'Terdeteksi ' + violations + ' pelanggaran batas Lipinski (permeabilitas berisiko).';
        elRo5Box.className = 'sketch-ro5-verdict-box warn';
      }
    }

    currentCalculated = { formula, mw, logp, tpsa, hbd, hba, smiles, violations, ro5Score };
  }

  function generateSmiles() {
    if (atoms.length === 0) return '';
    const nC = atoms.filter(a => a.element === 'C').length;
    const nO = atoms.filter(a => a.element === 'O').length;
    const nN = atoms.filter(a => a.element === 'N').length;
    const hasBenzene = bonds.filter(b => b.order === 2).length >= 3 && nC >= 6;

    if (hasBenzene && nO === 4 && nC === 9) return 'CC(=O)OC1=CC=CC=C1C(=O)O'; // Aspirin
    if (hasBenzene && nO === 2 && nN === 1 && nC === 8) return 'CC(=O)NC1=CC=C(O)C=C1'; // Paracetamol
    if (hasBenzene && nO === 2 && nC === 13) return 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O'; // Ibuprofen
    if (hasBenzene && nO === 2 && nC === 7) return 'C1=CC=C(C=C1)C(=O)O'; // Benzoic acid
    if (hasBenzene && nO === 0 && nN === 0 && nC === 6) return 'C1=CC=CC=C1'; // Benzene
    if (hasBenzene && nN === 1 && nC === 5) return 'C1=CC=NC=C1'; // Pyridine

    let parts = [];
    atoms.forEach(a => parts.push(a.element));
    return parts.join('');
  }

  function pushToMainAnalyzer() {
    if (!currentCalculated || !currentCalculated.smiles) {
      alert('Silakan gambarkan molekul terlebih dahulu.');
      return;
    }
    const query = currentCalculated.smiles;
    const searchInput = document.getElementById('compound-search-input');
    const btnSearch = document.getElementById('btn-search');

    if (searchInput && btnSearch) {
      searchInput.value = query;
      const firstTab = document.querySelector('.tab-btn[data-tab="tab-3d-overview"]');
      if (firstTab) firstTab.click();
      btnSearch.click();
    }
  }

  return {
    init: init,
    render: render,
    loadScaffold: loadScaffold,
    calculateProperties: calculateProperties
  };
})();
