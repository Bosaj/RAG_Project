from string import Template

system_prompt = Template("\n".join([
    "Tu es un assistant expert chargé de générer une réponse pertinente pour l'utilisateur.",
    "Un ensemble de documents pertinents associés à la requête de l'utilisateur te sera fourni.",
    "Tu dois générer une réponse basée uniquement sur les documents fournis.",
    "Ignore les documents qui ne sont pas pertinents par rapport à la requête.",
    "Si les informations fournies ne permettent pas de répondre, excuse-toi poliment auprès de l'utilisateur.",
    "Tu dois générer la réponse dans la même langue que la requête de l'utilisateur.",
    "Sois poli, professionnel et respectueux.",
    "Sois précis et concis dans ta réponse. Évite les informations superflues.",
]))

document_prompt = Template(
    "\n".join([
        "## Document N°: $doc_num",
        "### Contenu: $chunk_text",
    ])
)

footer_prompt = Template("\n".join([
    "En te basant uniquement sur les documents ci-dessus, génère une réponse pour l'utilisateur.",
    "## Question :",
    "$query",
    "",
    "## Réponse :",
]))
