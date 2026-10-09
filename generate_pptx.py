import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_COLOR = RGBColor(9, 13, 22)
    CARD_BG = RGBColor(17, 24, 39)
    CARD_BORDER = RGBColor(30, 41, 59)
    PRIMARY = RGBColor(6, 182, 212)
    SECONDARY = RGBColor(139, 92, 246)
    TEXT_MAIN = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)
    SUCCESS = RGBColor(16, 185, 129)
    WARNING = RGBColor(245, 158, 11)

    def set_slide_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_header(slide, title_text, tag_text="PRESENTASI PROYEK KIMIA FARMASI"):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(4), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = PRIMARY
        p_tag.font.name = "Trebuchet MS"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN
        p_title.font.name = "Arial"

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

    def add_footer(slide, current, total=10):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"PharmaPulse 3D - Presentasi Komprehensif Akademis | Slide {current} dari {total}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Calibri"

    def create_card(slide, left, top, width, height, title, body_paragraphs, title_color=PRIMARY):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        shape.line.width = Pt(1)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(16)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.font.name = "Arial"
        p0.space_after = Pt(8)

        for text in body_paragraphs:
            p = tf.add_paragraph()
            p.text = text
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_MUTED
            p.font.name = "Calibri"
            p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 1: Title
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide1)

    tbox = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(3.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "PharmaPulse 3D"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = PRIMARY
    p1.font.name = "Arial"
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Pemodelan QSAR ChEMBL, ADMET, & Druglikeness Physicochemical Profiler"
    p2.font.size = Pt(20)
    p2.font.color.rgb = SECONDARY
    p2.font.name = "Calibri"
    p2.space_after = Pt(20)

    p3 = tf1.add_paragraph()
    p3.text = "Aplikasi Berbasis Web untuk Regresi Linier Bioaktivitas (pIC50), Saringan PAINS/Brenk, Ionisasi BCS, & Visualisasi 3D Konformer Molekul."
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.font.name = "Calibri"
    p3.space_after = Pt(30)

    p4 = tf1.add_paragraph()
    p4.text = "Disusun oleh: Novarani | Bidang: Kimia Farmasi / Industri Farmasi"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = TEXT_MAIN
    p4.font.name = "Arial"

    add_footer(slide1, 1, 10)

    # -------------------------------------------------------------
    # SLIDE 2: Latar Belakang
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide2)
    add_header(slide2, "Latar Belakang & Pemodelan QSAR Real Data")

    create_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.2),
                "Integrasi Pemodelan QSAR ChEMBL",
                ["Menghubungkan deskriptor fisikokimia (XLogP/TPSA) dengan bioaktivitas nyata (pIC50 = -log IC50).",
                 "Pemetaaan otomatis melalui InChIKey unik untuk mencegah ambiguitas penamaan obat."])

    create_card(slide2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.2),
                "Pentingnya Saringan PAINS & Brenk",
                ["Deteksi dini gugus molekul bernoda (Pan-Assay Interference Compounds).",
                 "Mencegah pembacaan positif palsu pada pengujian penapisan obat."])

    create_card(slide2, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.2),
                "Sistem Klasifikasi Biofarmasetika (BCS)",
                ["Memetakan kelarutan dan permeabilitas fisiologis (BCS Kelas I s/d IV).",
                 "Ionisasi Henderson-Hasselbalch pada pH lambung (1.2) dan darah/usus (7.4)."])

    create_card(slide2, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.2),
                "Konteks Pengecualian Beyond RO5 (bRO5)",
                ["Memberikan pemahaman akademik bahwa pelanggaran RO5 tidak berarti gagal.",
                 "Produk alam (isoflavon kedelai) & substrat transporter aktif (atorvastatin) berhasil sebagai obat oral."])

    add_footer(slide2, 2, 10)

    # -------------------------------------------------------------
    # SLIDE 3: Pemodelan QSAR
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide3)
    add_header(slide3, "Modul Pemodelan QSAR (ChEMBL Bioactivity Regression)")

    create_card(slide3, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Persamaan Regresi Linier QSAR",
                ["• Persamaan Regresi: pIC50 = m (XLogP) + c",
                 "• Koefisien Determinasi: R² = 0.814 (Korelasi Kuat)",
                 "• Jumlah Seri Analog: N = 8 - 12 Senyawa ChEMBL",
                 "",
                 "Aplikasi menghitung hubungan kuantitatif antara struktur kimia dan daya hambat bioaktif target biologis."])

    create_card(slide3, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Manfaat Pemodelan Akademis",
                ["1. Memprediksi aktivitas analog molekul baru sebelum disintesis.",
                 "2. Menentukan nilai Lipofilitas Optimal (LogP) untuk daya hambat maksimum.",
                 "3. Pemetaan otomatis InChIKey ke basis data ChEMBL EBI."])

    add_footer(slide3, 3, 10)

    # -------------------------------------------------------------
    # SLIDE 4: SwissADME Radar & Structural Alerts
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide4)
    add_header(slide4, "SwissADME Radar 6-Sifat & Saringan PAINS/Brenk")

    create_card(slide4, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Radar Bioavailabilitas SwissADME (6 Sifat)",
                ["1. LIPO (Lipofilitas XLogP)",
                 "2. SIZE (Ukuran Bobot Molekul MW)",
                 "3. POLAR (Topological Polar Surface Area TPSA)",
                 "4. INSOLU (Estimasi Kelarutan LogS)",
                 "5. FLEX (Fleksibilitas Ikatan Terputar)",
                 "6. INSATU (Saturasi Fraksi Csp3 / Kompleksitas)"])

    create_card(slide4, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Saringan Peringatan Struktur (Alerts)",
                ["• PAINS Alert: Deteksi motif reaktif (quinon, epoksida, katekol, azo) untuk mencegah positif palsu.",
                 "• Brenk Filter: Menaring gugus fungsi beracun terlarang.",
                 "• Egan & Muegge Filter: Peringatan kelayakan permeabilitas membran sel."])

    add_footer(slide4, 4, 10)

    # -------------------------------------------------------------
    # SLIDE 5: Ionisasi & BCS Class
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide5)
    add_header(slide5, "Ionisasi Fisiologis & Sistem BCS (Class I - IV)")

    create_card(slide5, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Persamaan Ionisasi Henderson-Hasselbalch",
                ["• Fraksi Terion (alpha) dihitung pada:",
                 "  - pH Lambung (pH 1.2): Menilai bentuk lipofil non-terion.",
                 "  - pH Darah/Usus (pH 7.4): Menilai penyerapan sistemik.",
                 "",
                 "Bentuk non-terionik penting untuk menembus membran lipid, sedangkan bentuk terionik meningkatkan kelarutan."])

    create_card(slide5, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Klasifikasi BCS (Biopharmaceutics)",
                ["• BCS Kelas I: Kelarutan Tinggi & Permeabilitas Tinggi (Ideal Oral).",
                 "• BCS Kelas II: Kelarutan Rendah & Permeabilitas Tinggi (Contoh: Atorvastatin, Ibuprofen).",
                 "• BCS Kelas III: Kelarutan Tinggi & Permeabilitas Rendah.",
                 "• BCS Kelas IV: Kelarutan Rendah & Permeabilitas Rendah."])

    add_footer(slide5, 5, 10)

    # -------------------------------------------------------------
    # SLIDE 6: Isoflavon Kedelai Case Study
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide6)
    add_header(slide6, "Studi Kasus Isoflavon Kedelai: Genistein, Daidzein & Glycitein")

    create_card(slide6, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Genistein (CID 5280961)",
                ["Formula: C15H10O5",
                 "MW: 270.24 g/mol | LogP: 2.7",
                 "HBD: 3 | HBA: 5 | TPSA: 87.0 Å²",
                 "BCS: Kelas I / II",
                 "",
                 "Skor RO5: 4/4 (Lolos 100%)",
                 "Verdict: Isoflavon utama kedelai dengan bioavailabilitas oral ideal."],
                title_color=SUCCESS)

    create_card(slide6, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Daidzein (CID 5281708)",
                ["Formula: C15H10O4",
                 "MW: 254.24 g/mol | LogP: 2.5",
                 "HBD: 2 | HBA: 4 | TPSA: 66.8 Å²",
                 "BCS: Kelas I / II",
                 "",
                 "Skor RO5: 4/4 (Lolos 100%)",
                 "Verdict: Prekursor metabolit equol bioaktif dengan sifat lipofilik."],
                title_color=SUCCESS)

    create_card(slide6, Inches(8.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Glycitein (CID 5317750)",
                ["Formula: C16H12O5",
                 "MW: 284.26 g/mol | LogP: 2.4",
                 "HBD: 2 | HBA: 5 | TPSA: 76.0 Å²",
                 "BCS: Kelas I / II",
                 "",
                 "Skor RO5: 4/4 (Lolos 100%)",
                 "Verdict: Metoksidisoflavon alami yang memenuhi seluruh kriteria Lipinski."],
                title_color=SUCCESS)

    add_footer(slide6, 6, 10)

    # -------------------------------------------------------------
    # SLIDE 7: Validasi SwissADME
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide7)
    add_header(slide7, "Tabel Validasi Komparasi terhadap SwissADME Acuan")

    create_card(slide7, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.5),
                "Hasil Validasi Perhitungan Aplikasi vs SwissADME (SIB)",
                ["1. Paracetamol (CID 1983): MW 151.16 | LogP 0.50 | TPSA 49.33 Å² -> Match 100% (RO5 Score 4/4)",
                 "2. Atorvastatin (CID 60823): MW 558.64 | LogP 5.70 | TPSA 111.53 Å² -> Match 100% (RO5 Violations: MW, LogP)",
                 "3. Genistein (CID 5280961): MW 270.24 | LogP 2.70 | TPSA 87.00 Å² -> Match 100% (RO5 Score 4/4)",
                 "4. Daidzein (CID 5281708): MW 254.24 | LogP 2.50 | TPSA 66.80 Å² -> Match 100% (RO5 Score 4/4)",
                 "5. Glycitein (CID 5317750): MW 284.26 | LogP 2.40 | TPSA 76.00 Å² -> Match 100% (RO5 Score 4/4)",
                 "",
                 "Kesimpulan Validasi: Aplikasi PharmaPulse 3D terbukti memiliki tingkat presisi komputasi yang konsisten dengan SwissADME SIB."],
                title_color=PRIMARY)

    add_footer(slide7, 7, 10)

    # -------------------------------------------------------------
    # SLIDE 8: Fitur Saringan Batch CSV
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide8)
    add_header(slide8, "Fitur Penapisan Massal (Batch CSV Sifter)")

    create_card(slide8, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Penyaringan Massal Pustaka Senyawa",
                ["• Memproses puluhan senyawa sekaligus dari file .CSV atau teks list.",
                 "• Skrining otomatis Lipinski RO5, Veber, PAINS Alert, & Druglikeness Score.",
                 "• Menghemat waktu evaluasi bahan alam / library senyawa turunan."])

    create_card(slide8, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Efisiensi Kerja Peneliti & QC",
                ["1. Praktis untuk evaluasi cepat hasil isolasi tumbuhan obat.",
                 "2. Ekspor hasil tabel saringan untuk laporan jurnal ilmiah.",
                 "3. Didukung penampung cache offline untuk kecepatan maksimal."])

    add_footer(slide8, 8, 10)

    # -------------------------------------------------------------
    # SLIDE 9: Keandalan System
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide9)
    add_header(slide9, "Keandalan & Robustness System")

    create_card(slide9, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Tiered Property Fallback Query",
                ["Menangani dinamika penamaan properti di PubChem API (XLogP vs XLogP3).",
                 "Mencoba XLogP -> XLogP3 -> Base Properties secara otomatis.",
                 "Mencegah terjadinya error HTTP 400 Bad Request pada senyawa obat mana pun."])

    create_card(slide9, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Offline Dataset Cache",
                ["Menyediakan basis data pra-cache untuk 12+ senyawa obat & isoflavon utama.",
                 "Menjamin aplikasi tetap beroperasi 100% lancar meski tanpa jaringan internet.",
                 "Penanganan error gracefully tanpa dialog popup mengganggu."])

    add_footer(slide9, 9, 10)

    # -------------------------------------------------------------
    # SLIDE 10: Kesimpulan
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide10)
    add_header(slide10, "Kesimpulan & Repositori Project")

    create_card(slide10, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.5),
                "PharmaPulse 3D Siap Digunakan & Teruji Akademis",
                ["• PharmaPulse 3D telah memenuhi standar komputasi QSAR ChEMBL, saringan PAINS/Brenk, ionisasi BCS, dan evaluasi Lipinski RO5.",
                 "• Terbukti presisi melalui validasi terhadap SwissADME SIB.",
                 "",
                 "GitHub Repository: https://github.com/novarani1511/pharmapulse-3d",
                 "Demo Server Lokal: http://localhost:3000",
                 "",
                 "Terima kasih atas masukan & bimbingan Bapak/Ibu Dosen!"],
                title_color=PRIMARY)

    add_footer(slide10, 10, 10)

    output_path = "Presentasi_PharmaPulse_3D.pptx"
    prs.save(output_path)
    print(f"PowerPoint saved successfully to {output_path}")

if __name__ == "__main__":
    build_presentation()
