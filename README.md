# 🧪 PharmaPulse 3D - PubChem Powered Drug Discovery & QSAR Analyzer

**PharmaPulse 3D** adalah aplikasi web interaktif untuk industri dan akademis kimia farmasi. Aplikasi ini terintegrasi secara *live* dengan **PubChem PUG-REST API (NIH/NLM)** untuk menganalisis sifat fisikokimia, *druglikeness* (Lipinski's Rule of Five, Veber, Ghose, Pfizer 3/75), serta visualisasi konformer molekul 3D secara *real-time*.

![PharmaPulse 3D Demo](https://img.shields.io/badge/PubChem-PUG--REST%20Live-06b6d4?style=for-the-badge&logo=atom)
![Lipinski RO5 Evaluator](https://img.shields.io/badge/Lipinski%20RO5-QSAR%20Evaluator-10b981?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## 🌟 Fitur Utama

- 🔍 **Pencarian Live PubChem API:** Cari senyawa obat berdasarkan nama (misal: *Paracetamol, Aspirin, Ibuprofen, Atorvastatin, Amoxicillin, Ciprofloxacin, Artemisinin, Remdesivir*), SMILES, atau CID.
- 🧊 **Visualisator Konformer 3D Molekul Interaktif (3Dmol.js):** Mengunduh file SDF 3D secara live dari PubChem. Mendukung gaya *Ball & Stick*, *Sphere*, *Stick*, *Wireframe*, rotasi otomatis 360°, dan penyesuaian sudut pandang.
- 🛡️ **Evaluasi Lipinski's Rule of Five (RO5) & Saringan QSAR:**
  - **Lipinski RO5:** MW $\le 500$, LogP $\le 5$, HBD $\le 5$, HBA $\le 10$.
  - **Veber Filter:** Rotatable Bonds $\le 10$ & TPSA $\le 140\text{ Å}^2$.
  - **Ghose Filter:** Match kriteria rentang basis data obat.
  - **Pfizer 3/75 Toxicity Risk Rule:** Deteksi risiko toksisitas *in vivo*.
- 📊 **Radar Chart Profil Molekul:** Visualisasi grafik radar memetakan kelayakan lipofilitas & polaritas molekul (Chart.js).
- ⚠️ **Klasifikasi Bahaya GHS & Toksisitas:** Penarikan otomatis data *Laboratory Chemical Safety Summary* (LCSS) dari PubChem.
- ⚖️ **Mode Komparasi Multi-Obat:** Bandingkan hingga 3 senyawa obat secara berdampingan (*side-by-side comparison matrix*).

---

## 🚀 Cara Menjalankan Secara Lokal

1. **Clone repository:**
   ```bash
   git clone https://github.com/USERNAME/REPOSITORY-NAME.git
   cd REPOSITORY-NAME
   ```

2. **Jalankan server lokal (misal menggunakan Python):**
   ```bash
   python -m http.server 3000
   ```
   *atau menggunakan extension Live Server pada VS Code.*

3. Buka browser dan akses **`http://localhost:3000`**.

---

## 🛠️ Teknologi yang Digunakan

- **Frontend:** HTML5, CSS3 (Vanilla Dark Glassmorphism), Vanilla JavaScript (ES6+).
- **External Data Source:** PubChem PUG-REST API (US National Library of Medicine / NIH).
- **3D Molecular Engine:** [3Dmol.js](https://3dmol.org/)
- **Chart Engine:** [Chart.js](https://chartjs.org/)
- **Icons & Fonts:** FontAwesome 6, Google Fonts (Inter, Outfit, Fira Code).

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).
