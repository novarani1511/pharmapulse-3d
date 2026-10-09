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
        # Header bar tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(4), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = PRIMARY
        p_tag.font.name = "Trebuchet MS"

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN
        p_title.font.name = "Arial"

        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

    def add_footer(slide, current, total=8):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"PharmaPulse 3D - Presentasi Akademis | Slide {current} dari {total}"
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
    # SLIDE 1: Title Slide
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
    p2.text = "PubChem Powered Drug Discovery & QSAR Physicochemical Analyzer"
    p2.font.size = Pt(20)
    p2.font.color.rgb = SECONDARY
    p2.font.name = "Calibri"
    p2.space_after = Pt(20)

    p3 = tf1.add_paragraph()
    p3.text = "Aplikasi Berbasis Web untuk Penapisan Kelayakan Obat (Druglikeness), Evaluasi Lipinski RO5, & Visualisasi 3D Konformer Molekul secara Real-Time."
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

    add_footer(slide1, 1)

    # -------------------------------------------------------------
    # SLIDE 2: Latar Belakang
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide2)
    add_header(slide2, "Latar Belakang & Urgensi Penelitian")

    create_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.2),
                "Tantangan Desain Obat Klasik",
                ["Proses penemuan obat membutuhkan biaya tinggi dan waktu bertahun-tahun.",
                 "Banyak calon molekul obat gagal pada uji klinis akibat sifat permeabilitas dan absorpsi oral yang buruk."])

    create_card(slide2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.2),
                "Peran Aturan Lipinski (RO5)",
                ["Christopher A. Lipinski merumuskan Aturan Empat Parameter (Lipinski's Rule of Five).",
                 "Digunakan untuk memprediksi secara cepat permeabilitas membran sel dan bioavailabilitas oral molekul."])

    create_card(slide2, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.2),
                "Kebutuhan Akses Data Real-Time",
                ["Laboratorium akademis & R&D industri membutuhkan alat bantu komputasi cepat.",
                 "Terhubung langsung dengan basis data molekul ilmiah tanpa perlu menginput parameter manual."])

    create_card(slide2, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.2),
                "Pentingnya Spatial 3D Conformer",
                ["Pemahaman spasial 3D molekul (panjang ikatan, gugus fungsi, dan kepolaran ruang).",
                 "Sangat vital dalam memprediksi interaksi molekul obat dengan reseptor biologis target."])

    add_footer(slide2, 2)

    # -------------------------------------------------------------
    # SLIDE 3: Solusi & Inovasi
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide3)
    add_header(slide3, "Solusi & Inovasi Teknologi PharmaPulse 3D")

    create_card(slide3, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Integrasi PubChem API",
                ["Terhubung langsung dengan PubChem PUG-REST API (NIH/NLM).",
                 "Akses gratis tanpa API Key.",
                 "Menarik 15+ deskriptor sifat fisikokimia secara otomatis dalam hitungan milidetik."])

    create_card(slide3, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "3Dmol.js Engine",
                ["Visualisator konformer 3D molekul interaktif.",
                 "Rotasi otomatis 360°, zoom, dan penyesuaian gaya (Ball & Stick, Spacefill, Wireframe).",
                 "Pewarnaan atom standar CPK."])

    create_card(slide3, Inches(8.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Multi-QSAR Evaluator",
                ["Penilaian otomatis Lipinski RO5.",
                 "Saringan Veber Filter & Ghose Filter.",
                 "Pfizer 3/75 Toxicity Risk Rule.",
                 "Grafik Radar Lipofilitas berbasis Chart.js."])

    add_footer(slide3, 3)

    # -------------------------------------------------------------
    # SLIDE 4: Arsitektur Sistem
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide4)
    add_header(slide4, "Arsitektur Sistem & Alur Kerja Data")

    steps = [
        ("1. Input Pengguna", "Pengguna memasukkan Nama Obat (misal: Paracetamol, Atorvastatin), SMILES, atau CID."),
        ("2. Query PubChem API", "Aplikasi melakukan kueri HTTP REST API untuk mengambil CID, deskriptor fisikokimia, & koordinat 3D SDF."),
        ("3. Komputasi QSAR", "Algoritma mengevaluasi pelanggaran Lipinski (MW <= 500, LogP <= 5, HBD <= 5, HBA <= 10) & saringan pendukung."),
        ("4. Rendering UI", "Menampilkan hasil evaluasi pada dashboard Dark Glassmorphic beserta Grafik Radar & 3D Viewer.")
    ]

    top_pos = 1.9
    for title, desc in steps:
        create_card(slide4, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(1.0),
                    title, [desc], title_color=PRIMARY)
        top_pos += 1.2

    add_footer(slide4, 4)

    # -------------------------------------------------------------
    # SLIDE 5: Parameter Evaluasi
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide5)
    add_header(slide5, "Parameter Evaluasi Lipinski RO5 & QSAR")

    create_card(slide5, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "4 Aturan Lipinski (RO5)",
                ["• Bobot Molekul (MW): <= 500 g/mol",
                 "• Partisi Lipofilitas (XLogP): <= 5",
                 "• H-Bond Donors (HBD): <= 5 (gugus -OH, -NH)",
                 "• H-Bond Acceptors (HBA): <= 10 (atom O, N)",
                 "",
                 "Tujuan: Memprediksi kelayakan absorpsi dan permeabilitas sediaan obat oral."])

    create_card(slide5, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Saringan Tambahan Bioavailabilitas",
                ["• Veber Rule: Rotatable Bonds <= 10 & TPSA <= 140 Å² (Ideal permeabilitas membran sel)",
                 "• Ghose Filter: MW (160-480), LogP (-0.4 s/d 5.6) untuk kesesuaian basis data obat.",
                 "• Pfizer 3/75 Rule: Deteksi risiko toksisitas in vivo jika LogP > 3 & TPSA < 75 Å²."])

    add_footer(slide5, 5)

    # -------------------------------------------------------------
    # SLIDE 6: Studi Kasus Isoflavon Kedelai (Phytoestrogen)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide6)
    add_header(slide6, "Studi Kasus Isoflavon Kedelai: Genistein, Daidzein & Glycitein")

    create_card(slide6, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Genistein (CID 5280961)",
                ["Formula: C15H10O5",
                 "MW: 270.24 g/mol | LogP: 2.7",
                 "HBD: 3 | HBA: 5",
                 "TPSA: 87.00 Å² | RotB: 1",
                 "",
                 "Skor RO5: 4/4 (Lolos)",
                 "Verdict: Isoflavon kedelai utama dengan kelayakan penyerapan oral 100% ideal."],
                title_color=SUCCESS)

    create_card(slide6, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Daidzein (CID 5281708)",
                ["Formula: C15H10O4",
                 "MW: 254.24 g/mol | LogP: 2.5",
                 "HBD: 2 | HBA: 4",
                 "TPSA: 66.80 Å² | RotB: 1",
                 "",
                 "Skor RO5: 4/4 (Lolos)",
                 "Verdict: Prekursor metabolit equol bioaktif dengan profil lipofilitas tinggi."],
                title_color=SUCCESS)

    create_card(slide6, Inches(8.8), Inches(2.0), Inches(3.6), Inches(4.5),
                "Glycitein (CID 5317750)",
                ["Formula: C16H12O5",
                 "MW: 284.26 g/mol | LogP: 2.4",
                 "HBD: 2 | HBA: 5",
                 "TPSA: 76.00 Å² | RotB: 2",
                 "",
                 "Skor RO5: 4/4 (Lolos)",
                 "Verdict: Metoksidisoflavon alami yang memenuhi seluruh kriteria Lipinski RO5."],
                title_color=SUCCESS)

    add_footer(slide6, 6)

    # -------------------------------------------------------------
    # SLIDE 7: Keandalan Sistem
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide7)
    add_header(slide7, "Keandalan & Robustness System")

    create_card(slide7, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Tiered Property Fallback Query",
                ["Menangani dinamika penamaan properti di PubChem API (XLogP vs XLogP3).",
                 "Mencoba XLogP -> XLogP3 -> Base Properties secara otomatis.",
                 "Mencegah terjadinya error HTTP 400 Bad Request pada senyawa obat mana pun."])

    create_card(slide7, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5),
                "Offline Dataset Cache",
                ["Menyediakan basis data pra-cache untuk 9+ senyawa obat preset utama.",
                 "Menjamin aplikasi tetap beroperasi 100% lancar meski tanpa jaringan internet.",
                 "Penanganan error gracefully tanpa dialog popup mengganggu."])

    add_footer(slide7, 7)

    # -------------------------------------------------------------
    # SLIDE 8: Kesimpulan
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide8)
    add_header(slide8, "Kesimpulan & Repositori Project")

    create_card(slide8, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.5),
                "PharmaPulse 3D Siap Digunakan",
                ["• PharmaPulse 3D berhasil menggabungkan integrasi data molekul ilmiah PubChem real-time, visualisasi spatial 3D, dan komputasi evaluasi kelayakan obat (QSAR).",
                 "• Sangat bermanfaat untuk kegiatan praktikum akademis kimia farmasi maupun analisis awal R&D / QC industri farmasi.",
                 "",
                 "GitHub Repository: https://github.com/novarani1511/pharmapulse-3d",
                 "Demo Server Lokal: http://localhost:3000",
                 "",
                 "Terima kasih atas perhatian Bapak/Ibu Dosen!"],
                title_color=PRIMARY)

    add_footer(slide8, 8)

    # Save outputs
    output_path_scratch = "Presentasi_PharmaPulse_3D.pptx"
    prs.save(output_path_scratch)
    print(f"PowerPoint saved successfully to {output_path_scratch}")

if __name__ == "__main__":
    build_presentation()
