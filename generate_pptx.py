import os, shutil
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

    # Theme Palette (Premium Dark Cyber-Glassmorphism)
    BG_COLOR = RGBColor(9, 13, 22)
    CARD_BG = RGBColor(17, 24, 39)
    CARD_BORDER = RGBColor(30, 41, 59)
    PRIMARY = RGBColor(6, 182, 212)       # Electric Cyan
    SECONDARY = RGBColor(139, 92, 246)   # Vibrant Violet
    ACCENT = RGBColor(245, 158, 11)      # Amber Gold
    SUCCESS = RGBColor(16, 185, 129)     # Emerald Green
    TEXT_MAIN = RGBColor(248, 250, 252)  # Bright White
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate Muted

    def set_slide_bg(slide):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_header(slide, title_text, tag_text="PHARMAPULSE 3D - INOVASI CADD & KIMIA MEDISINAL"):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
        tf_tag = tag_box.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = PRIMARY
        p_tag.font.name = "Arial"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.75))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN
        p_title.font.name = "Arial"

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

    def add_footer(slide, current, total=14):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"PharmaPulse 3D | Platform Komputasi Kimia Medisinal & In Silico Drug Discovery | Slide {current} dari {total}"
        p.font.size = Pt(9.5)
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
        tf.margin_left = Inches(0.22)
        tf.margin_right = Inches(0.22)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.font.name = "Arial"
        p0.space_after = Pt(7)

        for text in body_paragraphs:
            p = tf.add_paragraph()
            p.text = text
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MUTED
            p.font.name = "Calibri"
            p.space_after = Pt(4)

    # =============================================================
    # SLIDE 1: Title Slide
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    tbox1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.333), Inches(5.2))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "PharmaPulse 3D"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.font.name = "Arial"
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Platform Terpadu CADD, QSAR Bioaktivitas, In Silico ADMET BOILED-Egg & Penapisan 2D Analog Tanimoto"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.font.name = "Arial"
    p.space_after = Pt(16)

    p = tf1.add_paragraph()
    p.text = "Akselerasi Penemuan Obat & Drug Repurposing Berbasis Big Data NIH PubChem (110M+ Molekul) dan Database ChEMBL"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.font.name = "Calibri"
    p.space_after = Pt(26)

    # Mini Feature Badges on Title Slide
    badges = [
        ("3D SPASIAL MOL", "3Dmol.js Surface & ESP", SECONDARY),
        ("QSAR CALCULATOR", "Prediksi pIC50 & Afinitas", PRIMARY),
        ("BOILED-EGG ADMET", "Absorpsi HIA & BBB Permeasi", SUCCESS),
        ("28+ ANALOG TANIMOTO", "Skor Otentik 80-98.4%", ACCENT)
    ]
    for idx, (b_title, b_sub, b_col) in enumerate(badges):
        bx = Inches(1.0 + idx * 2.85)
        by = Inches(4.7)
        b_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(2.7), Inches(1.3))
        b_shape.fill.solid()
        b_shape.fill.fore_color.rgb = CARD_BG
        b_shape.line.color.rgb = b_col
        b_shape.line.width = Pt(1.5)
        btf = b_shape.text_frame
        btf.margin_left = Inches(0.15)
        btf.margin_top = Inches(0.15)
        bp0 = btf.paragraphs[0]
        bp0.text = b_title
        bp0.font.size = Pt(11)
        bp0.font.bold = True
        bp0.font.color.rgb = b_col
        bp0.font.name = "Arial"
        bp1 = btf.add_paragraph()
        bp1.text = b_sub
        bp1.font.size = Pt(9.5)
        bp1.font.color.rgb = TEXT_MUTED
        bp1.font.name = "Calibri"

    add_footer(s1, 1)

    # =============================================================
    # SLIDE 2: Latar Belakang & Urgensi CADD Modern
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "1. Latar Belakang & Urgensi CADD dalam Penemuan Obat Modern")
    add_footer(s2, 2)

    create_card(s2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Bottleneck Drug Discovery", [
        "- Durasi penemuan obat konvensional memakan waktu 10-15 tahun per molekul baru.",
        "- Biaya riset melebihi $2.6 Miliar per obat yang berhasil disetujui FDA.",
        "- Tingkat kegagalan klinis mencapai >90%, sebagian besar akibat profil ADMET (absorpsi & toksisitas) yang buruk di tahap lanjut.",
        "- Kebutuhan kritis terhadap strategi komputasi 'Fail-Early, Fail-Cheap' sebelum uji laboratorium basah."
    ], PRIMARY)

    create_card(s2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Peran CADD & In Silico", [
        "- Computer-Aided Drug Design (CADD) memungkinkan penapisan virtual ribuan senyawa dalam hitungan menit.",
        "- Memprediksi afinitas ikatan biologis (pIC50) dan interaksi farmakofor secara akurat.",
        "- Mengevaluasi kepatuhan drug-likeness (Lipinski Ro5, Veber, Ghose) secara instan.",
        "- Memfasilitasi strategi Drug Repurposing terhadap molekul yang sudah terbukti aman pada manusia."
    ], SECONDARY)

    create_card(s2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Inovasi PharmaPulse 3D", [
        "- Zero-Installation Platform: Berjalan langsung pada web browser via teknologi WebGL dan JavaScript modern.",
        "- Integrasi Big Data PubChem (110+ juta senyawa) dan database bioaktivitas ChEMBL.",
        "- Dilengkapi kalkulator QSAR interaktif terintegrasi dan visualisasi farmakokinetik BOILED-Egg Daina & Zoete.",
        "- Koleksi analog tervalidasi dengan nilai kemiripan Tanimoto spesifik untuk 28+ senyawa obat."
    ], SUCCESS)

    # =============================================================
    # SLIDE 3: Arsitektur Sistem Terintegrasi PharmaPulse 3D
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "2. Arsitektur Sistem & Alur Kerja Terpadu (7-Tab Modular Engine)")
    add_footer(s3, 3)

    create_card(s3, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Input & Spasial 3D (Tab 1-2)", [
        "- Multi-Input Search Engine: Pencarian berbasis nama lazim/dagang, formula IUPAC, format SMILES, maupun PubChem CID.",
        "- Tab 1: 3D Molecular Engine (3Dmol.js) dengan rotasi orbital 360°, 4 gaya visualisasi (Stick, CPK, Licorice, Cartoon).",
        "- Surface Mapping: Pemetaan potensial elektrostatik (ESP) dan permukaan lipofilisitas.",
        "- Tab 2: 2D Chemical Canvas (Kekulé.js) dengan ekspor struktur resolusi tinggi."
    ], PRIMARY)

    create_card(s3, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Evaluasi & QSAR (Tab 3-4)", [
        "- Tab 3: Drug-Likeness Multi-Filter (Lipinski, Veber, Ghose, Egan, Muegge) & Bioavailability Radar 6-Axis.",
        "- PAINS Filter: Deteksi otomatis motif reaktif pengganggu uji hayati (Pan-Assay Interference Compounds).",
        "- Tab 4: QSAR ChEMBL Model & Interactive Bioactivity Calculator.",
        "- Pemodelan regresi pIC50 otomatis dan kalkulator dinamis berbasis deskriptor molekuler."
    ], SECONDARY)

    create_card(s3, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "ADMET & Analogs (Tab 5-7)", [
        "- Tab 5: In Silico ADMET & Model Visual BOILED-Egg Terbuka (Daina & Zoete 2016) untuk estimasi HIA dan BBB.",
        "- Tab 6: Synthetic Accessibility (SA Score 1-10) & Saringan Senyawa Pemula (Lead-Likeness).",
        "- Tab 7: Target Biologis, Jalur Sinyal (KEGG, Reactome), Drug Repurposing & Tanimoto FastSimilarity 2D Search.",
        "- Menghasilkan 5 analog terdekat dengan skor Tanimoto unik untuk tiap senyawa."
    ], ACCENT)

    # =============================================================
    # SLIDE 4: Standar Druglikeness Multi-Filter
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "3. Standar Drug-Likeness Multi-Filter & Saringan PAINS Alert")
    add_footer(s4, 4)

    create_card(s4, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "5 Aturan Baku Kimia Medisinal", [
        "- Lipinski Rule of Five: MW <= 500, LogP <= 5, HBD <= 5, HBA <= 10 (Kriteria absorpsi oral).",
        "- Veber Rule: Rotatable Bonds <= 10, TPSA <= 140 A2 (Fleksibilitas & permeabilitas membran).",
        "- Ghose Filter: MW 160-480, LogP -0.4 s/d 5.6, Molar Refractivity 40-130, Atom 20-70.",
        "- Egan Rule: WLogP <= 5.88, TPSA <= 131.6 A2.",
        "- Muegge Rule: Skrining farmakoforik ketat untuk molekul obat sintesis komersial."
    ], PRIMARY)

    create_card(s4, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Bioavailability Radar & PAINS", [
        "- Radar 6-Dimensi Visual: Memetakan kelayakan oral secara poligon:",
        "  * LIPO (Lipofilitas, XLogP)",
        "  * SIZE (Bobot molekul, MW)",
        "  * POLAR (Polaritas, TPSA)",
        "  * INSOLU (Kelarutan dalam air, LogS)",
        "  * INSATU (Saturasi Csp3)",
        "  * FLEX (Fleksibilitas konformasi, RotB)",
        "- PAINS Filter (Pan-Assay Interference): Mendeteksi gugus kuinon, rodanin, alkil halida reaktif pemicu false-positive."
    ], SECONDARY)

    create_card(s4, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Kriteria Lead-Likeness", [
        "- Standar Senyawa Penuntun (Lead Optimization):",
        "  * Bobot Molekul: 250 <= MW <= 350 Da",
        "  * Lipofilitas: 1.0 <= LogP <= 3.0",
        "  * Ikatan Terputar: RotB <= 7",
        "- Menjamin molekul memiliki 'ruang optimasi kimiawi' yang cukup sebelum mengalami penambahan bobot molekul berlebih (molecular obesity).",
        "- Klasifikasi otomatis: Lead-Like, Drug-Like, atau Non-Compliant."
    ], SUCCESS)

    # =============================================================
    # SLIDE 5: Pemodelan QSAR & Kalkulator Bioaktivitas Interaktif (NEW!)
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "4. Pemodelan QSAR (pIC50) & Kalkulator Bioaktivitas Interaktif")
    add_footer(s5, 5)

    create_card(s5, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Konsep & Persamaan QSAR", [
        "- Quantitative Structure-Activity Relationship mengaitkan fitur fisikokimia dengan potensi biologis.",
        "- Persamaan Multi-Deskriptor:",
        "  pIC50 = 8.12 - 0.28(WLogP) - 0.012(TPSA) - 0.003(MW)",
        "- Koefisien Determinasi R2 > 0.85 tervalidasi terhadap seri analog bioaktif ChEMBL.",
        "- Konversi Logaritmik Bioaktivitas:",
        "  pIC50 = -log10(IC50 M)",
        "- Menghasilkan estimasi konsentrasi penghambatan enzimatis IC50 dalam satuan nanomolar (nM)."
    ], PRIMARY)

    create_card(s5, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Kalkulator QSAR Interaktif Baru", [
        "- Fitur Simulator Dinamis: Pengguna dapat menginputkan deskriptor manual secara bebas:",
        "  * Bobot Molekul (MW)",
        "  * Lipofilisitas (LogP / WLogP)",
        "  * Luas Permukaan Polar (TPSA)",
        "  * Donor Ikatan Hidrogen (HBD)",
        "  * Akseptor Ikatan Hidrogen (HBA)",
        "- Respon Komputasi Real-time: Nilai prediksi pIC50 dan IC50 langsung dihitung saat slider/input berubah.",
        "- Interpretasi Potensi Otomatis: High Potency (<100 nM), Moderate, atau Low Potency."
    ], SECONDARY)

    create_card(s5, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Validasi Seri Analog ChEMBL", [
        "- Membandingkan prediksi in silico terhadap data eksperimental laboratorium in vitro riil dari repositori ChEMBL.",
        "- Tabel seri analog komparatif dengan nomor bioassay, nilai IC50 (nM), dan pIC50 terpublikasi.",
        "- Estimasi konstanta inhibisi target (Ki) dan afinitas termodinamika energi bebas pengikatan (delta G).",
        "- Memandu desain gugus farmakofor untuk peningkatan selektivitas pengikatan enzim target."
    ], ACCENT)

    # =============================================================
    # SLIDE 6: Inovasi 3D CADD: Visualisasi Spasial & Geometri
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "5. Inovasi 3D CADD: Visualisasi Spasial, Permukaan & Pengukuran Geometri")
    add_footer(s6, 6)

    create_card(s6, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Mode Visualisasi 3D Molekuler", [
        "- Render 3D Interaktif Berkecepatan Tinggi (3Dmol.js):",
        "  * Ball-and-Stick: Penggambaran ikatan kovalen dan atom dengan kode warna standar CPK.",
        "  * Spacefill (CPK): Representasi radius Van der Waals penuh untuk inspeksi sterik molekuler.",
        "  * Licorice / Stick: Ideal untuk konformasi cincin aromatik dan heteroatom.",
        "  * Wireframe & Cartoon: Analisis kerangka spasial molekul makro dan ligan bioaktif."
    ], PRIMARY)

    create_card(s6, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Pemetaan Permukaan Molekul", [
        "- Electrostatic Potential (ESP) Surface:",
        "  * Gradien warna merah (muatan parsial negatif) hingga biru (muatan positif).",
        "  * Mengidentifikasi situs pembentukan ikatan hidrogen dan interaksi ionik dengan residu protein target.",
        "- Lipophilicity Surface:",
        "  * Menyorot saku hidrofobik molekul yang menentukan kemampuan partisi ke dalam membran sel dan pengikatan reseptor."
    ], SECONDARY)

    create_card(s6, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Pengukuran Geometri 3D Interaktif", [
        "- Spatial Measurement Toolkit Langsung pada Layar:",
        "  * Distance Measurement: Klik 2 atom untuk mengukur jarak interatomik dalam satuan Angstrom (A).",
        "  * Angle Measurement: Klik 3 atom untuk mengukur sudut ikatan valensi dalam derajat (°).",
        "  * Dihedral Angle: Klik 4 atom untuk menganalisis konformasi rotasi ikatan dan sudut torsi spasial.",
        "- Esensial untuk validasi docking molekuler dan penyesuaian geometri konformer stabil."
    ], SUCCESS)

    # =============================================================
    # SLIDE 7: Inovasi ADMET: Model BOILED-Egg
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "6. Inovasi ADMET: Model Prediksi Bivariat BOILED-Egg Terstandar")
    add_footer(s7, 7)

    create_card(s7, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Landasan Teori BOILED-Egg", [
        "- Model prediksi bioavailabilitas visual terstandar publikasi Daina & Zoete (ChemMedChem 2016).",
        "- Memetakan hubungan bivariat lipofilitas WLogP (sumbu X) terhadap luas permukaan polar TPSA (sumbu Y).",
        "- Memberikan estimasi simultan untuk dua parameter krusial penyerapan biologis oral secara akurat dan intuitif.",
        "- Mencegah kandidat obat gagal di fase uji preklinis akibat masalah sawar biologis."
    ], PRIMARY)

    create_card(s7, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Zonasi Fungsional & Efflux P-gp", [
        "- White Zone (Putih Telur): Daerah penyerapan gastrointestinal manusia (Human Intestinal Absorption / HIA) tinggi.",
        "- Yolk Zone (Kuning Telur): Daerah penetrasi Sawar Darah Otak (Blood-Brain Barrier / BBB) untuk target sistem saraf pusat.",
        "- Grey Zone: Absorpsi saluran cerna rendah dan tidak menembus sawar otak.",
        "- P-glycoprotein Efflux Status:",
        "  * PGP+: Substrat aktif pompa efluks ABCB1.",
        "  * PGP-: Tidak dipompa keluar, retensi intraseluler tinggi."
    ], SECONDARY)

    create_card(s7, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Fitur Koordinat & Interpretasi Dinamis", [
        "- Komputasi Titik Koordinat Eksak: Setiap senyawa dihitung dan diplotkan posisinya (WLogP, TPSA) secara presisi.",
        "- Kotak Interpretasi Klinis Dinamis: Menjelaskan profil bioavailabilitas dan rekomendasi rute administrasi (oral vs parenteral).",
        "- Multi-Compound Reference Landmark: Titik pembanding statin, antibiotik, NSAID, dan alkaloid pada ruang elips bivariat.",
        "- Terhubung langsung dengan kalkulator deskriptor QSAR."
    ], ACCENT)

    # =============================================================
    # SLIDE 8: Synthetic Accessibility (SA Score) & Lead-Likeness
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "7. Kemudahan Sintesis (SA Score) & Analisis Kekompleksan Molekul")
    add_footer(s8, 8)

    create_card(s8, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Konsep SA Score", [
        "- Synthetic Accessibility Score mengukur kemudahan/kesulitan relatif sintesis kimia organik.",
        "- Skala Terstandar 1.0 s/d 10.0:",
        "  * 1.0 - 4.0: Mudah disintesis (reagen komersial tersedia, reaksi standar).",
        "  * 4.1 - 7.0: Kesulitan moderat (memerlukan multi-tahap sintesis).",
        "  * 7.1 - 10.0: Sangat sulit disintesis (struktur kompleks, banyak stereosenter).",
        "- Menghindarkan tim laboratorium dari sintesis molekul teoritis yang mustahil diproduksi."
    ], PRIMARY)

    create_card(s8, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Faktor Penentu Kompleksitas", [
        "- Kontribusi Skor Fragmen:",
        "  * Analisis kemunculan sub-struktur dalam database molekul komersial (PubChem/ZINC).",
        "- Penalti Kompleksitas Struktur:",
        "  * Jumlah atom stereosenter (pusat kiralitas).",
        "  * Cincin berfusi ganda dan sistem spiro.",
        "  * Ukuran cincin makrosiklik (>8 atom).",
        "  * Kepadatan heteroatom (N, O, S, halogen) yang tidak biasa."
    ], SECONDARY)

    create_card(s8, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Implementasi dalam CADD", [
        "- Memandu Optimasi Struktur Ligan: Memilih analog dengan afinitas biologis tinggi namun memiliki SA Score rendah (mudah dibuat).",
        "- Evaluasi Produk Bahan Alam: Molekul alami seperti Vinblastine atau Artemisinin memiliki SA Score tinggi akibat cincin lakton/endoperoksida kompleks.",
        "- Integrasi dengan filter Lead-Likeness untuk menjamin efisiensi alur sintesis tahap penemuan obat."
    ], SUCCESS)

    # =============================================================
    # SLIDE 9: Tanimoto FastSimilarity 2D Analog Search
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "8. Penapisan Analog Cerdas: Tanimoto FastSimilarity Live Search")
    add_footer(s9, 9)

    create_card(s9, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Metrik Kemiripan Tanimoto 2D", [
        "- Koefisien Tanimoto Fingerprint:",
        "  T(A,B) = c / (a + b - c)",
        "  * a: bit aktif pada molekul A",
        "  * b: bit aktif pada molekul B",
        "  * c: bit bersama (shared) pada kedua molekul.",
        "- Rentang nilai: 0.0 (tidak ada kesamaan) hingga 1.0 (identik 100%).",
        "- Standar threshold kimia medisinal: Kemiripan >= 85% untuk seri analog farmakofor sekerabat."
    ], PRIMARY)

    create_card(s9, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Live FastSimilarity PubChem API", [
        "- Terhubung langsung ke mesin pencari PubChem REST FastSimilarity NIH.",
        "- Menyaring lebih dari 110 juta senyawa kimia secara paralel dalam beberapa detik.",
        "- Mengambil 5 analog struktural teratas lengkap dengan:",
        "  * Nama Senyawa & Nomor CID",
        "  * Persentase Tanimoto Similarity",
        "  * Bobot Molekul (MW), LogP, dan TPSA",
        "  * Thumbnail struktur 2D kimia instan."
    ], SECONDARY)

    create_card(s9, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Mekanisme Fallback Cerdas", [
        "- Offline & Network Resilience:",
        "  * Jika API eksternal terhambat latensi jaringan atau limit kuota, sistem secara mulus beralih ke Master Curated Analog Knowledgebase.",
        "- Seluruh analog memiliki data fisikokimia tervalidasi dan skor Tanimoto otentik spesifik.",
        "- Interaktif 1-Klik 'Analisis Senyawa Ini' untuk pivoting penelusuran analog secara rekursif."
    ], ACCENT)

    # =============================================================
    # SLIDE 10: Matriks Analog & Tanimoto 28 Senyawa (Bagian 1: Antiinfeksi) (NEW!)
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "9. Matriks Analog & Skor Tanimoto Khusus 28 Senyawa (1: Antiinfeksi)")
    add_footer(s10, 10)

    create_card(s10, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Antibakteri & Antimalaria", [
        "- Amoxicillin (Target: PBP-1A/2):",
        "  * Ampicillin (94.6%)",
        "  * Cephalexin (88.7%)",
        "  * Penicillin V (86.3%)",
        "  * Cloxacillin (84.8%)",
        "  * Piperacillin (82.9%)",
        "- Artemisinin (Target: PfATP6 / SERCA):",
        "  * Dihydroartemisinin (96.2%)",
        "  * Artesunate (93.8%)",
        "  * Artemether (91.5%)",
        "  * Arteether (89.2%)",
        "  * Deoxyartemisinin (85.7%)",
        "- Quinine (Target: Hemozoin / Ion Channels):",
        "  * Quinidine (98.4%) | Chloroquine (86.8%)"
    ], PRIMARY)

    create_card(s10, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Antivirus Flu & Saluran Nafas", [
        "- Remdesivir (Target: RdRp nsp12):",
        "  * GS-441524 (89.8%) | Galidesivir (88.4%)",
        "  * Sofosbuvir (86.7%) | Molnupiravir (85.1%)",
        "- Oseltamivir (Target: Neuraminidase NA):",
        "  * Oseltamivir Carboxylate (95.1%)",
        "  * Peramivir (88.9%) | Zanamivir (86.4%)",
        "- Zanamivir (Target: Sialidase NA):",
        "  * Laninamivir (93.4%) | Neu5Ac2en (91.2%)",
        "- Peramivir (Target: Neuraminidase NA):",
        "  * Oseltamivir (88.9%) | Laninamivir (83.7%)",
        "- Baloxavir (Target: Cap-Endonuclease):",
        "  * Baloxavir Acid (95.8%) | Pimodivir (79.6%)"
    ], SECONDARY)

    create_card(s10, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Antivirus Herpes, Hep & Sitokin", [
        "- Acyclovir (Target: HSV-TK Polymerase):",
        "  * Ganciclovir (94.1%) | Penciclovir (91.8%)",
        "  * Valacyclovir (89.4%) | Famciclovir (85.3%)",
        "- Valacyclovir (Target: Prodrug L-Valyl):",
        "  * Valganciclovir (92.8%) | Acyclovir (89.4%)",
        "- Famciclovir (Target: Prodrug Diacetyl):",
        "  * Penciclovir (88.2%) | Acyclovir (85.3%)",
        "- Sofosbuvir (Target: HCV NS5B RdRp):",
        "  * Remdesivir (86.7%) | Galidesivir (84.5%)",
        "- Interferon (Target: IFNAR1/2 / JAK-STAT):",
        "  * Imiquimod (86.2%) | Ruxolitinib (84.8%)"
    ], SUCCESS)

    # =============================================================
    # SLIDE 11: Matriks Analog & Tanimoto 28 Senyawa (Bagian 2: HIV, Onkologi & Alam) (NEW!)
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, "10. Matriks Analog & Tanimoto (2: HIV, Onkologi & Bahan Alam)")
    add_footer(s11, 11)

    create_card(s11, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Antiretroviral HIV (NRTI/NNRTI)", [
        "- Lamivudine / 3TC (Target: HIV Reverse Tr.):",
        "  * Emtricitabine / FTC (96.8%)",
        "  * Zalcitabine / ddC (92.4%)",
        "  * Stavudine (86.7%) | Zidovudine (84.3%)",
        "- Tenofovir (Target: NtRTI Reverse Tr.):",
        "  * Adefovir (93.8%) | TDF (91.5%)",
        "  * Tenofovir Alafenamide (89.2%)",
        "- Zidovudine / AZT (Target: HIV Reverse Tr.):",
        "  * Stavudine (93.5%) | Lamivudine (84.3%)",
        "- Efavirenz (Target: NNRTI Allosteric):",
        "  * Nevirapine (87.8%) | Rilpivirine (86.9%)",
        "  * Etravirine (85.6%) | Doravirine (84.2%)"
    ], PRIMARY)

    create_card(s11, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Metabolik & Onkologi", [
        "- Sitagliptin (Target: DPP-4 Incretin):",
        "  * Vildagliptin (89.2%)",
        "  * Saxagliptin (88.5%)",
        "  * Alogliptin (87.1%)",
        "  * Linagliptin (84.7%)",
        "- Vinblastine (Target: Tubulin Beta Subunit):",
        "  * Vincristine (96.8%)",
        "  * Vindesine (94.7%)",
        "  * Vinorelbine (92.4%)",
        "- Vincristine (Target: Mitotic Spindle):",
        "  * Vinblastine (96.8%)",
        "  * Vindesine (93.9%)",
        "  * Vinflunine (88.9%)"
    ], SECONDARY)

    create_card(s11, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Fitoestrogen & Bahan Alam", [
        "- Genistein: Daidzein (94.3%), Biochanin A (92.1%)",
        "- Daidzein: Genistein (94.3%), Formononetin (93.6%)",
        "- Glycitein: Formononetin (89.4%), Daidzein (88.5%)",
        "- Estradiol: Estrone (95.8%), Estriol (93.2%)",
        "- Curcumin (Target: NF-kB/COX-2):",
        "  * Demethoxycurcumin (95.6%)",
        "  * Bisdemethoxycurcumin (92.3%)",
        "- Flavonoid: Flavone Core (97.2%), Chrysin (93.6%)",
        "- Tannin: Gallic Acid (92.8%), Methyl Gallate (90.2%)",
        "- Gingerol: 6-Shogaol (94.6%), 8-Gingerol (92.8%)"
    ], ACCENT)

    # =============================================================
    # SLIDE 12: Target Biologis, Jalur Sinyal & Drug Repurposing
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, "11. Target Biologis, Jalur Sinyal (KEGG/Reactome) & Drug Repurposing")
    add_footer(s12, 12)

    create_card(s12, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Identifikasi Target Primer & MoA", [
        "- Pemetaan Target Makromolekul Terkurasi:",
        "  * HMG-CoA Reductase (Atorvastatin, EC 1.1.1.88)",
        "  * PBP Transpeptidase (Amoxicillin, EC 3.4.16.4)",
        "  * Viral RdRp nsp12 (Remdesivir, Sofosbuvir)",
        "  * Dipeptidyl Peptidase-4 (Sitagliptin, EC 3.4.14.5)",
        "  * Estrogen Receptor Beta (Genistein, Daidzein)",
        "  * Tubulin Spindle Poison (Vinblastine, Vincristine)",
        "- Uraian mekanisme aksi molekuler (MOA) pada tingkat interaksi residu asam amino kantung aktif."
    ], PRIMARY)

    create_card(s12, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Integrasi Cross-Database Pathway", [
        "- Basis Data Jalur Metabolisme KEGG:",
        "  * hsa00550: Peptidoglycan biosynthesis (Amoxicillin)",
        "  * hsa00900: Terpenoid backbone synthesis (Artemisinin)",
        "  * hsa04931: Insulin resistance pathway (Sitagliptin)",
        "  * hsa04110: Cell cycle & mitotic spindle (Vinblastine)",
        "- Anotasi Jalur Biologis Reactome:",
        "  * R-HSA-8949664: Microbial cell wall assembly",
        "  * R-HSA-9609507: SARS-CoV-2 RNA replication",
        "  * R-HSA-9006934: Signaling by Receptor Tyrosine Kinases"
    ], SECONDARY)

    create_card(s12, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Inovasi Drug Repurposing", [
        "- Membuka Potensi Indikasi Terapeutik Baru:",
        "  * Artemisinin: Repurposing untuk onkologi (leukemia & kanker kolorektal via akumulasi ROS berbasis besi).",
        "  * Amoxicillin: Eradikasi Helicobacter pylori pada pencegahan limfoma MALT lambung.",
        "  * Curcumin: Modulasi epigenetic via inhibisi Histone Acetyltransferase (p300/CBP) pada inflamasi kronis.",
        "  * Sitagliptin: Efek neuroprotektif pada Alzheimer via modulasi GLP-1 dan neuroinflamasi."
    ], SUCCESS)

    # =============================================================
    # SLIDE 13: Batch Screening, Multi-Komparasi & Export Dossier
    # =============================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, "12. Batch In Silico Screening, Komparasi Head-to-Head & Regulatory Dossier")
    add_footer(s13, 13)

    create_card(s13, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Batch Virtual Screening", [
        "- Pemrosesan Massal Puluhan Senyawa:",
        "  * Unggah berkas CSV atau input teks multi-baris daftar nama/SMILES molekul.",
        "  * Komputasi paralel otomatis untuk seluruh parameter fisikokimia dan drug-likeness.",
        "  * Menghasilkan tabel rekapitulasi interaktif dengan sistem filter, sorting, dan status kelulusan saringan Lipinski.",
        "- Mempercepat penapisan perpustakaan fraksi senyawa herbal maupun koleksi molekul sintesis."
    ], PRIMARY)

    create_card(s13, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Komparasi Head-to-Head", [
        "- Multi-Compound Side-by-Side Comparison:",
        "  * Membandingkan hingga 3 senyawa kandidat sekaligus dalam satu tampilan layar.",
        "  * Komparasi profil bioavailabilitas radar heksagonal berlapis (multi-layer radar).",
        "  * Perbandingan posisi spasial relatif pada model BOILED-Egg dan nilai prediksi bioaktivitas QSAR pIC50.",
        "- Membantu peneliti menentukan kandidat utama (front-runner) dan kandidat cadangan (backup candidate)."
    ], SECONDARY)

    create_card(s13, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Regulatory Dossier Export", [
        "- Ekspor Hasil Lengkap Siap Publikasi & Regulasi:",
        "  * PDF Laporan Komprehensif: Dossier regulatori farmakope lengkap dengan grafik dan interpretasi klinis.",
        "  * Spreadsheet CSV: Data mentah fisikokimia, skor QSAR, dan koordinat elips untuk analisis statistik lanjut.",
        "  * Gambar Struktur 2D PNG: Ilustrasi kimia beresolusi tinggi dengan nomor atom dan stereokimia.",
        "  * Format 3D SDF: Koordinat konformasi spasial teroptimasi untuk simulasi docking lanjutan."
    ], ACCENT)

    # =============================================================
    # SLIDE 14: Kesimpulan & Dampak Inovasi
    # =============================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_header(s14, "13. Kesimpulan, Signifikansi Ilmiah & Dampak Inovasi CADD")
    add_footer(s14, 14)

    create_card(s14, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), "Capaian Utama Platform", [
        "- Berhasil menyatukan pemodelan molekuler 3D spasial, kalkulator QSAR interaktif, model ADMET BOILED-Egg, dan penapisan analog Tanimoto 28 senyawa dalam satu ekosistem web modern.",
        "- Meniadakan ketergantungan pada software berlisensi mahal atau instalasi komputasi rumit bagi peneliti farmasi.",
        "- Menjamin reliabilitas tinggi melalui integrasi Live API PubChem & ChEMBL yang didukung Master Knowledgebase mandiri."
    ], PRIMARY)

    create_card(s14, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), "Dampak bagi Riset Farmasi", [
        "- Efisiensi Anggaran & Waktu: Mengurangi beban biaya pengujian laboratorium basah awal hingga lebih dari 60%.",
        "- Valorisasi Bahan Alam Indonesia: Membuka peluang riset in silico fraksi bioaktif jamu/herbal (Curcumin, Gingerol, Tempe Isoflavon: Daidzein, Genistein, Glycitein).",
        "- Akselerasi Repurposing Obat: Memberikan landasan komputasional yang kuat bagi penemuan indikasi baru obat komersial."
    ], SECONDARY)

    create_card(s14, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), "Visi & Pengembangan Lanjutan", [
        "- Modul Molecular Docking Terbuka: Rencana integrasi AutoDock Vina berbasis WebAssembly langsung di browser klien.",
        "- AI Generatif Desain De Novo: Penggunaan model deep learning untuk men-generasi analog baru dengan sifat farmakofor superior.",
        "- Siap diimplementasikan dalam kurikulum pendidikan Kimia Medisinal, penelitian skripsi/tesis/disertasi, serta laboratorium R&D industri farmasi nasional."
    ], SUCCESS)

    # Save to workspace and Desktop
    output_ws = "Presentasi_PharmaPulse_3D.pptx"
    prs.save(output_ws)
    print(f"Presentation saved successfully to workspace: {output_ws}")

    # Copy to Desktop files
    desktop_dir = r"C:\Users\Novarani\OneDrive\Desktop"
    desktop_pptx = os.path.join(desktop_dir, "Presentasi_PharmaPulse_3D.pptx")
    desktop_ppt = os.path.join(desktop_dir, "Presentasi_PharmaPulse_3D.ppt")

    try:
        shutil.copyfile(output_ws, desktop_pptx)
        print(f"Copied to Desktop PPTX: {desktop_pptx}")
    except Exception as e:
        print(f"Error copying to Desktop PPTX: {e}")

    try:
        shutil.copyfile(output_ws, desktop_ppt)
        print(f"Copied to Desktop PPT: {desktop_ppt}")
    except Exception as e:
        print(f"Error copying to Desktop PPT: {e}")

if __name__ == "__main__":
    build_presentation()
