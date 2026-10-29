/**
 * PharmaPulse 3D - CADD Suite Orchestrator
 * Connects all CADD extensions to the application lifecycle
 */
(function() {
  'use strict';

  function initCaddSuite() {
    console.log('[PharmaPulse 3D] Menghidupkan CADD Suite Extensions...');

    if (window.CADD_PDB) window.CADD_PDB.init();
    if (window.CADD_Sketcher) window.CADD_Sketcher.init();
    if (window.CADD_Docking) window.CADD_Docking.init();
    if (window.CADD_Notebook) window.CADD_Notebook.init();

    // Hook tab switches to trigger viewport resizes
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(t => {
      t.addEventListener('click', () => {
        const tabId = t.getAttribute('data-tab');
        if (tabId === 'tab-pdb-target' && window.CADD_PDB) {
          setTimeout(() => {
            const v = window.CADD_PDB.viewer();
            if (v) {
              v.resize();
              v.zoomTo();
              v.render();
            }
          }, 150);
        } else if (tabId === 'tab-sketcher' && window.CADD_Sketcher) {
          setTimeout(() => {
            window.CADD_Sketcher.render();
          }, 150);
        }
      });
    });

    // Intercept renderSingleCompoundView if already defined
    if (typeof window.renderSingleCompoundView === 'function') {
      const origRender = window.renderSingleCompoundView;
      window.renderSingleCompoundView = function(data) {
        origRender.apply(this, arguments);
        triggerExtensionsUpdate(data);
      };
    }

    // Trigger update on initial loaded compound if present
    if (window.currentCompoundData) {
      triggerExtensionsUpdate(window.currentCompoundData);
    }
  }

  function triggerExtensionsUpdate(data) {
    if (!data || !data.props) return;
    const p = data.props;

    if (window.CADD_Toxicity) {
      try { window.CADD_Toxicity.render(p); } catch (e) { console.warn('Tox err:', e); }
    }
    if (window.CADD_Bioisostere) {
      try { window.CADD_Bioisostere.render(p); } catch (e) { console.warn('Bio err:', e); }
    }
    if (window.CADD_TargetFishing) {
      try { window.CADD_TargetFishing.render(p); } catch (e) { console.warn('Targ err:', e); }
    }
    if (window.CADD_OpenFDA) {
      try { window.CADD_OpenFDA.render(p); } catch (e) { console.warn('FDA err:', e); }
    }
    if (window.CADD_PDB) {
      try {
        const suggested = window.CADD_PDB.suggestPDBForDrug(p.Title || '');
        if (suggested) {
          const sel = document.getElementById('pdb-select-preset');
          if (sel) sel.value = suggested;
          window.CADD_PDB.loadStructure(suggested);
        }
      } catch (e) { console.warn('PDB err:', e); }
    }
  }

  window.triggerCaddExtensions = triggerExtensionsUpdate;
  window.triggerExtensionsUpdate = triggerExtensionsUpdate;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCaddSuite);
  } else {
    initCaddSuite();
  }
})();
