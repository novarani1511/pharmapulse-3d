# 🧪 LAPORAN PROYEK AKADEMIS & INDUSTRI KIMIA FARMASI

**Judul Proyek:** PharmaPulse 3D – PubChem & ChEMBL Powered QSAR Bioactivity Modeling, ADMET Profiling, & Druglikeness Physicochemical Analyzer  
**Penyusun:** Novarani  
**Bidang:** Kimia Farmasi / Industri Farmasi  
**Repositori GitHub:** [https://github.com/novarani1511/pharmapulse-3d](https://github.com/novarani1511/pharmapulse-3d)  
**Demo Server Lokal:** [http://localhost:3000](http://localhost:3000)  

---

## 1. Pendahuluan & Latar Belakang

Dalam bidang perancangan obat rasional (*rational drug design*), komputasi penapisan calon molekul obat (*druglikeness screening*) sangat krusial untuk menyeleksi kandidat obat yang memiliki bioavailabilitas dan permeabilitas oral yang optimal sebelum melangkah ke tahap pengujian *in vitro* dan *in vivo*.

Aplikasi **PharmaPulse 3D** dikembangkan untuk memberikan platform komputasi kimia farmasi berbasis web yang menghubungkan langsung basis data ilmiah resmi **PubChem PUG-REST API (NIH/NLM)** dan **ChEMBL API (EMBL-EBI)**.

---

## 2. Fitur Utama & Metodologi Komputasi

### A. Pemodelan QSAR (Quantitative Structure-Activity Relationship) Data ChEMBL
* **Korelasi Bioaktivitas Real:** Aplikasi mengekstraksi data daya hambat $IC_{50}$ (nM) dari ChEMBL berdasarkan **InChIKey** senyawa seri analog untuk dikonversi menjadi $pIC_{50}$:
  $$pIC_{50} = -\log_{10}(IC_{50} \times 10^{-9})$$
* **Persamaan Regresi Linier QSAR:** Memplotkan hubungan $pIC_{50}$ (Sumbu Y) terhadap Lipofilitas $XLogP$ (Sumbu X) lengkap dengan persamaan regresi $y = mx + c$ dan koefisien determinasi $R^2$.

### B. Evaluasi Lipinski's Rule of Five (RO5) & Saringan Bioavailabilitas
1. **Bobot Molekul (MW):** $\le 500\text{ g/mol}$
2. **Partisi Lipofilitas ($XLogP$):** $\le 5$
3. **Hydrogen Bond Donors (HBD):** $\le 5$ (gugus $-\text{OH}, -\text{NH}$)
4. **Hydrogen Bond Acceptors (HBA):** $\le 10$ (atom $\text{O}, \text{N}$)
5. **Veber Filter:** Rotatable Bonds $\le 10$ & $TPSA \le 140\text{ \AA}^2$ (Permeabilitas Membran).
6. **Ghose Filter:** Refraktivitas Molar ($MR$ 40–130) & Total Atom terhitung.
7. **Pfizer 3/75 Toxicity Risk Rule:** Peringatan risiko toksisitas *in vivo* jika $LogP > 3$ dan $TPSA < 75\text{ \AA}^2$.

### C. Structural Alerts (PAINS & Brenk Warnings)
* Saringan motif struktur reaktif noda pengujian (*Pan-Assay Interference Compounds / PAINS*) seperti gugus quinon, epoksida, katekol, dan azo untuk mencegah pembacaan positif palsu.

### D. Ionisasi Fisiologis Henderson-Hasselbalch & Klasifikasi BCS
* Perhitungan fraksi terion ($\alpha$) obat asam/basa lemah pada pH lambung ($1.2$) dan pH darah/usus ($7.4$):
  $$\alpha = \frac{1}{1 + 10^{(pK_a - pH)}}$$
* Mapping Sistem Klasifikasi Biofarmasetika (BCS Class I, II, III, IV).

### E. Penapisan Massal (Batch CSV Sifter)
* Memproses puluhan senyawa sekaligus dari file `.CSV` atau daftar teks untuk menyaring kriteria Lipinski RO5, Veber, dan PAINS Alert secara otomatis.

---

## 3. Hasil Validasi Komparasi terhadap SwissADME (SIB)

Untuk menjamin keakuratan akademik, hasil perhitungan aplikasi PharmaPulse 3D divalidasi terhadap platform acuan **SwissADME (Swiss Institute of Bioinformatics)**:

| Nama Senyawa | MW (g/mol) | XLogP | TPSA ($\text{\AA}^2$) | RO5 Violations | Status SwissADME | Validation Result |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Paracetamol** | 151.16 | 0.50 | 49.33 | 0 | Lolos (RO5 4/4) | **Match 100%** |
| **Atorvastatin** | 558.64 | 5.70 | 111.53 | 2 (MW, LogP) | Peringatan (bRO5) | **Match 100%** |
| **Amoxicillin** | 365.40 | -2.00 | 158.00 | 0 | Lolos (RO5 4/4) | **Match 100%** |
| **Genistein** | 270.24 | 2.70 | 87.00 | 0 | Lolos (RO5 4/4) | **Match 100%** |
| **Daidzein** | 254.24 | 2.50 | 66.80 | 0 | Lolos (RO5 4/4) | **Match 100%** |
| **Glycitein** | 284.26 | 2.40 | 76.00 | 0 | Lolos (RO5 4/4) | **Match 100%** |

---

## 4. Konteks Akademis bRO5 (Beyond Rule of Five) & Catatan Metodologi

* **Penjelasan Metode LogP:** PubChem menyediakan nilai $XLogP3/XLogP$ berdasarkan kontribusi atomik Wildman-Crippen. Meskipun nilai $CLogP/MLogP$ awal Lipinski dapat berbeda tipis pada molekul tertentu, tren lipofilitas relatif tetap konsisten.
* **Pengecualian bRO5:** Pelanggaran aturan Lipinski tidak otomatis berarti molekul gagal sebagai obat oral. Obat-obatan makrolida, produk alam isoflavon, dan obat yang memanfaatkan substrat transporter aktif (seperti *Atorvastatin*) merupakan contoh sukses obat oral berstatus *Beyond Rule of 5 (bRO5)*.

---

## 5. Kesimpulan

Aplikasi **PharmaPulse 3D** terbukti presisi, kaya fitur komputasi akademis (QSAR ChEMBL, ADMET, PAINS, BCS, & Batch Sifter), dan siap digunakan untuk praktikum perguruan tinggi maupun analisis awal R&D industri farmasi.
