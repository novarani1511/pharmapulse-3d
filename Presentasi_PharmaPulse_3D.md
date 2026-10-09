---
marp: true
theme: default
paginate: true
header: 'PharmaPulse 3D - Presentasi Proyek Kimia Farmasi'
footer: 'Disusun oleh Novarani | https://github.com/novarani1511/pharmapulse-3d'
---

# 🧪 PharmaPulse 3D
### PubChem Powered Drug Discovery & QSAR Physicochemical Analyzer

Aplikasi Berbasis Web untuk Penapisan Kelayakan Obat (*Druglikeness*), Evaluasi Lipinski RO5, & Visualisasi 3D Konformer Molekul secara Real-Time.

**Disusun oleh:** Novarani  
**Bidang:** Kimia Farmasi / Industri Farmasi  
**Repositori:** [github.com/novarani1511/pharmapulse-3d](https://github.com/novarani1511/pharmapulse-3d)

---

# 🥼 1. Latar Belakang & Urgensi Penelitian

* **Tantangan Desain Obat Klasik:**  
  Proses penemuan obat membutuhkan biaya tinggi dan bertahun-tahun. Banyak calon obat gagal akibat sifat penyerapan (absorpsi) dan permeabilitas oral yang buruk.

* **Peran Aturan Lipinski (Rule of Five):**  
  Pedoman empat parameter fisikokimia untuk memprediksi secara cepat kelayakan penyerapan oral calon molekul obat.

* **Visualisasi Ruang 3D:**  
  Pemahaman spasial konformasi 3D molekul sangat krusial untuk menganalisis interaksi molekul obat dengan protein target biologis.

---

# 💡 2. Solusi & Inovasi Teknologi

* 🔌 **Integrasi PubChem PUG-REST API Live:**  
  Terhubung langsung secara gratis tanpa API Key dengan basis data molekul NIH/NLM untuk mengambil 15+ deskriptor sifat molekul secara otomatis.

* 🧊 **3D Molecular Engine (3Dmol.js):**  
  Menampilkan konformer 3D molekul yang dapat diputar 360°, di-zoom, dan disesuaikan mode visualnya (*Ball & Stick, Spacefill, Wireframe*).

* 📊 **Multi-QSAR & Evaluator Bioavailabilitas:**  
  Evaluasi otomatis Lipinski RO5, Veber Filter, Ghose Filter, Pfizer 3/75 Toxicity Risk, serta Grafik Radar Polaritas (Chart.js).

---

# ⚙️ 3. Arsitektur Sistem & Alur Kerja Data

1. **Input Pengguna:** Memasukkan Nama Obat (misal: *Paracetamol, Atorvastatin*), SMILES, atau PubChem CID.
2. **Query PubChem API:** Pengambilan data CID, deskriptor fisikokimia, dan file koordinat 3D SDF secara asynchronous.
3. **Komputasi QSAR & RO5:** Algoritma menghitung nilai kelayakan Lipinski (MW $\le 500$, LogP $\le 5$, HBD $\le 5$, HBA $\le 10$).
4. **Rendering UI Dashboard:** Menampilkan antarmuka Dark Glassmorphism beserta grafik radar dan viewer 3D.

---

# 🛡️ 4. Parameter Evaluasi Lipinski RO5 & QSAR

### 📌 Lipinski's Rule of Five (RO5)
* **Bobot Molekul (MW):** $\le 500\text{ g/mol}$
* **Partisi Lipofilitas (LogP):** $\le 5$
* **H-Bond Donors (HBD):** $\le 5$ (gugus -OH, -NH)
* **H-Bond Acceptors (HBA):** $\le 10$ (atom O, N)

### 📌 Saringan Tambahan
* **Veber Filter:** RotB $\le 10$ & TPSA $\le 140\text{ Å}^2$ (Permeabilitas Membran)
* **Pfizer 3/75 Rule:** Deteksi risiko toksisitas *in vivo* (LogP > 3 & TPSA < 75 Å²)

---

# 🧪 5. Studi Kasus Isoflavon Kedelai (Phytoestrogen)

* 🟢 **Genistein (CID 5280961):**  
  MW: 270.24 g/mol | LogP: 2.7 | HBD: 3 | HBA: 5 | TPSA: 87.0 Å²  
  **Skor RO5: 4/4 (Lolos 100% Ideal Absorpsi Oral)**

* 🟢 **Daidzein (CID 5281708):**  
  MW: 254.24 g/mol | LogP: 2.5 | HBD: 2 | HBA: 4 | TPSA: 66.8 Å²  
  **Skor RO5: 4/4 (Lolos - Prekursor Metabolit Equol)**

* 🟢 **Glycitein (CID 5317750):**  
  MW: 284.26 g/mol | LogP: 2.4 | HBD: 2 | HBA: 5 | TPSA: 76.0 Å²  
  **Skor RO5: 4/4 (Lolos - Metoksidisoflavon Alami)**

---

# 🛡️ 6. Keandalan System & Robustness

* **Tiered Property Fallback Query:**  
  Menangani dinamika penamaan properti di PubChem API (`XLogP` vs `XLogP3`) secara otomatis tanpa pernah memicu error HTTP 400 Bad Request.

* **Offline Dataset Cache:**  
  Menyediakan basis data pra-cache untuk 9+ senyawa obat preset utama, menjamin aplikasi tetap beroperasi 100% lancar meski tanpa jaringan internet.

---

# 🏁 7. Kesimpulan & Penutup

* **PharmaPulse 3D** berhasil menggabungkan integrasi data molekul ilmiah terpercaya secara live, visualisasi 3D spatial, dan komputasi evaluasi kelayakan obat (QSAR).
* Sangat bermanfaat untuk kegiatan praktikum akademis kimia farmasi maupun analisis awal R&D / QC industri farmasi.

👉 **Repositori GitHub:** [https://github.com/novarani1511/pharmapulse-3d](https://github.com/novarani1511/pharmapulse-3d)  
👉 **Demo Lokal:** `http://localhost:3000`
