def get_prompt(fullname: str, job_title: str, experience_years: int, skills: str, background: str) -> str:
    prompt = f"""Tu es un expert en recrutement et un rédacteur professionnel de CV (Curriculum Vitae).
Ton but est de rédiger le contenu textuel d'un CV percutant, moderne et optimisé pour les systèmes ATS (logiciels de tri de CV).

[DONNÉES DE L'UTILISATEUR]
- Nom complet : {fullname}
- Poste visé : {job_title}
- Années d'expérience : {experience_years} ans
- Compétences clés : {skills}
- Parcours / Informations : {background}

Rédige le CV en suivant STRICTEMENT cette structure textuelle (utilise des puces claires) :

--- ACCROCHE PROFESSIONNELLE ---
(Un résumé de 3 lignes max, percutant, décrivant le profil et l'objectif de {fullname} pour le poste de {job_title})

--- COMPÉTENCES ---
(Organise les compétences fournies : {skills} et ajoute 2-3 compétences techniques ou soft-skills indispensables pour un {job_title})

--- EXPÉRIENCES PROFESSIONNELLES ---
(Génère 2 exemples d'expériences professionnelles fictives mais ultra-réalistes adaptées au profil. Pour chaque expérience, inclus : un titre de poste, une entreprise fictive, une durée, et 3 puces d'actions/réalisations concrètes avec des verbes d'action)

--- FORMATION ---
(Propose une structure de formation cohérente avec le poste de {job_title})

[CONSIGNE STRICTE]
Réponds uniquement avec le contenu du CV structuré par les balises '---'. Pas d'introduction, pas de 'Voici le CV', pas de commentaires."""

    return prompt