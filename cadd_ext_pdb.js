/**
 * PharmaPulse 3D - CADD Suite: Target Macromolecule PDB Viewer
 * Integrates RCSB PDB 3D Protein-Ligand Co-Crystals & Active Site Analysis
 */
window.CADD_PDB = (function() {
  'use strict';

  let viewer = null;
  let currentPdbId = '1HWK';
  let isSpinning = true;
  let isSurfaceOn = false;
  let showBindingResidues = true;
  let surfaceObj = null;

  const presets = {
    '1HWK': {
      title: 'Human HMG-CoA Reductase Catalytic Domain complexed with Atorvastatin',
      organism: 'Homo sapiens',
      res: '2.22 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Atorvastatin (Lipitor)',
      target: 'HMG-CoA Reductase (EC 1.1.1.88)',
      residues: ['Ser565', 'Arg590', 'Lys735', 'Asp690', 'Glu559', 'Val805', 'Leu853', 'Ala856'],
      notes: [
        'Ikatan Hidrogen: Gugus dihidroksi heptanoat membentuk jejaring ikatan hidrogen kuat dengan Ser565, Arg590, dan Asp690.',
        'Interaksi Hidrofobik: Cincin pirol, fluoro-fenil, dan isopropil menempati saku lipofilik yang dibatasi oleh Leu853 dan Val805.',
        'Jembatan Garam: Karboksilat terminal ligan berinteraksi elektrostatik dengan gugus kationik Lys735.'
      ]
    },
    '1CX2': {
      title: 'Murine Cyclooxygenase-2 (COX-2) complexed with selective inhibitor Celecoxib',
      organism: 'Mus musculus',
      res: '3.00 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Celecoxib (Celebrex)',
      target: 'Prostaglandin G/H Synthase 2 (COX-2)',
      residues: ['Arg120', 'Tyr355', 'Val523', 'Ser530', 'Gln192', 'Phe518', 'Leu352'],
      notes: [
        'Saku Selektivitas COX-2: Gugus sulfonamida Celecoxib masuk secara presisi ke dalam saku samping (side-pocket) hidrofilik Val523.',
        'Ikatan Hidrogen: Gugus sulfonamida berikatan hidrogen dengan Gln192 dan Arg513.',
        'Penghambatan Sterik: Residu Ile523 pada COX-1 menghalangi ligan ini, menghasilkan selektivitas COX-2 >300x.'
      ]
    },
    '4COX': {
      title: 'Ovine Cyclooxygenase-1 (COX-1) complexed with Salicylate / Aspirin',
      organism: 'Ovis aries',
      res: '2.90 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Aspirin / Salicylic Acid',
      target: 'Prostaglandin G/H Synthase 1 (COX-1)',
      residues: ['Ser529', 'Arg120', 'Tyr385', 'Trp387', 'Phe518', 'Ile523'],
      notes: [
        'Asetilasi Kovalen: Aspirin mentransfer gugus asetil secara ireversibel ke rantai samping Ser529 (Ser530 pada COX-2).',
        'Rintangan Ruang: Gugus asetil pada Ser529 memblok kanal hidrofobik asam arakidonat seumur hidup trombosit.',
        'Ikatan Ionik: Gugus karboksilat berlabuh pada residu Arg120 di mulut saluran katalitik.'
      ]
    },
    '4NOB': {
      title: 'Acetaminophen (Paracetamol) Binding Cavity & Catalytic Pocket Complex',
      organism: 'Homo sapiens / Ovis aries',
      res: '1.85 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Paracetamol (Acetaminophen)',
      target: 'Cyclooxygenase Peroxidase Subsite & TRPA1',
      residues: ['Tyr385', 'Ser530', 'Phe518', 'Leu352', 'Arg120'],
      notes: [
        'Inhibisi Peroksidase: Paracetamol mereduksi radikal tirosil katalitik (Tyr385) pada siklus peroksidase COX.',
        'Ikatan Hidrogen: Gugus fenolik -OH berikatan hidrogen dengan Ser530.',
        'Metabolit Aktif: Di SSP diubah oleh FAAH menjadi AM404 yang mengaktivasi reseptor kanabinoid CB1.'
      ]
    },
    '1IEP': {
      title: 'Human Abl Kinase Domain in complex with Imatinib (Gleevec)',
      organism: 'Homo sapiens',
      res: '2.10 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Imatinib (STI571 / Gleevec)',
      target: 'BCR-Abl Tyrosine Kinase (Onkologi)',
      residues: ['Thr315', 'Glu286', 'Met318', 'Asp381', 'Phe382', 'Val256'],
      notes: [
        'Konformasi DFG-Out: Imatinib mengikat konformasi inaktif dari kinase domain, menstabilkan konformasi DFG-out (Asp381-Phe382-Gly383).',
        'Gatekeeper Residue: Gugus piridinil bertetangga dengan residu penjaga pintu Thr315. Mutasi T315I memicu resistensi klinis.',
        'H-Bond Hinge: Ikatan hidrogen antara amida Imatinib dan Glu286 serta Asp381.'
      ]
    },
    '2XCT': {
      title: 'Acinetobacter baumannii Topoisomerase IV with Ciprofloxacin & DNA',
      organism: 'Acinetobacter baumannii',
      res: '2.50 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Ciprofloxacin',
      target: 'DNA Gyrase / Topoisomerase IV',
      residues: ['Ser84', 'Glu88', 'Arg121', 'Asp87', 'Gly81'],
      notes: [
        'Jembatan Magnesium Ion (Mg2+): Karboksilat dan keto oksigen Ciprofloxacin mengkhelat ion Mg2+ terhidrasi.',
        'Residu Penentu Resistensi (QRDR): Ser84 dan Glu88 mengkoordinasikan jembatan air Mg2+.',
        'Interkalasi DNA: Cincin quinolon berinterkalasi langsung di antara pasangan basa DNA yang terpotong.'
      ]
    },
    '1PME': {
      title: 'Penicillin-Binding Protein 2a (PBP2a) in complex with beta-lactam core',
      organism: 'Staphylococcus aureus',
      res: '2.40 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Amoxicillin / Beta-Lactam Core',
      target: 'Transpeptidase / Penicillin-Binding Protein',
      residues: ['Ser403', 'Lys406', 'Asn464', 'Ser461', 'Thr600'],
      notes: [
        'Asilasi Kovalen: Ser403 melakukan serangan nukleofilik membuka cincin beta-laktam menjadi kompleks asil-enzim stabil.',
        'Inhibisi Dinding Sel: Reaksi transpeptidasi terhambat permanen mencegah cross-linking peptidoglikan bakteri.',
        'Motif SXXK: Gugus amina Lys406 bertindak sebagai basa umum memfasilitasi deprotonasi Ser403.'
      ]
    },
    '2HU4': {
      title: 'Avian Influenza H5N1 Neuraminidase complexed with Oseltamivir (Tamiflu)',
      organism: 'Influenza A virus H5N1',
      res: '2.50 Å',
      method: 'X-RAY DIFFRACTION',
      drug: 'Oseltamivir Carboxylate',
      target: 'Viral Neuraminidase (Sialidase)',
      residues: ['Arg118', 'Glu119', 'Asp151', 'Arg292', 'Glu276', 'Arg371'],
      notes: [
        'Triad Arginin: Gugus karboksilat berlabuh kuat pada triad arginin konservatif (Arg118, Arg292, Arg371).',
        'Rotasi Glu276: Rantai samping lipofilik pentil eter memaksa Glu276 berotasi membentuk saku hidrofobik.',
        'Transisi Asam Sialat: Meniru geometri keadaan transisi planar glikosil.'
      ]
    },
    '7BV2': {
      title: 'SARS-CoV-2 RNA-dependent RNA polymerase (RdRp) with Remdesivir RNA',
      organism: 'SARS-CoV-2',
      res: '2.50 Å',
      method: 'CRYO-ELECTRON MICROSCOPY',
      drug: 'Remdesivir Monophosphate (RTP)',
      target: 'Viral RdRp (nsp12/nsp7/nsp8)',
      residues: ['Ser759', 'Asp760', 'Asp761', 'Asn691', 'Arg555'],
      notes: [
        'Triad Katalitik nsp12: Residu Ser759-Asp760-Asp761 mengkoordinasikan ion magnesium penggabung nukleotida.',
        'Terminasi Tertunda (+3): Gugus 1-siano pada Remdesivir menimbulkan benturan sterik dengan Ser861 setelah transkripsi 3 nukleotida berikutnya.',
        'Interaksi Basa: Gugus 1-siano membentuk kontak polar tambahan menstabilkan ikatan pada cetakan RNA viral.'
      ]
    }
  };

  function init() {
    const container = document.getElementById('pdb-viewport');
    if (!container || !window.$3Dmol) return;

    if (!viewer) {
      viewer = $3Dmol.createViewer(container, {
        defaultcolors: $3Dmol.rasmolElementColors
      });
    }

    setupEvents();
    loadStructure(currentPdbId);
  }

  function setupEvents() {
    const presetSelect = document.getElementById('pdb-select-preset');
    if (presetSelect) {
      presetSelect.addEventListener('change', (e) => {
        loadStructure(e.target.value);
      });
    }

    const btnFetch = document.getElementById('btn-fetch-pdb');
    const inputCustom = document.getElementById('pdb-custom-input');
    if (btnFetch && inputCustom) {
      btnFetch.addEventListener('click', () => {
        const code = inputCustom.value.trim().toUpperCase();
        if (code.length === 4) {
          loadStructure(code);
        } else {
          alert('Silakan ketik 4 karakter kode PDB yang valid (misal: 1HWK, 1CX2, 6LU7, 1M17).');
        }
      });
      inputCustom.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') btnFetch.click();
      });
    }

    const styleSelect = document.getElementById('pdb-render-style');
    if (styleSelect) {
      styleSelect.addEventListener('change', () => applyStyling());
    }

    const btnSurface = document.getElementById('btn-toggle-surface');
    if (btnSurface) {
      btnSurface.addEventListener('click', () => {
        isSurfaceOn = !isSurfaceOn;
        btnSurface.classList.toggle('active', isSurfaceOn);
        toggleSurface();
      });
    }

    const btnResidues = document.getElementById('btn-toggle-binding-residues');
    if (btnResidues) {
      btnResidues.addEventListener('click', () => {
        showBindingResidues = !showBindingResidues;
        btnResidues.classList.toggle('active', showBindingResidues);
        applyStyling();
      });
    }

    const btnSpin = document.getElementById('btn-pdb-spin');
    if (btnSpin) {
      btnSpin.addEventListener('click', () => {
        isSpinning = !isSpinning;
        if (viewer) viewer.spin(isSpinning);
        btnSpin.classList.toggle('active', isSpinning);
      });
    }

    const btnReset = document.getElementById('btn-pdb-reset');
    if (btnReset) {
      btnReset.addEventListener('click', () => {
        if (viewer) {
          viewer.zoomTo();
          viewer.render();
        }
      });
    }
  }

  async function loadStructure(pdbId) {
    currentPdbId = pdbId.toUpperCase();
    const statusEl = document.getElementById('pdb-load-status');
    if (statusEl) {
      statusEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Mengunduh kristal 3D PDB (' + currentPdbId + ') dari RCSB...';
      statusEl.style.color = 'var(--color-primary)';
    }

    try {
      const url = 'https://files.rcsb.org/download/' + currentPdbId + '.pdb';
      const res = await fetch(url);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const pdbText = await res.text();

      renderPdb(pdbText);
      updateMetadata(currentPdbId);

      if (statusEl) {
        statusEl.innerHTML = '<i class="fa-solid fa-circle-check"></i> Struktur 3D ' + currentPdbId + ' Berhasil Dimuat';
        statusEl.style.color = 'var(--color-success)';
      }
    } catch (err) {
      console.warn('Fallback ke metadata kurasi lokal:', err);
      if (statusEl) {
        statusEl.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> RCSB offline/terbatas. Menampilkan metadata.';
        statusEl.style.color = 'var(--color-warning)';
      }
      updateMetadata(currentPdbId);
    }
  }

  function renderPdb(pdbText) {
    if (!viewer) return;
    viewer.clear();
    surfaceObj = null;

    viewer.addModel(pdbText, 'pdb');
    applyStyling();
    viewer.zoomTo();
    viewer.spin(isSpinning);
    viewer.render();
  }

  function applyStyling() {
    if (!viewer) return;
    const styleSelect = document.getElementById('pdb-render-style');
    const styleType = styleSelect ? styleSelect.value : 'spectrum';

    let cartoonStyle = { color: 'spectrum', opacity: 0.88 };
    if (styleType === 'ss') {
      cartoonStyle = { colorscheme: 'ssPyMOL', opacity: 0.9 };
    } else if (styleType === 'slate') {
      cartoonStyle = { color: '#64748b', opacity: 0.8 };
    } else if (styleType === 'chain') {
      cartoonStyle = { colorscheme: 'chainHetatm', opacity: 0.88 };
    }

    viewer.setStyle({ hetflag: false }, { cartoon: cartoonStyle });

    const ligandSel = { hetflag: true, not: { resn: ['HOH', 'WAT', 'DOD', 'SO4', 'PO4', 'CL', 'NA', 'MG'] } };
    viewer.setStyle(ligandSel, {
      stick: { colorscheme: 'greenCarbon', radius: 0.28 },
      sphere: { scale: 0.32 }
    });

    if (showBindingResidues) {
      viewer.addStyle(
        { within: { distance: 5.0, sel: ligandSel }, hetflag: false },
        { stick: { colorscheme: 'cyanCarbon', radius: 0.16 } }
      );
    }

    if (isSurfaceOn) {
      toggleSurface(true);
    }

    viewer.render();
  }

  function toggleSurface(forceState) {
    if (!viewer) return;
    if (surfaceObj) {
      viewer.removeSurface(surfaceObj);
      surfaceObj = null;
    }
    if (isSurfaceOn || forceState) {
      surfaceObj = viewer.addSurface($3Dmol.SurfaceType.MS, {
        opacity: 0.38,
        color: '#cbd5e1'
      });
    }
    viewer.render();
  }

  function updateMetadata(pdbId) {
    const data = presets[pdbId] || {
      title: 'Macromolecular Co-Crystal Complex ' + pdbId,
      organism: 'Terekspresi Ilmiah',
      res: 'Resolusi Tinggi',
      method: 'X-RAY DIFFRACTION',
      drug: 'Ligan Aktif',
      target: 'Enzim / Reseptor Target',
      residues: ['Residu Katalitik Saku Pengikatan', 'Donor Ikatan Hidrogen', 'Kontak Hidrofobik'],
      notes: ['Ligan terikat secara komplementer pada kantung aktif makromolekul target.']
    };

    const elId = document.getElementById('pdb-info-id');
    const elTitle = document.getElementById('pdb-info-title');
    const elMethod = document.getElementById('pdb-info-method');
    const elRes = document.getElementById('pdb-info-res');
    const elOrganism = document.getElementById('pdb-info-organism');
    const elResidues = document.getElementById('pdb-residues-list');
    const elNotes = document.getElementById('pdb-interaction-notes');
    const elLink = document.getElementById('pdb-link-rcsb');

    if (elId) elId.textContent = pdbId;
    if (elTitle) elTitle.textContent = data.title;
    if (elMethod) elMethod.textContent = data.method;
    if (elRes) elRes.textContent = data.res;
    if (elOrganism) elOrganism.innerHTML = '<i class="fa-solid fa-dna"></i> <em>' + data.organism + '</em> | Target: <strong>' + data.target + '</strong>';

    if (elResidues) {
      elResidues.innerHTML = data.residues.map(r => '<span class="residue-chip"><i class="fa-solid fa-circle-dot"></i> ' + r + '</span>').join('');
    }

    if (elNotes) {
      elNotes.innerHTML = data.notes.map(n => '<li>' + n + '</li>').join('');
    }

    if (elLink) {
      elLink.href = 'https://www.rcsb.org/structure/' + pdbId;
    }
  }

  function suggestPDBForDrug(drugName) {
    const d = (drugName || '').toLowerCase();
    if (d.includes('atorvastatin') || d.includes('lipitor')) return '1HWK';
    if (d.includes('celecoxib') || d.includes('celebrex')) return '1CX2';
    if (d.includes('aspirin') || d.includes('salicyl')) return '4COX';
    if (d.includes('paracetamol') || d.includes('acetaminophen')) return '4NOB';
    if (d.includes('imatinib') || d.includes('gleevec')) return '1IEP';
    if (d.includes('ciprofloxacin')) return '2XCT';
    if (d.includes('amoxicillin') || d.includes('penicillin')) return '1PME';
    if (d.includes('oseltamivir') || d.includes('tamiflu')) return '2HU4';
    if (d.includes('remdesivir')) return '7BV2';
    return null;
  }

  return {
    init: init,
    viewer: () => viewer,
    loadStructure: loadStructure,
    suggestPDBForDrug: suggestPDBForDrug
  };
})();
