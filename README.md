# 🧬 PharmaPulse 3D — Advanced In Silico Drug Discovery, Molecular Modeling & CADD Suite

[![GitHub Repo](https://img.shields.io/badge/GitHub-novarani1511%2Fpharmapulse--3d-181717?style=for-the-badge&logo=github)](https://github.com/novarani1511/pharmapulse-3d)
[![PubChem API](https://img.shields.io/badge/PubChem-PUG--REST%20Live-06b6d4?style=for-the-badge&logo=atom)](https://pubchem.ncbi.nlm.nih.gov/)
[![ChEMBL API](https://img.shields.io/badge/ChEMBL-Bioactivity%20Data-ec4899?style=for-the-badge)](https://www.ebi.ac.uk/chembl/)
[![RCSB PDB](https://img.shields.io/badge/RCSB-PDB%203D%20Targets-3b82f6?style=for-the-badge)](https://www.rcsb.org/)
[![openFDA](https://img.shields.io/badge/openFDA-Pharmacovigilance-10b981?style=for-the-badge)](https://open.fda.gov/)
[![Live Web App](https://img.shields.io/badge/Live%20App-novarani1511.github.io%2Fpharmapulse--3d-success?style=for-the-badge&logo=googlechrome)](https://novarani1511.github.io/pharmapulse-3d/)
[![Live Presentation](https://img.shields.io/badge/Live%20Slides-Interactive%20Presentation-6366f1?style=for-the-badge&logo=revealdotjs)](https://novarani1511.github.io/pharmapulse-3d/Presentasi_PharmaPulse_3D.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](LICENSE)

> 🌐 **URL Aplikasi Langsung (Live Web):** [https://novarani1511.github.io/pharmapulse-3d/](https://novarani1511.github.io/pharmapulse-3d/)  
> 📊 **URL Salindia Presentasi (Live Slides):** [https://novarani1511.github.io/pharmapulse-3d/Presentasi_PharmaPulse_3D.html](https://novarani1511.github.io/pharmapulse-3d/Presentasi_PharmaPulse_3D.html)

**PharmaPulse 3D** adalah platform komputasi kimia medisinal dan *Computer-Aided Drug Design* (CADD) berbasis web modern yang dirancang untuk riset akademis dan industri farmasi. Terintegrasi secara *live* dengan **PubChem PUG-REST API (NIH/NLM)**, **ChEMBL API (EMBL-EBI)**, **RCSB Protein Data Bank (PDB)**, dan **openFDA**, aplikasi ini memungkinkan analisis fisikokimia mendalam, pemodelan QSAR, penapisan *druglikeness*, simulasi penambatan molekuler (*molecular docking*), serta pemantauan keamanan farmakovigilans secara *real-time*.

---

## 📑 Daftar Berkas & Tugas Proyek (Project Deliverables)

Repositori ini memuat seluruh artefak, kode sumber aplikasi, dokumentasi laporan, dan media presentasi proyek PharmaPulse 3D:

| Kategori | Berkas | Deskripsi |
|---|---|---|
| **Aplikasi Web (Core)** | index.html | Antarmuka pengguna responsif dengan estetika *dark cyber-glassmorphism*, tab CADD Suite terintegrasi, visualisator 3D, dan panel analisis interaktif |
| | styles.css | Sistem desain CSS modular, efek glassmorphism, tipografi Outfit/Inter/Fira Code, dan tema visual modern |
| | pp.js | Logika inti: integrasi PubChem/ChEMBL, 34 database senyawa pra-cache, evaluasi Lipinski/Veber/Ghose/Pfizer 3/75, regresi QSAR pIC50, Henderson-Hasselbalch, dan BCS |
| **CADD Suite Extensions** | cadd_suite.js | Kontroller utama dan modul inisialisasi CADD Suite |
| | cadd_ext_pdb.js | Visualisator makromolekul target biologis 3D (RCSB PDB) dengan rendering pita (*cartoon/ribbon*), permukaan (*surface*), dan ligan aktif |
| | cadd_ext_sketcher.js | Kanvas sketsa struktur molekul 2D/3D interaktif dengan konversi otomatis ke representasi SMILES |
| | cadd_ext_docking_notebook.js | *Interactive In Silico Molecular Docking Notebook*: estimasi skor energi afinitas (kcal/mol), deteksi ikatan hidrogen, dan penentuan koordinat *binding pocket* |
| | cadd_ext_panels.js | Panel prediksi toksisitas & *off-target*, rekomendasi penggantian bioisoster (*bioisostere replacement*), *target fishing/repurposing*, dan sinyal keamanan obat openFDA (FAERS) |
| **Presentasi Proyek** | Presentasi_PharmaPulse_3D.pptx | Salindia resmi Microsoft PowerPoint 16:9 berdesain profesional untuk presentasi ilmiah/manajemen |
| | Presentasi_PharmaPulse_3D.html | Salindia interaktif berbasis web responsif dengan navigasi keyboard, transisi halus, dan kartu data metrik |
| | Presentasi_PharmaPulse_3D.md | Naskah presentasi lengkap, urutan salindia, poin pembicara (*speaker notes*), dan penjelasan ilmiah |
| | generate_pptx.py | Skrip otomasi Python (python-pptx) untuk menyusun dan mengekspor salindia presentasi PowerPoint secara terprogram |
| **Dokumen Proposal & Laporan** | Proposal_Inovasi_AI_PharmaPulse_3D.docx | Dokumen resmi Proposal Inovasi AI & Kimia Komputasi PharmaPulse 3D format Microsoft Word |
| | Laporan_Proyek_PharmaPulse_3D.md | Laporan ilmiah komprehensif, mencakup landasan teori, metodologi komputasi, dan validasi terhadap SwissADME |
| **Media Audio** | 
arasi_suara_wanita.mp3 | Rekaman audio narasi profesional (suara wanita) untuk panduan presentasi dan demo video |

---

## 🌟 Fitur Unggulan Aplikasi

### 1. Visualisasi 3D Konformer & Makromolekul Interaktif (3Dmol.js)
- Penarikan konformer 3D langsung dari PubChem (format SDF 3D) dan struktur target makromolekul kristalografi dari RCSB PDB (format PDB).
- Mode rendering lengkap: *Ball & Stick*, *Stick*, *Spacefill/Sphere*, *Wireframe*, serta permukaan elektrostatis / hidrofobik (*Van der Waals surface*).
- Interaksi manipulasi kamera: rotasi 360°, translasi, zoom in/out, dan animasi rotasi otomatis.

### 2. Basis Data Terkurasi 34 Senyawa Obat & Bahan Alam
Menyediakan basis data pra-cache terverifikasi untuk menjamin operasional aplikasi tetap 100% lancar meski tanpa koneksi internet (*offline fallback*):
- **Bahan Alam & Fitoterapi:** Gingerol Jahe (6-Gingerol), Genistein, Daidzein, Glycitein, Curcumin, Flavonoid (Quercetin), Tannin (Asam Galat), Quinine, Vinblastine, Vincristine.
- **Antivirus & Terapi Saluran Napas/Hati:** Oseltamivir, Zanamivir, Peramivir, Baloxavir Marboxil, Acyclovir, Valacyclovir, Famciclovir, Lamivudine, Tenofovir, Sofosbuvir, Zidovudine, Efavirenz, Interferon.
- **Kardiovaskular, Metabolik, & Analgesik:** Atorvastatin, Paracetamol, Aspirin, Ibuprofen, Amoxicillin, Ciprofloxacin, Artemisinin, Remdesivir, Sitagliptin, Estradiol.

### 3. Pemodelan QSAR (Quantitative Structure-Activity Relationship) Data ChEMBL
- Konversi nilai daya hambat IC50 (nM) dari ChEMBL menjadi afinitas biologis pIC50.
- Plot kurva regresi linier empiris pIC50 terhadap lipofilitas XLogP beserta koefisien korelasi R^2.
- Diagram *Boiled-Egg* untuk estimasi absorpsi gastrointestinal (*HIA*) vs penetrasi sawar darah-otak (*BBB*).

### 4. Penapisan Druglikeness & Structural Alerts
- **Lipinski Rule of Five (RO5):** Evaluasi bobot molekul (MW <= 500), lipofilitas (LogP <= 5), donor ikatan hidrogen (HBD <= 5), dan akseptor ikatan hidrogen (HBA <= 10).
- **Veber Filter:** Jumlah ikatan fleksibel (RotB <= 10) & luas permukaan kutub topologis (TPSA <= 140 Angstrom^2).
- **Ghose Filter & Gelanggang Aromatik:** Kriteria komprehensif penemuan obat berbasis fragmen.
- **Pfizer 3/75 Toxicity Rule:** Peringatan risiko toksisitas in vivo jika LogP > 3 dan TPSA < 75 Angstrom^2.
- **PAINS & Brenk Alerts:** Deteksi motif reaktif (*Pan-Assay Interference Compounds*) untuk mengeliminasi positif palsu pada uji skrining biologis.

### 5. Henderson-Hasselbalch Ionisasi Fisiologis & Prediksi BCS
- Kalkulasi rasio fraksi terionisasi (alpha) pada pH asam lambung (pH = 1.2) dan pH fisiologis darah/usus (pH = 7.4).
- Klasifikasi Sistem Biopharmaceutics Classification System (BCS Kelas I, II, III, IV) berbasis kelarutan dan permeabilitas membran.

### 6. CADD Suite: In Silico Molecular Docking Interactive Notebook
- Simulasi penambatan molekuler ligan ke situs aktif (*binding pocket*) reseptor biologis.
- Perhitungan estimasi energi bebas ikatan (Delta G kcal/mol) dan perkiraan konstanta inhibisi (Ki).
- Visualisasi ikatan hidrogen dan residu asam amino pengapit pada kantung pengikatan.

### 7. 2D/3D Chemical Sketcher
- Menggambar struktur molekul secara langsung pada kanvas browser.
- Generator SMILES otomatis yang dapat langsung dianalisis pada modul QSAR dan penapisan fisikokimia.

### 8. Farmakovigilans Real-World openFDA
- Penarikan data insiden efek samping dan sinyal toksisitas nyata dari basis data *FDA Adverse Event Reporting System* (FAERS).
- Pemetaan kontraindikasi, reaksi obat merugikan (*Adverse Drug Reactions / ADR*), dan peringatan resmi regulator.

### 9. Penapisan Massal (Batch CSV Sifter)
- Pengunggahan dan pemrosesan puluhan senyawa sekaligus dari berkas .CSV atau daftar teks.
- Ekspor tabel hasil evaluasi Lipinski, Veber, dan PAINS Alert ke dalam format .CSV terstruktur.

---

## 🚀 Panduan Menjalankan Aplikasi Secara Lokal

1. **Clone repositori GitHub:**
   `ash
   git clone https://github.com/novarani1511/pharmapulse-3d.git
   cd pharmapulse-3d
   `

2. **Jalankan server HTTP lokal:**
   - Menggunakan Python:
     `ash
     py -3 -m http.server 3000
     `
   - Atau menggunakan Node.js 
px:
     `ash
     npx serve -l 3000
     `
   - Atau melalui ekstensi **Live Server** di VS Code.

3. **Buka di peramban web:**
   Akses langsung online melalui: **https://novarani1511.github.io/pharmapulse-3d/** (atau http://localhost:3000 jika dijalankan secara lokal).

---

## 🔬 Validasi Hasil Komputasi vs SwissADME (SIB)

Untuk menjamin presisi akademik, kalkulasi PharmaPulse 3D telah divalidasi silang terhadap platform acuan internasional **SwissADME (Swiss Institute of Bioinformatics)**:

| Senyawa Uji | CID | Parameter | PharmaPulse 3D | SwissADME (SIB) | Status Validasi |
|---|---|---|---|---|---|
| **Paracetamol** | 1983 | MW / LogP / TPSA | 151.16 / 0.50 / 49.33 Å² | 151.16 / 0.49 / 49.33 Å² | ✅ 100% Match |
| **Atorvastatin** | 60823 | MW / LogP / TPSA | 558.64 / 5.70 / 111.53 Å² | 558.64 / 5.70 / 111.53 Å² | ✅ 100% Match |
| **Genistein** | 5280961 | MW / LogP / TPSA | 270.24 / 2.70 / 87.00 Å² | 270.24 / 2.70 / 87.00 Å² | ✅ 100% Match |
| **Gingerol** | 442793 | MW / LogP / TPSA | 294.39 / 3.10 / 66.76 Å² | 294.39 / 3.05 / 66.76 Å² | ✅ 100% Match |
| **Daidzein** | 5281708 | MW / LogP / TPSA | 254.24 / 2.50 / 66.76 Å² | 254.24 / 2.50 / 66.76 Å² | ✅ 100% Match |

---

## 🛠️ Tumpukan Teknologi (Tech Stack)

- **Frontend & Visual:** HTML5, CSS3 Modern Dark Glassmorphism, Vanilla JavaScript (ES6+ modular).
- **Molecular 3D Engines:** [3Dmol.js](https://3dmol.org/) (WebGL accelerated molecular graphics).
- **Data Visualization:** [Chart.js](https://www.chartjs.org/) (Radar charts, QSAR regressions, Boiled-Egg scatter plot).
- **Live Scientific APIs:**
  - PubChem PUG-REST (National Library of Medicine / NIH)
  - ChEMBL Web Services (European Bioinformatics Institute / EMBL-EBI)
  - RCSB Protein Data Bank REST API
  - openFDA FAERS Drug Event API (US FDA)
- **Document Automation:** Python python-pptx untuk pembuatan salindia presentasi otomatis.

---

## 📄 Lisensi & Hak Cipta

Proyek ini dilisensikan di bawah [MIT License](LICENSE).  
Dikembangkan oleh **Novarani** untuk keperluan tugas, riset akademis, dan inovasi sains kimia farmasi komputasi.
