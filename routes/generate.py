from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.claude_service import generate_cv_content
from services.pdf_service import generate_pdf_from_text
import io

router = APIRouter()

# ==========================================
# MODÈLES DE DONNÉES (PYDANTIC)
# ==========================================

# Modèle de la requête pour créer le texte du CV
class CVRequest(BaseModel):
    fullname: str
    job_title: str          
    experience_years: int   
    skills: str             
    background: str         

# Modèle de la réponse pour le texte du CV
class CVResponse(BaseModel):
    fullname: str
    job_title: str
    experience_years: int
    skills: str
    background: str
    cv_content: str         

# Modèle de la requête pour générer le fichier PDF
class PDFRequest(BaseModel):
    fullname: str
    job_title: str
    cv_content: str

# ==========================================
# ENDPOINTS (ROUTES API)
# ==========================================

@router.post("/generate", response_model=CVResponse)
async def generate(request: CVRequest):

    # 1. Vérification rigoureuse champ par champ
    if not request.fullname or request.fullname.strip() == "":
        raise HTTPException(status_code=400, detail="Le nom complet (fullname) est obligatoire.")
        
    if not request.job_title or request.job_title.strip() == "":
        raise HTTPException(status_code=400, detail="Le poste visé (job_title) est obligatoire.")
        
    if request.experience_years < 0:
        raise HTTPException(status_code=400, detail="Le nombre d'années d'expérience ne peut pas être négatif.")
        
    if not request.skills or request.skills.strip() == "":
        raise HTTPException(status_code=400, detail="Veuillez fournir au moins une compétence (skills).")
        
    if not request.background or request.background.strip() == "":
        raise HTTPException(status_code=400, detail="Le résumé du parcours (background) est obligatoire.")

    # 2. Appel au service de génération
    cv_generated = await generate_cv_content(
        fullname=request.fullname,
        job_title=request.job_title,
        experience_years=request.experience_years,
        skills=request.skills,
        background=request.background
    )

    # 3. Retour de la réponse structurée
    return CVResponse(
        fullname=request.fullname,
        job_title=request.job_title,
        experience_years=request.experience_years,
        skills=request.skills,
        background=request.background,
        cv_content=cv_generated
    )


@router.post("/export-pdf")
async def export_cv_pdf(request: PDFRequest):
    
    # 1. Vérification individuelle des entrées pour le PDF
    if not request.fullname or request.fullname.strip() == "":
        raise HTTPException(status_code=400, detail="Le nom complet est requis pour générer le PDF.")
        
    if not request.job_title or request.job_title.strip() == "":
        raise HTTPException(status_code=400, detail="Le titre du poste est requis pour générer le PDF.")
        
    if not request.cv_content or request.cv_content.strip() == "":
        raise HTTPException(status_code=400, detail="Le contenu textuel du CV ne peut pas être vide.")
        
    try:
        # 2. Génération du fichier PDF sous forme de flux binaire (en mémoire)
        pdf_file = generate_pdf_from_text(
            fullname=request.fullname,
            job_title=request.job_title,
            cv_content=request.cv_content
        )
        
        # Formatage du nom de fichier propre (remplacement des espaces par des underscores)
        filename = f"CV_{request.fullname.replace(' ', '_')}.pdf"
        
        # 3. Transmission directe du flux binaire téléchargeable au client
        return StreamingResponse(
            pdf_file,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du PDF : {str(e)}")