---
marp: true
theme: default
paginate: true
header: 'PharmaPulse 3D - Platform CADD & In Silico Screening'
footer: 'Disusun oleh Novarani | https://github.com/novarani1511/pharmapulse-3d'
---

# 🧬 PharmaPulse 3D
### Platform CADD & In Silico Screening Terintegrasi Berbasis PubChem PUG-REST Live API

Aplikasi Web Berstandar Industri untuk Visualisasi Konformer 3D Molekul, Farmakofor 3D, Pengukuran Ikatan Spasial Atom (Å), Model Prediksi BOILED-Egg, Evaluasi Druglikeness Lipinski RO5, Kemudahan Sintesis (SA Score), Penapisan Analog Tanimoto Similarity, dan Drug Repurposing.

**Disusun oleh:** Novarani  
**Bidang:** Kimia Farmasi, Komputasi Medisinal & In Silico CADD  
**Repositori:** [github.com/novarani1511/pharmapulse-3d](https://github.com/novarani1511/pharmapulse-3d)  
**Server Demo:** http://localhost:3000

---

# ⚠️ 1. Latar Belakang & Urgensi CADD di Industri Farmasi

* **Krisis Biaya & Kegagalan Uji (Attrition Rate):**  
  Riset obat baru menelan biaya rata-rata .6 Miliar dengan durasi 10–15 tahun. Tingkat kegagalan fase klinis mencapai >90%, sebagian besar akibat profil farmakokinetik (ADMET) yang buruk.
* **Keterbatasan Software CADD Konvensional:**  
  Software CADD profesional (MOE, Schrodinger, Discovery Studio) berlisensi ribuan dolar dan membutuhkan workstation komputasi berat.
* **Solusi Inovasi PharmaPulse 3D:**  
  Platform berbasis web murni (*zero-installation*), gratis, dan open-access yang menghubungkan data live PubChem NIH/NLM dengan algoritma komputasi industri farmasi.

---

# 🔄 2. Arsitektur Sistem & Alur Kerja Terpadu

1. **Live Data Ingestion Layer:**  
   Query asinkron ke PubChem PUG-REST API (NIH/NLM) untuk mengambil CID, IUPAC, SMILES, file konformer 3D SDF, dan 15+ deskriptor fisikokimia.
2. **CADD Analytics Engine:**  
   Algoritma JavaScript di sisi klien untuk evaluasi Lipinski RO5, Veber, Ghose, Pfizer 3/75, Model BOILED-Egg, SA Score, dan regresi QSAR ChEMBL.
3. **High-Aesthetic UI/UX:**  
   Viewer 3Dmol.js WebGL, overlay Farmakofor 3D, pengukur jarak ikatan (Å), dan ekspor dokumen ilmiah resmi siap publikasi.

---

# 🛡️ 3. Evaluasi Fisikokimia & Druglikeness Standar

* **Lipinski's Rule of Five (RO5):**
  *  \le 500	ext{ g/mol}$ (Difusi membran optimal)
  * $	ext{LogP} \le 5.0$ (Keseimbangan hidrofilik-lipofilik)
  * $	ext{HBD} \le 5$ (Energi desolvasi ikatan hidrogen)
  * $	ext{HBA} \le 10$ (Membatasi luas polaritas)
* **Saringan Tambahan:**
  * **Veber Filter:** $	ext{RotB} \le 10$ & $	ext{TPSA} \le 140	ext{ Å}^2$ (Bioavailabilitas oral tinggi)
  * **Ghose Filter:** Rentang database obat komersial
  * **Pfizer 3/75 Rule:** Deteksi risiko toksisitas in vivo 2.5x lebih tinggi ($	ext{LogP} > 3$ & $	ext{TPSA} < 75	ext{ Å}^2$)

---

# 📈 4. Pemodelan QSAR (pIC50), SwissADME Radar & PAINS

* **Pemodelan QSAR ChEMBL:**  
  Plot regresi linier bioaktivitas {50} = -\log_{10}(IC_{50})$ terhadap deskriptor lipofilitas dengan persamaan otomatis (^2 > 0.8$).
* **SwissADME 6-Axis Radar:**  
  Visualisasi radar heksagonal kelayakan bioavailabilitas: LIPO, SIZE, POLAR, INSOLU, FLEX, dan INSATU.
* **Peringatan Struktur PAINS & Brenk:**  
  Deteksi motif pengganggu assay laboratorium (quinone, catecol, azo) dan gugus toksik terlarang.

---

# 🎯 5. Inovasi 3D CADD: Farmakofor & Pengukuran Ikatan Spasial

* **3D Pharmacophore Feature Mapping:**
  * 🔴 **Bola Merah (HBA):** Akseptor ikatan hidrogen (O & N non-protonasi).
  * 🔵 **Bola Biru (HBD):** Donor ikatan hidrogen aktif (-OH & -NH).
  * 🟡 **Bola Kuning (Aromatic/Hydrophobic):** Cincin aromatik & gugus lipofilik.
* **Alat Ukur Jarak & Sudut Ikatan 3D:**
  * **Jarak Euclidean (Å):** Klik 2 atom berurutan untuk menghitung jarak riil  = \sqrt{dx^2 + dy^2 + dz^2}$ dalam satuan Ångström.
  * **Sudut Ikatan (°):** Klik 3 atom untuk menghitung sudut ikatan via vector dot product.

---

# 🍳 6. Inovasi ADMET: Model Prediksi BOILED-Egg

* **Berdasarkan Model Global Daina & Zoete (ChemMedChem 2016):**  
  Plot bivariat $ vs $ untuk memprediksi penyerapan usus dan penetrasi sawar darah otak secara simultan.
* **Dua Kompartemen Utama:**
  * 🥚 **Zona Putih (HIA):** Absorpsi gastrointestinal usus tinggi (>80% bioavailabilitas oral).
  * 🟡 **Zona Kuning / Yolk (BBB):** Kemampuan menembus Sawar Darah Otak untuk obat sistem saraf pusat.
* **Status P-gp Efflux Transporter:**  
  Titik Biru (Substrat PGP+) vs Titik Merah (Non-substrat).

---

# 🧪 7. Kemudahan Sintesis (SA Score) & Lead-Likeness

* **Synthetic Accessibility (SA Score 1.0 - 10.0):**  
  Diadaptasi dari benchmark *Ertl & Schuffenhauer*:
  * **Skor 1.0 - 3.5:** Sintesis Sangat Mudah (Bahan baku luas, rute 1-3 tahap).
  * **Skor 3.6 - 6.0:** Sintesis Moderat (Rute organik multistep standar industri).
  * **Skor > 6.0:** Sintesis Sangat Kompleks (Pusat kiral banyak/makrosiklik).
* **Saringan Senyawa Penuntun (Lead-Likeness Teague & Oprea):**  
   \in [150, 350]	ext{ g/mol}$, $	ext{LogP} \in [-3.5, 3.5]$, $	ext{RotB} \le 7$ (Ideal untuk molekul awal optimasi).

---

# 🌿 8. Penapisan Analog Cerdas (Tanimoto Similarity $\ge 85\%$)

* **PubChem FastSimilarity 2D Live:**  
  Menyaring molekul analog struktural berbasis koefisien Tanimoto 2D Fingerprint ($\ge 85\%$) dari database 110+ juta molekul NIH.
* **Penyelamatan Kandidat Obat (Lead Rescue):**  
  Jika molekul utama melanggar aturan Lipinski atau toksik, daftar analog menyediakan alternatif turunan kimia yang lebih aman dan poten.
* **Aksi 1-Klik Muat Senyawa:**  
  Klik tombol *"Analisis Senyawa Ini"* untuk langsung mengevaluasi profil analog tanpa mengetik ulang.

---

# 🧬 9. Target Biologis, Jalur Sinyal & Drug Repurposing

* **Pemetaan Target Makromolekul Primer:**  
  HMG-CoA Reductase, COX-1/2, Penicillin-Binding Proteins, Bacterial DNA Gyrase, Adenosine Receptors.
* **Integrasi Jalur Sinyal Biologis:**  
  Pemetaan KEGG Pathway (hsa00900, hsa00590), Reactome Pathway, dan klasifikasi WHO ATC Code.
* **Hipotesis Drug Repurposing In Silico:**  
  Eksplorasi indikasi terapeutik baru untuk obat yang sudah beredar (misal: efek pleiotropik statin pada inflamasi endotel & onkologi).

---

# 📊 10. Penapisan Massal CSV, Komparasi & Dokumen Cetak

* **Saringan Massal Batch CSV:**  
  Unggah daftar ratusan CID PubChem, lakukan audit Lipinski otomatis, dan unduh hasil penapisan kembali ke file CSV.
* **Mode Komparasi Multi-Obat:**  
  Matriks perbandingan berdampingan (*side-by-side*) hingga 3 senyawa obat secara simultan.
* **Dokumen Dossier Ilmiah (Print Ready):**  
  Format cetak resmi @media print yang mengubah tema web menjadi dokumen laporan riset laboratorium berstandar publikasi ilmiah.

---

# 🏆 11. Kesimpulan & Nilai Inovasi Akademis

* **Pencapaian Inovasi:**  
  Sukses mengintegrasikan 7 pilar CADD modern dalam satu platform web interaktif berbasis PubChem PUG-REST Live API.
* **Dampak Akademis & Pedagogis:**  
  Mendemokratisasi akses alat komputasi kimia medisinal canggih bagi mahasiswa dan dosen tanpa biaya lisensi software komersial.
* **Kesiapan Implementasi:**  
  Sangat siap dan berbobot tinggi untuk diajukan sebagai Proposal Inovasi Kompetisi Ilmiah, PKM-KC/RE, Tugas Akhir, maupun Skripsi.

---

# 🙏 Terima Kasih

Akses Langsung Aplikasi & Slide Interaktif:
* **Aplikasi Utama:** http://localhost:3000
* **Slide Presentasi:** http://localhost:3000/Presentasi_PharmaPulse_3D.html
* **File PowerPoint:** Presentasi_PharmaPulse_3D.pptx
* **Repositori:** https://github.com/novarani1511/pharmapulse-3d
