import io
from fpdf import FPDF

class Modern_CV_PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        # Désactiver les sauts de page automatiques pour gérer le layout asymétrique parfaitement
        self.set_auto_page_break(auto=False)
        
    def draw_layout(self, fullname, job_title):
        # 1. Fond de la page blanc
        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, 210, 297, "F")
        
        # 2. Colonne de Gauche (Gris-bleuté épuré)
        self.set_fill_color(240, 244, 248)
        self.rect(0, 0, 75, 297, "F")
        
        # 3. Bandeau Supérieur Droit (Bleu nuit très corporate)
        self.set_fill_color(44, 62, 80)
        self.rect(75, 0, 135, 45, "F")
        
        # Affichage du Nom Complet (Blanc)
        self.set_xy(82, 12)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, fullname.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        
        # Affichage du Poste Recherché (Bleu d'accentuation)
        self.set_xy(82, 24)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(52, 152, 219) # Bleu moderne brillant
        self.cell(0, 8, job_title.upper().encode('latin-1', 'replace').decode('latin-1'), ln=True)

def generate_pdf_from_text(fullname: str, job_title: str, cv_content: str) -> io.BytesIO:
    pdf = Modern_CV_PDF()
    pdf.add_page()
    pdf.draw_layout(fullname, job_title)
    
    # Encodage sécurisé global
    cv_content = cv_content.encode('latin-1', 'replace').decode('latin-1')
    sections = cv_content.split("---")
    
    # Marges et coordonnées pour l'asymétrie
    left_y = 15
    right_y = 55
    
    for section in sections:
        clean_section = section.strip()
        if not clean_section:
            continue
            
        lines = clean_section.split("\n")
        title = lines[0].strip().replace("**", "").upper()
        content_lines = [l.strip() for l in lines[1:] if l.strip()]
        
        # ==========================================
        # BLOCS COLONNE GAUCHE (Accroche & Compétences)
        # ==========================================
        if any(keyword in title for keyword in ["ACCROCHE", "COMPETENCE", "COMPÉTENCE", "CONTACT"]):
            pdf.set_xy(6, left_y)
            
            # Titre de la section à gauche
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(63, 6, title, ln=True)
            
            # CORRECTION ICI : set_line_width au lieu de set_thickness
            pdf.set_draw_color(52, 152, 219)
            pdf.set_line_width(0.5)
            pdf.line(6, pdf.get_y(), 25, pdf.get_y())
            pdf.ln(4)
            
            # Contenu
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(79, 93, 107) # Gris lisible
            
            for line in content_lines:
                if line.startswith("* ") or line.startswith("- "):
                    line = "- " + line[2:]
                line = line.replace("**", "")
                
                pdf.set_x(6)
                pdf.multi_cell(63, 5, line)
                pdf.ln(1)
                
            left_y = pdf.get_y() + 8
            
        # ==========================================
        # BLOCS COLONNE DROITE (Expériences & Formations)
        # ==========================================
        else:
            pdf.set_xy(82, right_y)
            
            # Titre de la section à droite
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(118, 6, title, ln=True)
            
            # CORRECTION ICI : set_line_width au lieu de set_thickness
            pdf.set_draw_color(220, 224, 230)
            pdf.set_line_width(0.2)
            pdf.line(82, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
            
            # Contenu
            for line in content_lines:
                pdf.set_x(82)
                
                # S'il s'agit d'une ligne principale (Poste ou Diplôme)
                if line.startswith("* ") or line.startswith("- "):
                    pdf.set_font("Helvetica", "B", 11)
                    pdf.set_text_color(44, 62, 80)
                    clean_line = line[2:].replace("**", "")
                    pdf.multi_cell(118, 5, clean_line)
                else:
                    # S'il s'agit du descriptif de l'expérience (retrait vers la droite)
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(100, 110, 120)
                    clean_line = line.replace("**", "")
                    pdf.set_x(85) # Décale le texte pour faire un effet de sous-puce propre
                    pdf.multi_cell(115, 4.5, clean_line)
                pdf.ln(1)
                
            right_y = pdf.get_y() + 6

    # Génération du buffer
    pdf_buffer = io.BytesIO()
    pdf_buffer.write(pdf.output())
    pdf_buffer.seek(0)
    
    return pdf_buffer