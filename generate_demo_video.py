import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw
    HAS_RDKIT = True
except Exception:
    HAS_RDKIT = False


WIDTH, HEIGHT = 1920, 1080
FPS = 15

# Theme Palette matching styles.css (Dark Cyber-Glassmorphism)
BG_DARK = (9, 13, 22)
PANEL_BG = (17, 24, 39)
CARD_BG = (24, 34, 54)
CARD_DARK = (13, 19, 33)
BORDER_COL = (45, 62, 90)
CYAN = (6, 182, 212)
BLUE = (59, 130, 246)
PURPLE = (139, 92, 246)
GREEN = (16, 185, 129)
AMBER = (245, 158, 11)
RED = (239, 68, 68)
WHITE = (248, 250, 252)
MUTED = (148, 163, 184)


def load_font(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates = ["consolab.ttf" if bold else "consola.ttf", "courbd.ttf" if bold else "cour.ttf"]
    else:
        candidates = ["segoeuib.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf"]
    for name in candidates:
        path = os.path.join("C:\\Windows\\Fonts", name)
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


F_H1 = load_font(30, bold=True)
F_H2 = load_font(22, bold=True)
F_H3 = load_font(18, bold=True)
F_BODY = load_font(15, bold=False)
F_BOLD = load_font(15, bold=True)
F_SMALL = load_font(13, bold=False)
F_TINY = load_font(12, bold=False)
F_MONO = load_font(15, bold=True, mono=True)
F_MONO_LG = load_font(22, bold=True, mono=True)
F_SUB = load_font(19, bold=True)


def build_3d_molecule(smiles):
    """Generate 3D coordinates and bonds for a molecule (Atorvastatin fallback if RDKit unavailable)."""
    if HAS_RDKIT:
        try:
            mol = Chem.MolFromSmiles(smiles)
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol, maxIters=100)
            mol = Chem.RemoveHs(mol)
            conf = mol.GetConformer()
            atoms = []
            for a in mol.GetAtoms():
                pos = conf.GetAtomPosition(a.GetIdx())
                atoms.append((a.GetSymbol(), float(pos.x), float(pos.y), float(pos.z)))
            coords = np.array([[x, y, z] for _, x, y, z in atoms])
            center = coords.mean(axis=0)
            scale = np.max(np.linalg.norm(coords - center, axis=1)) or 1.0
            norm_atoms = [(sym, (x - center[0]) / scale, (y - center[1]) / scale, (z - center[2]) / scale)
                          for sym, x, y, z in atoms]
            bonds = [(b.GetBeginAtomIdx(), b.GetEndAtomIdx(), int(b.GetBondTypeAsDouble()))
                     for b in mol.GetBonds()]
            return norm_atoms, bonds
        except Exception:
            pass

    # Fallback procedural 3D ring-chain scaffold
    atoms = []
    bonds = []
    for i in range(26):
        ang = i * 0.65
        r = 0.35 + 0.45 * (i / 26.0)
        sym = "C"
        if i in (3, 11, 19, 24):
            sym = "O"
        elif i in (6, 15):
            sym = "N"
        elif i == 22:
            sym = "F"
        atoms.append((sym, r * math.cos(ang), r * math.sin(ang), 0.35 * math.sin(i * 0.9)))
        if i > 0:
            bonds.append((i - 1, i, 1))
    return atoms, bonds


def render_2d_mol_card(smiles, size=(220, 150)):
    if HAS_RDKIT:
        try:
            mol = Chem.MolFromSmiles(smiles)
            img = Draw.MolToImage(mol, size=size)
            return img.convert("RGB")
        except Exception:
            pass
    img = Image.new("RGB", size, (255, 255, 255))
    d = ImageDraw.Draw(img)
    cx, cy = size[0] // 2, size[1] // 2
    pts = [(cx + 40 * math.cos(k * math.pi / 3), cy + 40 * math.sin(k * math.pi / 3)) for k in range(6)]
    d.polygon(pts, outline=(30, 41, 59), width=3)
    return img


ATORVASTATIN_SMILES = "CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccccc2)c(-c2ccc(F)cc2)n1CCC(O)CC(O)CC(=O)O"
PARACETAMOL_SMILES = "CC(=O)Nc1ccc(O)cc1"
OSELTAMIVIR_SMILES = "CCOC(=O)C1=CC(OC(CC)CC)C(NC(C)=O)C(N)C1"

MOL_ATOR, BONDS_ATOR = build_3d_molecule(ATORVASTATIN_SMILES)
IMG2D_ATOR = render_2d_mol_card(ATORVASTATIN_SMILES, (180, 130))
IMG2D_PARA = render_2d_mol_card(PARACETAMOL_SMILES, (140, 105))
IMG2D_OSEL = render_2d_mol_card(OSELTAMIVIR_SMILES, (140, 105))


def draw_mol_3d(draw, box, atoms, bonds, angle_y, angle_x=0.32, show_pharm=False, show_dist=False, show_pocket=False):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) * 0.5
    cy = (y0 + y1) * 0.5 + 12
    radius_px = min(x1 - x0, y1 - y0) * 0.36

    # Subtle 3D viewport grid & radial glow
    for r_glow, col in [(180, (12, 32, 56)), (120, (15, 42, 72))]:
        draw.ellipse((cx - r_glow, cy - r_glow, cx + r_glow, cy + r_glow), fill=col)

    if show_pocket:
        # Binding pocket mesh wireframe rings (HMG-CoA Reductase 1HWK pocket)
        for k in range(4):
            rx = 165 - k * 22
            ry = 120 - k * 15
            draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(30, 90, 130), width=1)
        draw.text((x0 + 18, y0 + 52), "Target PDB: 1HWK (HMG-CoA Reductase Active Pocket)", fill=CYAN, font=F_SMALL)

    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)

    proj = []
    for sym, x, y, z in atoms:
        rx = x * cos_y + z * sin_y
        rz = -x * sin_y + z * cos_y
        ry = y * cos_x - rz * sin_x
        rz2 = y * sin_x + rz * cos_x
        scale = 1.0 / (2.4 - rz2 * 0.55)
        px = cx + rx * radius_px * 1.85 * scale
        py = cy + ry * radius_px * 1.85 * scale
        proj.append((sym, px, py, rz2, scale))

    # Draw covalent bonds sorted by average depth
    bond_items = []
    for i, j, btype in bonds:
        z_avg = 0.5 * (proj[i][3] + proj[j][3])
        bond_items.append((z_avg, i, j, btype))
    bond_items.sort(key=lambda t: t[0])

    for _, i, j, btype in bond_items:
        _, x_a, y_a, _, _ = proj[i]
        _, x_b, y_b, _, _ = proj[j]
        draw.line((x_a, y_a, x_b, y_b), fill=(148, 163, 184), width=4 if btype == 1 else 6)

    # Atom colors (CPK standard)
    cpk = {
        "C": (56, 189, 248),
        "O": (239, 68, 68),
        "N": (59, 130, 246),
        "F": (16, 185, 129),
        "S": (245, 158, 11),
    }

    atom_indices = list(range(len(proj)))
    atom_indices.sort(key=lambda idx: proj[idx][3])

    for idx in atom_indices:
        sym, px, py, rz2, scale = proj[idx]
        col = cpk.get(sym, (203, 213, 225))
        r = max(6, int(15 * scale))
        draw.ellipse((px - r, py - r, px + r, py + r), fill=col, outline=(15, 23, 42), width=1)
        # Specular highlight dot
        hr = max(2, r // 3)
        draw.ellipse((px - r // 3 - hr, py - r // 3 - hr, px - r // 3 + hr, py - r // 3 + hr), fill=(240, 249, 255))

    if show_pharm and len(proj) >= 12:
        # Highlight HBA (Red), HBD (Blue), and Aromatic Hydrophobic Center (Yellow)
        pharm_features = [
            (proj[2][1], proj[2][2], 26, (239, 68, 68), "HBA (Acceptor)"),
            (proj[5][1], proj[5][2], 24, (59, 130, 246), "HBD (Donor)"),
            (proj[10][1], proj[10][2], 32, (245, 158, 11), "Aromatic Ring"),
        ]
        for px, py, pr, pcol, plabel in pharm_features:
            draw.ellipse((px - pr, py - pr, px + pr, py + pr), outline=pcol, width=3)
            draw.ellipse((px - pr - 4, py - pr - 4, px + pr + 4, py + pr + 4), outline=pcol, width=1)
            draw.text((px + pr + 6, py - 8), plabel, fill=pcol, font=F_TINY)

    if show_dist and len(proj) >= 16:
        _, x_a, y_a, _, _ = proj[3]
        _, x_b, y_b, _, _ = proj[14]
        draw.line((x_a, y_a, x_b, y_b), fill=AMBER, width=3)
        mx, my = (x_a + x_b) * 0.5, (y_a + y_b) * 0.5
        draw.rounded_rectangle((mx - 58, my - 16, mx + 58, my + 16), radius=8, fill=(15, 23, 42), outline=AMBER, width=2)
        draw.text((mx - 48, my - 9), "d = 4.82 Å", fill=AMBER, font=F_MONO)


def draw_base_chrome(img, active_tab_idx, compound_name="Atorvastatin", cid="60823", formula="C33H35FN2O5", mw="558.64 g/mol", logp="5.70", tpsa="111.79 Å²"):
    draw = ImageDraw.Draw(img)

    # Top Header Bar
    draw.rounded_rectangle((24, 16, WIDTH - 24, 92), radius=14, fill=PANEL_BG, outline=BORDER_COL, width=2)
    draw.ellipse((42, 32, 86, 76), fill=(6, 182, 212))
    draw.text((54, 40), "3D", fill=BG_DARK, font=F_H2)
    draw.text((98, 26), "PharmaPulse 3D", fill=WHITE, font=F_H1)
    draw.text((98, 60), "In Silico Drug Discovery, Ensemble Machine Learning QSAR & CADD Suite", fill=CYAN, font=F_SMALL)

    # Search Box in Header
    draw.rounded_rectangle((680, 28, 1280, 80), radius=10, fill=CARD_DARK, outline=CYAN, width=2)
    draw.text((700, 44), f"🔍  {compound_name} (PubChem CID: {cid})", fill=WHITE, font=F_BOLD)
    draw.rounded_rectangle((1145, 35, 1268, 73), radius=8, fill=CYAN)
    draw.text((1164, 44), "Analisis 3D", fill=BG_DARK, font=F_BOLD)

    # Live API Status Pills
    apis = [("PubChem PUG-REST", GREEN), ("ChEMBL pIC50", PURPLE), ("RCSB PDB 3D", BLUE), ("openFDA FAERS", AMBER)]
    px = 1305
    for label, col in apis:
        draw.rounded_rectangle((px, 36, px + 142, 72), radius=16, fill=CARD_DARK, outline=col, width=1)
        draw.ellipse((px + 10, 49, px + 20, 59), fill=col)
        draw.text((px + 26, 45), label, fill=WHITE, font=F_TINY)
        px += 148

    # Quick-Select 34 Compounds Strip
    draw.rounded_rectangle((24, 102, WIDTH - 24, 146), radius=10, fill=PANEL_BG, outline=BORDER_COL, width=1)
    draw.text((40, 115), "34 Senyawa Terkurasi:", fill=CYAN, font=F_BOLD)
    pills = ["Atorvastatin", "Paracetamol", "Aspirin", "Ibuprofen", "Amoxicillin", "Ciprofloxacin", "Oseltamivir", "Remdesivir", "Artemisinin", "Gingerol Jahe", "Genistein", "Curcumin", "Quercetin"]
    qx = 225
    for p in pills:
        is_sel = (p.lower() in compound_name.lower())
        w_pill = len(p) * 8 + 26
        draw.rounded_rectangle((qx, 109, qx + w_pill, 139), radius=14,
                               fill=CYAN if is_sel else CARD_DARK,
                               outline=CYAN if is_sel else BORDER_COL, width=1)
        draw.text((qx + 13, 115), p, fill=BG_DARK if is_sel else MUTED, font=F_TINY)
        qx += w_pill + 8

    # Left Column: 3D Molecular Viewport + 2D Structure Summary Card
    draw.rounded_rectangle((24, 158, 690, 965), radius=16, fill=PANEL_BG, outline=BORDER_COL, width=2)
    draw.text((44, 174), f"WebGL 3D Conformer Viewport — {compound_name}", fill=WHITE, font=F_H3)
    draw.rounded_rectangle((535, 170, 670, 200), radius=12, fill=(16, 185, 129, 40), outline=GREEN, width=1)
    draw.text((548, 177), "3Dmol.js Active", fill=GREEN, font=F_TINY)

    # 3D Viewport Canvas Box
    draw.rounded_rectangle((40, 210, 674, 680), radius=14, fill=(8, 14, 26), outline=BORDER_COL, width=2)

    # 3D Toolbar Buttons below viewport
    tools = [("Ball & Stick", True), ("VdW Surface", active_tab_idx == 1), ("Farmakofor 3D", active_tab_idx == 1), ("Ukur Jarak (Å)", active_tab_idx == 1), ("Ekspor .PDBQT", active_tab_idx == 5)]
    tx = 40
    for tname, t_on in tools:
        tw = len(tname) * 7 + 26
        draw.rounded_rectangle((tx, 692, tx + tw, 724), radius=8,
                               fill=BLUE if t_on else CARD_DARK,
                               outline=CYAN if t_on else BORDER_COL, width=1)
        draw.text((tx + 12, 700), tname, fill=WHITE, font=F_TINY)
        tx += tw + 8

    # Bottom-Left 2D Structure & Identity Card
    draw.rounded_rectangle((40, 736, 674, 948), radius=12, fill=CARD_DARK, outline=BORDER_COL, width=1)
    img.paste(IMG2D_ATOR, (54, 752))
    draw.text((250, 750), f"{compound_name} (CID: {cid})", fill=WHITE, font=F_H3)
    draw.text((250, 780), f"Rumus Molekul : {formula}", fill=CYAN, font=F_MONO)
    draw.text((250, 806), f"Bobot Molekul : {mw}", fill=WHITE, font=F_BODY)
    draw.text((250, 832), f"Lipofilisitas : XLogP = {logp}", fill=GREEN, font=F_BODY)
    draw.text((250, 858), f"Polaritas     : TPSA = {tpsa}", fill=AMBER, font=F_BODY)
    draw.text((250, 886), "InChIKey      : XUKUURHRXDUEBC-KAYWLYCHSA-N", fill=MUTED, font=F_TINY)
    draw.rounded_rectangle((250, 912, 465, 938), radius=6, fill=(16, 185, 129), outline=GREEN)
    draw.text((262, 917), "✓ Validasi 100% Match SwissADME", fill=BG_DARK, font=F_TINY)

    # Right Column: Main Analysis & CADD Suite Container
    draw.rounded_rectangle((708, 158, WIDTH - 24, 965), radius=16, fill=PANEL_BG, outline=BORDER_COL, width=2)

    # Navigation Tabs inside Right Column
    tabs = [
        "1. Fisikokimia & RO5",
        "2. SwissADME & BCS",
        "3. BOILED-Egg & SA",
        "4. QSAR & Ensemble ML",
        "5. Analog Tanimoto",
        "6. CADD Docking & FDA"
    ]
    tab_x = 728
    for idx, tlabel in enumerate(tabs):
        is_act = (idx == active_tab_idx)
        tw = 186
        draw.rounded_rectangle((tab_x, 174, tab_x + tw, 214), radius=10,
                               fill=BLUE if is_act else CARD_DARK,
                               outline=CYAN if is_act else BORDER_COL, width=2 if is_act else 1)
        draw.text((tab_x + 14, 186), tlabel, fill=WHITE if is_act else MUTED, font=F_TINY)
        tab_x += tw + 8


def draw_right_panel_content(img, draw, scene_idx, progress):
    rx0, ry0, rx1, ry1 = 728, 228, WIDTH - 44, 948

    if scene_idx in (0, 1):
        # Scene 1 & 2: Physicochemical Descriptors, Lipinski RO5, 3D Pharmacophore & Spatial Measurement
        draw.text((rx0, ry0), "Evaluasi Fisikokimia, Lipinski Rule of Five (RO5) & Geometri Spasial 3D", fill=WHITE, font=F_H2)
        draw.text((rx0, ry0 + 30), "Data diambil langsung dari PubChem PUG-REST API (NIH/NLM) & dievaluasi terhadap kriteria kimia medisinal.", fill=MUTED, font=F_SMALL)

        cards = [
            ("Bobot Molekul (MW)", "558.64 g/mol", "Batas RO5: <= 500 g/mol", "bRO5 (Substrat OATP1B1)", AMBER),
            ("Lipofilisitas (XLogP3)", "5.70", "Batas RO5: <= 5.0", "Afinitas Hidrofobik Tinggi", AMBER),
            ("Donor Ikatan H (HBD)", "4 Gugus (-OH/-NH)", "Batas RO5: <= 5", "✓ Lolos Kriteria Lipinski", GREEN),
            ("Akseptor Ikatan H (HBA)", "6 Atom (O/N)", "Batas RO5: <= 10", "✓ Lolos Kriteria Lipinski", GREEN),
            ("Luas Kutub (TPSA)", "111.79 Å²", "Batas Veber: <= 140 Å²", "✓ Absorpsi Usus Optimal", GREEN),
            ("Ikatan Fleksibel (RotB)", "12 Ikatan", "Filter Konformasi", "Fleksibilitas Rantai Heptanoat", CYAN),
        ]
        for i, (title, val, sub, badge_txt, col) in enumerate(cards):
            col_i = i % 3
            row_i = i // 3
            cx0 = rx0 + col_i * 388
            cy0 = ry0 + 68 + row_i * 155
            draw.rounded_rectangle((cx0, cy0, cx0 + 372, cy0 + 140), radius=12, fill=CARD_BG, outline=col, width=2)
            draw.text((cx0 + 18, cy0 + 14), title, fill=MUTED, font=F_SMALL)
            draw.text((cx0 + 18, cy0 + 42), val, fill=WHITE, font=F_MONO_LG)
            draw.text((cx0 + 18, cy0 + 78), sub, fill=MUTED, font=F_TINY)
            draw.rounded_rectangle((cx0 + 18, cy0 + 104, cx0 + 350, cy0 + 128), radius=6, fill=CARD_DARK, outline=col, width=1)
            draw.text((cx0 + 28, cy0 + 108), badge_txt, fill=col, font=F_TINY)

        # Bottom Spatial 3D Pharmacophore & Distance Measurement Box
        by0 = ry0 + 390
        draw.rounded_rectangle((rx0, by0, rx1, ry1), radius=14, fill=CARD_BG, outline=CYAN, width=2)
        draw.text((rx0 + 22, by0 + 16), "🎯 Inovasi 3D CADD: Pemetaan Farmakofor Spasial & Pengukuran Jarak Euclidean (Å)", fill=CYAN, font=F_H3)
        features = [
            ("🔴 Bola Merah (HBA - Hydrogen Bond Acceptor)", "Menandai 6 pusat akseptor ikatan hidrogen (gugus karbonil & karboksilat pengikat residu Ser684/Lys691).", RED),
            ("🔵 Bola Biru (HBD - Hydrogen Bond Donor)", "Menandai 4 gugus hidroksil (-OH) & amida (-NH) untuk jangkar ikatan hidrogen situs katalitik.", BLUE),
            ("🟡 Bola Kuning (Aromatic / Hydrophobic Core)", "Menandai cincin pirol & fluorofenil yang berinteraksi van der Waals pada kantung hidrofobik.", AMBER),
            ("📏 Alat Ukur Jarak & Sudut Ikatan 3D Real-Time", "Jarak Atom O3 — C14: d = √(dx² + dy² + dz²) = 4.82 Å (0.482 nm) | Sudut Valensi θ = 118.4°", GREEN),
        ]
        fy = by0 + 56
        for ftitle, fdesc, fcol in features:
            draw.rounded_rectangle((rx0 + 22, fy, rx1 - 22, fy + 60), radius=10, fill=CARD_DARK, outline=fcol, width=1)
            draw.text((rx0 + 36, fy + 8), ftitle, fill=fcol, font=F_BOLD)
            draw.text((rx0 + 36, fy + 32), fdesc, fill=WHITE, font=F_SMALL)
            fy += 68

    elif scene_idx == 2:
        # Scene 3: SwissADME Radar, PAINS & Henderson-Hasselbalch / BCS
        draw.text((rx0, ry0), "SwissADME 6-Axis Bioavailability Radar, PAINS Alert & Ionisasi Fisiologis", fill=WHITE, font=F_H2)
        # Left Radar Box
        draw.rounded_rectangle((rx0, ry0 + 42, rx0 + 540, ry1), radius=14, fill=CARD_BG, outline=BORDER_COL, width=2)
        draw.text((rx0 + 20, ry0 + 58), "Radar Heptagonal Bioavailabilitas Oral (Standar SIB)", fill=CYAN, font=F_H3)
        rcx, rcy = rx0 + 270, ry0 + 360
        axes = ["LIPO (LogP)", "SIZE (MW)", "POLAR (TPSA)", "INSOLU (LogS)", "INSATU (Fsp3)", "FLEX (RotB)"]
        for ring_r in (60, 120, 180, 220):
            pts = [(rcx + ring_r * math.cos(k * math.pi / 3 - math.pi / 2),
                    rcy + ring_r * math.sin(k * math.pi / 3 - math.pi / 2)) for k in range(6)]
            draw.polygon(pts, outline=(50, 70, 100), width=1)
        # Optimal pink/cyan zone polygon
        opt_pts = [(rcx + 150 * math.cos(k * math.pi / 3 - math.pi / 2),
                    rcy + 150 * math.sin(k * math.pi / 3 - math.pi / 2)) for k in range(6)]
        draw.polygon(opt_pts, outline=GREEN, width=2)
        # Compound animated polygon
        anim = min(1.0, 0.4 + progress * 0.8)
        vals = [0.85, 0.80, 0.72, 0.68, 0.55, 0.78]
        mol_pts = []
        for k, v in enumerate(vals):
            ang = k * math.pi / 3 - math.pi / 2
            rr = 210 * v * anim
            mol_pts.append((rcx + rr * math.cos(ang), rcy + rr * math.sin(ang)))
            lx = rcx + 245 * math.cos(ang) - 42
            ly = rcy + 245 * math.sin(ang) - 10
            draw.text((lx, ly), axes[k], fill=WHITE, font=F_TINY)
        draw.polygon(mol_pts, outline=CYAN, width=4)
        for px, py in mol_pts:
            draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=CYAN)

        # Right column boxes: PAINS, Pfizer 3/75, Henderson-Hasselbalch, BCS
        bx = rx0 + 560
        boxes = [
            ("🛡️ Peringatan Struktur PAINS & Brenk", "0 Alert Terdeteksi (Bebas Gugus Kuinon, Rodanin, Katekol & Epoksida Reaktif)", "Menjamin senyawa tidak menghasilkan sinyal positif palsu (false-positive) pada bioassay HTS.", GREEN),
            ("⚠️ Aturan Toksisitas Pfizer 3/75", "AMAN — TPSA = 111.79 Å² (> 75 Å²) Mengimbangi Lipofilisitas", "Risiko toksisitas preklinis in vivo meningkat 2.5x hanya jika LogP > 3 DAN TPSA < 75 Å².", CYAN),
            ("🧪 Ionisasi Henderson-Hasselbalch (pKa = 4.46)", "Lambung (pH 1.2): 0.05% Terion | Darah/Usus (pH 7.4): 99.89% Terion (Anion Karboksilat)", "Kelarutan meningkat tajam pada pH fisiologis duodenum, mendukung absorpsi transpor aktif.", PURPLE),
            ("💊 Biopharmaceutics Classification System (BCS)", "BCS Kelas II (Permeabilitas Membran Tinggi, Kelarutan Air Intrinsik ESOL LogS = -5.82)", "Rekomendasi Formulasi: Penggunaan garam kalsium trihidrat amorf / dispersi padat.", AMBER),
        ]
        by = ry0 + 42
        for btitle, bmain, bsub, bcol in boxes:
            draw.rounded_rectangle((bx, by, rx1, by + 160), radius=12, fill=CARD_BG, outline=bcol, width=2)
            draw.text((bx + 18, by + 16), btitle, fill=bcol, font=F_H3)
            draw.text((bx + 18, by + 50), bmain, fill=WHITE, font=F_BOLD)
            draw.text((bx + 18, by + 84), bsub, fill=MUTED, font=F_SMALL)
            by += 174

    elif scene_idx == 3:
        # Scene 4: Multi-Model Machine Learning Ensemble & ChEMBL QSAR + XAI SHAP Attribution
        draw.text((rx0, ry0), "Pemodelan QSAR ChEMBL & Komparasi 4 Algoritma Machine Learning (Real-Time)", fill=WHITE, font=F_H2)
        draw.rounded_rectangle((rx1 - 355, ry0 - 2, rx1, ry0 + 30), radius=14, fill=CARD_DARK, outline=GREEN, width=2)
        draw.text((rx1 - 340, ry0 + 5), "✓ Konsensus 3 Model ML: 97.2% (σ = 0.04)", fill=GREEN, font=F_TINY)

        # Top 4 ML Model Cards (Stacking, OLS/Ridge, Random Forest 15-Tree, MLP Neural Net)
        active_ml = int(progress * 4) % 4
        ml_models = [
            ("Stacking Meta-Ensemble", "Inverse-Var Weighted (OLS+RF+MLP)", "pIC50: 8.54 ± 0.16", "IC50: 2.9 nM", "R²: 0.962 | RMSE: 0.14", CYAN),
            ("Linear OLS / Ridge QSAR", "L2 Hyperplane + Hat Leverage h*", "pIC50: 8.52 ± 0.21", "IC50: 3.0 nM", "R²: 0.918 | RMSE: 0.19", BLUE),
            ("Random Forest Regressor", "15 Bootstrap CART Decision Trees", "pIC50: 8.58 ± 0.17", "IC50: 2.6 nM", "R²: 0.954 | RMSE: 0.15", GREEN),
            ("MLP Neural Network", "Deep Net 5→8→4→1 (tanh / ELU)", "pIC50: 8.51 ± 0.18", "IC50: 3.1 nM", "R²: 0.946 | RMSE: 0.16", PURPLE),
        ]
        for idx, (mname, march, mpic, mic, mstat, mcol) in enumerate(ml_models):
            mx0 = rx0 + idx * 290
            my0 = ry0 + 42
            is_sel = (idx == active_ml)
            draw.rounded_rectangle((mx0, my0, mx0 + 278, my0 + 165), radius=12,
                                   fill=(22, 48, 78) if is_sel else CARD_BG,
                                   outline=mcol if is_sel else BORDER_COL, width=3 if is_sel else 1)
            draw.text((mx0 + 14, my0 + 12), mname, fill=mcol, font=F_BOLD)
            if is_sel:
                draw.rounded_rectangle((mx0 + 212, my0 + 10, mx0 + 266, my0 + 32), radius=8, fill=mcol)
                draw.text((mx0 + 222, my0 + 13), "AKTIF", fill=BG_DARK, font=F_TINY)
            draw.text((mx0 + 14, my0 + 38), march, fill=MUTED, font=F_TINY)
            draw.text((mx0 + 14, my0 + 66), mpic, fill=WHITE, font=F_MONO)
            draw.text((mx0 + 14, my0 + 96), f"Estimasi {mic}  |  ΔG = -11.65 kkal/mol", fill=GREEN, font=F_TINY)
            draw.line((mx0 + 14, my0 + 126, mx0 + 264, my0 + 126), fill=BORDER_COL, width=1)
            draw.text((mx0 + 14, my0 + 134), mstat, fill=WHITE, font=F_TINY)

        # Middle Left: QSAR Regression Plot (pIC50 vs XLogP)
        px0, py0, px1, py1 = rx0, ry0 + 222, rx0 + 590, ry1
        draw.rounded_rectangle((px0, py0, px1, py1), radius=14, fill=CARD_BG, outline=BORDER_COL, width=2)
        draw.text((px0 + 18, py0 + 14), "Plot Regresi Seri Statin ChEMBL (Target: HMG-CoA Reductase CHEMBL402)", fill=CYAN, font=F_BOLD)
        draw.text((px0 + 18, py0 + 40), "pIC50 = +0.44(LogP) + 6.72 - 0.005(ΔTPSA)   |   Q²_LOO = 0.891   |   AD: In-Domain (h = 0.21 < h* = 0.75)", fill=GREEN, font=F_TINY)
        # Plot axes
        gx0, gy0, gx1, gy1 = px0 + 58, py0 + 80, px1 - 28, py1 - 42
        draw.line((gx0, gy1, gx1, gy1), fill=MUTED, width=2)
        draw.line((gx0, gy0, gx0, gy1), fill=MUTED, width=2)
        # Regression line
        draw.line((gx0 + 20, gy1 - 45, gx1 - 20, gy0 + 35), fill=CYAN, width=3)
        pts_data = [
            (0.15, 0.22, "Pravastatin (7.15)"),
            (0.28, 0.78, "Rosuvastatin (8.85)"),
            (0.65, 0.52, "Fluvastatin (7.92)"),
            (0.72, 0.74, "Atorvastatin (8.52)"),
            (0.82, 0.82, "Pitavastatin (8.68)"),
            (0.88, 0.92, "Cerivastatin (9.10)"),
        ]
        for fx, fy_val, plab in pts_data:
            sx = gx0 + fx * (gx1 - gx0)
            sy = gy1 - fy_val * (gy1 - gy0)
            is_ator = "Atorvastatin" in plab
            r_pt = 9 if is_ator else 6
            draw.ellipse((sx - r_pt, sy - r_pt, sx + r_pt, sy + r_pt), fill=AMBER if is_ator else PURPLE, outline=WHITE, width=2)
            draw.text((sx - 35, sy - 24), plab, fill=AMBER if is_ator else WHITE, font=F_TINY)

        # Middle Right: Explainable AI (XAI) SHAP Attribution Breakdown
        xx0, xy0 = rx0 + 608, ry0 + 222
        draw.rounded_rectangle((xx0, xy0, rx1, ry1), radius=14, fill=CARD_BG, outline=PURPLE, width=2)
        draw.text((xx0 + 18, xy0 + 16), "🧠 Explainable AI (XAI) — SHAP Feature Attribution", fill=PURPLE, font=F_H3)
        draw.text((xx0 + 18, xy0 + 44), "Dekonvolusi kontribusi aditif setiap deskriptor terhadap baseline E[pIC50] = 7.68:", fill=MUTED, font=F_TINY)

        shap_items = [
            ("Lipofilisitas (LogP = 5.70)", "+0.68 pIC50", 0.86, GREEN, "Kontribusi desolvasi hidrofobik kuat pada kantung katalitik HMGCR"),
            ("Ikatan Hidrogen (HBD: 4 / HBA: 6)", "+0.28 pIC50", 0.55, GREEN, "Jangkar ikatan H spesifik dengan residu katalitik Ser684, Asp690 & Lys691"),
            ("Polaritas Topologis (TPSA = 111.8 Å²)", "-0.06 pIC50", 0.24, RED, "Keseimbangan kontak polar vs penalti energi desolvasi air"),
            ("Sterik Massa (MW = 558.6 g/mol)", "-0.04 pIC50", 0.18, RED, "Batas ambang volume kavitas kantung aktif (MW > 520 Da)"),
        ]
        sy_pos = xy0 + 78
        for sname, sdelta, spct, scol, sdesc in shap_items:
            draw.rounded_rectangle((xx0 + 18, sy_pos, rx1 - 18, sy_pos + 92), radius=10, fill=CARD_DARK, outline=BORDER_COL, width=1)
            draw.text((xx0 + 30, sy_pos + 10), sname, fill=WHITE, font=F_BOLD)
            draw.text((rx1 - 145, sy_pos + 10), sdelta, fill=scol, font=F_MONO)
            bar_w = int((rx1 - xx0 - 60) * spct * min(1.0, 0.5 + progress * 0.7))
            draw.rounded_rectangle((xx0 + 30, sy_pos + 38, xx0 + 30 + bar_w, sy_pos + 50), radius=5, fill=scol)
            draw.text((xx0 + 30, sy_pos + 58), sdesc, fill=MUTED, font=F_TINY)
            sy_pos += 102

    elif scene_idx == 4:
        # Scene 5: BOILED-Egg ADMET, SA Score & Tanimoto 2D Similarity Analog Search
        draw.text((rx0, ry0), "Prediksi ADMET BOILED-Egg (HIA/BBB), SA Score & Penapisan Analog Tanimoto", fill=WHITE, font=F_H2)
        # Left: BOILED-Egg Visual Model
        bx0, by0, bx1, by1 = rx0, ry0 + 42, rx0 + 540, ry1
        draw.rounded_rectangle((bx0, by0, bx1, by1), radius=14, fill=CARD_BG, outline=BORDER_COL, width=2)
        draw.text((bx0 + 18, by0 + 16), "🍳 Model Prediksi BOILED-Egg (Daina & Zoete, 2016)", fill=AMBER, font=F_H3)
        draw.text((bx0 + 18, by0 + 44), "Pemetaan serentak Absorpsi Gastrointestinal (HIA) & Penetrasi Sawar Darah Otak (BBB)", fill=MUTED, font=F_TINY)
        ecx, ecy = bx0 + 270, by0 + 310
        # Egg White (HIA)
        draw.ellipse((ecx - 210, ecy - 150, ecx + 210, ecy + 160), fill=(241, 245, 249), outline=WHITE, width=3)
        draw.text((ecx - 85, ecy + 115), "ZONA PUTIH: Absorpsi Usus (HIA Tinggi)", fill=(15, 23, 42), font=F_TINY)
        # Egg Yolk (BBB)
        draw.ellipse((ecx - 105, ecy - 115, ecx + 95, ecy + 55), fill=(251, 191, 36), outline=(217, 119, 6), width=3)
        draw.text((ecx - 78, ecy - 35), "YOLK: BBB Permeant (SSP)", fill=(15, 23, 42), font=F_TINY)
        # Plotted reference drugs
        egg_pts = [
            (ecx - 30, ecy - 65, BLUE, "Ibuprofen (BBB+)"),
            (ecx + 25, ecy - 50, RED, "Paracetamol (BBB+)"),
            (ecx + 95, ecy + 55, BLUE, "Atorvastatin (HIA+ / PGP+)"),
        ]
        for px, py, pcol, plab in egg_pts:
            draw.ellipse((px - 10, py - 10, px + 10, py + 10), fill=pcol, outline=WHITE, width=2)
            draw.text((px + 14, py - 8), plab, fill=(15, 23, 42), font=F_BOLD)

        # Synthetic Accessibility Score bar inside BOILED-Egg card bottom
        draw.rounded_rectangle((bx0 + 18, by1 - 165, bx1 - 18, by1 - 18), radius=10, fill=CARD_DARK, outline=GREEN, width=1)
        draw.text((bx0 + 32, by1 - 150), "🧪 Synthetic Accessibility (SA Score): 3.4 / 10 (Mudah-Moderat)", fill=GREEN, font=F_BOLD)
        draw.rounded_rectangle((bx0 + 32, by1 - 116, bx1 - 32, by1 - 96), radius=8, fill=(30, 41, 59))
        draw.rounded_rectangle((bx0 + 32, by1 - 116, bx0 + 32 + int(460 * 0.34), by1 - 96), radius=8, fill=GREEN)
        draw.text((bx0 + 32, by1 - 82), "Benchmark Ertl & Schuffenhauer: Synthon pirol komersial tersedia, 2 pusat kiralitas terkontrol.", fill=MUTED, font=F_TINY)

        # Right: Tanimoto 2D Fingerprint Analog Search Cards
        ax0 = rx0 + 558
        draw.rounded_rectangle((ax0, by0, rx1, by1), radius=14, fill=CARD_BG, outline=CYAN, width=2)
        draw.text((ax0 + 18, by0 + 16), "🌿 Penapisan Analog Cerdas (PubChem FastSimilarity Tanimoto ≥ 85%)", fill=CYAN, font=F_H3)
        analogs = [
            ("Pitavastatin Calcium", "CID: 5282452", "94.2% Tanimoto", "MW: 421.46 | LogP: 4.30 | TPSA: 77.8 Å²", "Lulus penuh Lipinski RO5 (4/4) — Alternatif Lead Rescue optimal.", GREEN),
            ("Fluvastatin Sodium", "CID: 446155", "91.6% Tanimoto", "MW: 411.47 | LogP: 4.10 | TPSA: 77.8 Å²", "Indol fluorofenil analog dengan risiko interaksi CYP3A4 minimal.", CYAN),
            ("Rosuvastatin", "CID: 446157", "88.9% Tanimoto", "MW: 481.54 | LogP: 1.90 | TPSA: 140.8 Å²", "Hidrofilisitas tinggi (sulfonamida-pirimidina), selektif hepatosit.", PURPLE),
            ("Cerivastatin", "CID: 446156", "87.4% Tanimoto", "MW: 459.55 | LogP: 3.80 | TPSA: 77.8 Å²", "Afinitas picomolar tertinggi (IC50 = 0.8 nM, pIC50 = 9.10).", AMBER),
        ]
        ay = by0 + 58
        for aname, acid, atan, amet, anote, acol in analogs:
            draw.rounded_rectangle((ax0 + 18, ay, rx1 - 18, ay + 142), radius=12, fill=CARD_DARK, outline=acol, width=1)
            img.paste(IMG2D_PARA if "Rosuva" in aname else IMG2D_OSEL, (ax0 + 30, ay + 18))
            draw.text((ax0 + 185, ay + 14), f"{aname}  ({acid})", fill=WHITE, font=F_BOLD)
            draw.rounded_rectangle((rx1 - 175, ay + 12, rx1 - 32, ay + 38), radius=10, fill=acol)
            draw.text((rx1 - 162, ay + 17), atan, fill=BG_DARK, font=F_TINY)
            draw.text((ax0 + 185, ay + 46), amet, fill=CYAN, font=F_MONO)
            draw.text((ax0 + 185, ay + 74), anote, fill=MUTED, font=F_TINY)
            draw.rounded_rectangle((ax0 + 185, ay + 102, ax0 + 365, ay + 128), radius=6, fill=BLUE)
            draw.text((ax0 + 200, ay + 107), "⚡ Analisis Senyawa Ini", fill=WHITE, font=F_TINY)
            ay += 152

    else:
        # Scene 6 & 7: CADD Suite — AutoDock Vina Molecular Docking, Toxicity QSTR, openFDA FAERS & Batch CSV
        draw.text((rx0, ry0), "CADD Suite: Simulasi Molecular Docking AutoDock Vina, QSTR & openFDA FAERS", fill=WHITE, font=F_H2)

        # Top Box: AutoDock Vina Empirical Scoring Deconvolution & PDBQT Export
        dy0 = ry0 + 40
        draw.rounded_rectangle((rx0, dy0, rx1, dy0 + 315), radius=14, fill=CARD_BG, outline=CYAN, width=2)
        draw.text((rx0 + 20, dy0 + 14), "🧬 In Silico Molecular Docking Notebook — Target RCSB PDB: 1HWK × Atorvastatin", fill=CYAN, font=F_H3)
        dock_metrics = [
            ("Energi Bebas Ikatan (ΔG_bind)", "-10.84 kcal/mol", CYAN),
            ("Konstanta Inhibisi (Ki, 298 K)", "11.20 nM", GREEN),
            ("Ligand Efficiency (LE)", "0.27 kcal/mol/atom", PURPLE),
            ("Koordinat Grid Box kantung Aktif", "X:19.4, Y:-8.2, Z:14.7 (22³ Å³)", AMBER),
        ]
        for idx, (mlab, mval, mcol) in enumerate(dock_metrics):
            mx = rx0 + 20 + idx * 282
            draw.rounded_rectangle((mx, dy0 + 52, mx + 268, dy0 + 132), radius=10, fill=CARD_DARK, outline=mcol, width=1)
            draw.text((mx + 14, dy0 + 62), mlab, fill=MUTED, font=F_TINY)
            draw.text((mx + 14, dy0 + 90), mval, fill=mcol, font=F_MONO)

        # Vina Energy Terms Breakdown
        terms = [
            ("Gauss₁ Steric Attraction", "-2.94 kcal/mol", GREEN),
            ("Gauss₂ Dispersion", "-4.18 kcal/mol", GREEN),
            ("Hydrophobic Contacts", "-2.65 kcal/mol", CYAN),
            ("H-Bonding (Ser684/Lys691)", "-2.35 kcal/mol", BLUE),
            ("Torsional Entropy Penalty", "+1.28 kcal/mol", RED),
        ]
        ty = dy0 + 148
        for idx, (tname, tval, tcol) in enumerate(terms):
            tx = rx0 + 20 + (idx % 3) * 376
            row = idx // 3
            draw.rounded_rectangle((tx, ty + row * 74, tx + 362, ty + row * 74 + 62), radius=8, fill=CARD_DARK, outline=BORDER_COL, width=1)
            draw.text((tx + 14, ty + row * 74 + 10), tname, fill=WHITE, font=F_SMALL)
            draw.text((tx + 14, ty + row * 74 + 34), tval, fill=tcol, font=F_MONO)

        draw.rounded_rectangle((rx0 + 772, ty + 74, rx1 - 20, ty + 136), radius=10, fill=GREEN)
        draw.text((rx0 + 792, ty + 94), "📥 Unduh AutoDock Vina (.PDBQT) + Muatan PEOE", fill=BG_DARK, font=F_BOLD)

        # Bottom Left: QSTR Logistic Regression Organ Toxicity (hERG, Ames, DILI, CYP450)
        ty0 = dy0 + 332
        draw.rounded_rectangle((rx0, ty0, rx0 + 565, ry1), radius=14, fill=CARD_BG, outline=PURPLE, width=2)
        draw.text((rx0 + 18, ty0 + 14), "🛡️ Prediksi Toksisitas Organ QSTR (Logistic Regression) & CYP450", fill=PURPLE, font=F_H3)
        tox_rows = [
            ("Kardiotoksisitas hERG (Kv11.1)", "Risiko Rendah — P(Blokade) = 24% (Est. IC50 ≈ 38.5 µM)", GREEN),
            ("Mutagenisitas Ames (Kazius-Bursi)", "Non-Mutagenik (Lolos 6 kelas toksikofor DNA)", GREEN),
            ("Hepatotoksisitas DILI (FDA LTKB)", "Risiko Moderat (Pemantauan transaminase ALT/AST)", AMBER),
            ("Metabolisme Sitokrom P450", "Substrat Primer CYP3A4 (62% klirens) | Non-Inhibitor CYP2D6", CYAN),
        ]
        ry_t = ty0 + 54
        for ttitle, tdesc, tcol in tox_rows:
            draw.rounded_rectangle((rx0 + 18, ry_t, rx0 + 547, ry_t + 64), radius=8, fill=CARD_DARK, outline=tcol, width=1)
            draw.text((rx0 + 30, ry_t + 8), ttitle, fill=tcol, font=F_BOLD)
            draw.text((rx0 + 30, ry_t + 34), tdesc, fill=WHITE, font=F_TINY)
            ry_t += 72

        # Bottom Right: openFDA FAERS Pharmacovigilance & Batch CSV / Dossier
        fx0 = rx0 + 582
        draw.rounded_rectangle((fx0, ty0, rx1, ry1), radius=14, fill=CARD_BG, outline=GREEN, width=2)
        draw.text((fx0 + 18, ty0 + 14), "🏥 Farmakovigilans openFDA (FAERS Live) & Utilitas Riset", fill=GREEN, font=F_H3)
        fda_bars = [
            ("Myalgia / Nyeri Otot Skelet", "PRR = 4.82 (Sinyal Terdeteksi)", 0.78, AMBER),
            ("Peningkatan Enzim Hepar (ALT/AST)", "PRR = 2.45 (Pemantauan Klinis)", 0.48, CYAN),
            ("Arthralgia / Nyeri Sendi", "PRR = 1.62 (Frekuensi Rendah)", 0.34, GREEN),
        ]
        fy = ty0 + 56
        for fname, fprr, fpct, fcol in fda_bars:
            draw.text((fx0 + 22, fy), f"{fname}   —   {fprr}", fill=WHITE, font=F_SMALL)
            draw.rounded_rectangle((fx0 + 22, fy + 26, rx1 - 22, fy + 42), radius=6, fill=CARD_DARK)
            draw.rounded_rectangle((fx0 + 22, fy + 26, fx0 + 22 + int(510 * fpct), fy + 42), radius=6, fill=fcol)
            fy += 58

        draw.rounded_rectangle((fx0 + 22, fy + 8, rx1 - 22, ry1 - 18), radius=10, fill=CARD_DARK, outline=CYAN, width=1)
        draw.text((fx0 + 36, fy + 20), "📊 Batch CSV Sifter, 2D/3D Chemical Sketcher & Dossier Ilmiah PDF", fill=CYAN, font=F_BOLD)
        draw.text((fx0 + 36, fy + 48), "• Unggah ratusan CID via .CSV  • Komparasi 3 Obat  • Cetak Laporan PDF", fill=WHITE, font=F_SMALL)
        draw.text((fx0 + 36, fy + 74), "🌐 Live Web: https://novarani1511.github.io/pharmapulse-3d/", fill=GREEN, font=F_MONO)


def draw_cursor(draw, x, y, clicking=False):
    if clicking:
        draw.ellipse((x - 22, y - 22, x + 22, y + 22), outline=CYAN, width=3)
    pts = [(x, y), (x, y + 26), (x + 7, y + 20), (x + 13, y + 32), (x + 18, y + 29), (x + 12, y + 17), (x + 21, y + 17)]
    draw.polygon(pts, fill=WHITE, outline=BG_DARK)


def draw_subtitle_bar(draw, text, progress_total, scene_label):
    # Bottom Subtitle & Timeline Overlay
    draw.rounded_rectangle((160, 976, WIDTH - 160, 1064), radius=16, fill=(9, 13, 22), outline=CYAN, width=2)
    draw.rounded_rectangle((180, 986, 490, 1012), radius=8, fill=CYAN)
    draw.text((194, 990), scene_label, fill=BG_DARK, font=F_TINY)
    draw.text((185, 1018), text, fill=WHITE, font=F_SUB)

    # Progress Bar at bottom edge of subtitle box
    bar_w = int((WIDTH - 360) * progress_total)
    draw.rounded_rectangle((180, 1052, WIDTH - 180, 1058), radius=3, fill=CARD_BG)
    draw.rounded_rectangle((180, 1052, 180 + max(8, bar_w), 1058), radius=3, fill=GREEN)


SCENES = [
    (0.0, 26.0, 0, "BAGIAN 1 / 7 — ANTARMUKA & INGESTI BIG DATA",
     "PharmaPulse 3D menghubungkan PubChem PUG-REST API, ChEMBL, RCSB PDB & 34 senyawa obat terkurasi."),
    (26.0, 52.0, 1, "BAGIAN 2 / 7 — FARMAKOFOR 3D & JARAK IKATAN (Å)",
     "Visualisasi konformer 3D WebGL dengan pemetaan bola Farmakofor (HBA, HBD, Aromatik) & ukur jarak atom (Å)."),
    (52.0, 82.0, 2, "BAGIAN 3 / 7 — DRUGLIKENESS, SWISSADME & BCS",
     "Evaluasi Lipinski RO5, Veber, Pfizer 3/75, Radar SwissADME 6-Sumbu, PAINS Alert & ionisasi fisiologis pH."),
    (82.0, 118.0, 3, "BAGIAN 4 / 7 — ENSEMBLE MACHINE LEARNING & XAI",
     "Komparasi 4 algoritma ML (Stacking, OLS/Ridge, Random Forest 15-Tree, MLP Neural Net) & atribusi SHAP XAI."),
    (118.0, 148.0, 4, "BAGIAN 5 / 7 — MODEL BOILED-EGG, SA SCORE & TANIMOTO",
     "Prediksi serentak absorpsi usus (HIA) & sawar darah otak (BBB), kemudahan sintesis, & analog Tanimoto >=85%."),
    (148.0, 179.47, 5, "BAGIAN 6 & 7 — DOCKING VINA, QSTR & OPENFDA FAERS",
     "Simulasi energi ikatan AutoDock Vina (ΔG kcal/mol), ekspor .PDBQT, toksisitas organ QSTR, & sinyal openFDA."),
]


def get_cursor_pos(scene_idx, local_p):
    waypoints = {
        0: [(1180, 54), (310, 124), (820, 194), (910, 340)],
        1: [(380, 708), (495, 708), (360, 450), (1120, 750)],
        2: [(1010, 194), (990, 560), (1450, 380), (1450, 720)],
        3: [(1390, 194), (840, 340), (1130, 340), (1420, 340), (1710, 340), (1540, 660)],
        4: [(1200, 194), (990, 540), (1550, 420), (1550, 720)],
        5: [(1680, 194), (980, 350), (1640, 500), (1050, 750), (1550, 780)],
    }
    pts = waypoints.get(scene_idx, [(960, 540), (1200, 500)])
    seg_count = len(pts) - 1
    seg_f = local_p * seg_count
    seg_i = min(seg_count - 1, int(seg_f))
    t = seg_f - seg_i
    # Smooth cosine interpolation
    t_smooth = 0.5 - 0.5 * math.cos(t * math.pi)
    x = pts[seg_i][0] + (pts[seg_i + 1][0] - pts[seg_i][0]) * t_smooth
    y = pts[seg_i][1] + (pts[seg_i + 1][1] - pts[seg_i][1]) * t_smooth
    clicking = (abs(t - 0.92) < 0.06)
    return int(x), int(y), clicking


def main():
    audio_path = "narasi_suara_wanita.mp3"
    output_path = "Demo_Aplikasi_PharmaPulse_3D.mp4"
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    total_duration = 179.47
    total_frames = int(total_duration * FPS)

    # Pre-cache static scene backgrounds (without 3D molecule, dynamic overlays, cursor, and subtitle)
    scene_Order = [0, 1, 1, 3, 2, 5]  # tab highlights corresponding to each scene

    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
    ]
    if os.path.exists(audio_path):
        cmd.extend(["-i", audio_path, "-c:a", "aac", "-b:a", "128k", "-shortest"])
    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-crf", "22",
        output_path
    ])

    print(f"Generating {total_frames} frames ({total_duration:.1f}s @ {FPS} fps) -> {output_path} ...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    # Cache static chrome + right panel content across 12 progress steps per scene (72 cached base frames total)
    scene_step_cache = {}
    for s_idx in range(6):
        tab_map = {0: 0, 1: 0, 2: 1, 3: 3, 4: 2, 5: 5}
        for step_k in range(12):
            base_img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
            draw_base_chrome(base_img, tab_map[s_idx])
            d_step = ImageDraw.Draw(base_img)
            draw_right_panel_content(base_img, d_step, s_idx, step_k / 11.0)
            scene_step_cache[(s_idx, step_k)] = base_img

    for frame_idx in range(total_frames):
        t_sec = frame_idx / FPS
        progress_total = frame_idx / max(1, total_frames - 1)

        # Find current scene
        cur_scene = SCENES[-1]
        for sc in SCENES:
            if sc[0] <= t_sec <= sc[1]:
                cur_scene = sc
                break
        t_start, t_end, scene_idx, scene_label, sub_text = cur_scene
        local_p = (t_sec - t_start) / max(0.01, (t_end - t_start))
        step_k = min(11, max(0, int(local_p * 12)))

        frame = scene_step_cache[(scene_idx, step_k)].copy()
        draw = ImageDraw.Draw(frame)

        # Render rotating 3D conformer on left viewport
        angle_y = t_sec * 0.85
        angle_x = 0.28 + 0.14 * math.sin(t_sec * 0.4)
        draw_mol_3d(
            draw,
            (40, 210, 674, 680),
            MOL_ATOR,
            BONDS_ATOR,
            angle_y,
            angle_x,
            show_pharm=(scene_idx in (1, 3)),
            show_dist=(scene_idx == 1),
            show_pocket=(scene_idx == 5)
        )

        # Render subtitle & progress bar
        draw_subtitle_bar(draw, sub_text, progress_total, scene_label)

        # Render animated cursor
        cx, cy, clicking = get_cursor_pos(scene_idx, local_p)
        draw_cursor(draw, cx, cy, clicking=clicking)

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    stderr_out = proc.stderr.read().decode("utf-8", errors="ignore")
    proc.wait()
    if proc.returncode != 0:
        print("FFmpeg error:", stderr_out[-600:])
        raise RuntimeError(f"FFmpeg exited with code {proc.returncode}")
    print(f"Successfully created {output_path} ({os.path.getsize(output_path) / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    main()
