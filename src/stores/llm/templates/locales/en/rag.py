from string import Template

#### RAG PROMPTS ####

#### System ####

system_prompt = Template(
    "You are an assistant to generate a response for the user.\nYou will be provided by a set of docuemnts associated with the user's query.\nYou have to generate a response based on the documents provided.\nIgnore the documents that are not relevant to the user's query.\nYou can applogize to the user if you are not able to generate a response.\nYou have to generate response in the same language as the user's query.\nBe polite and respectful to the user.\nBe precise and concise in your response. Avoid unnecessary information."
)

#### Document ####
document_prompt = Template("## Document No: $doc_num\n### Content: $chunk_text")

#### Footer ####
footer_prompt = Template(
    "Based only on the above documents, please generate an answer for the user.\n## Question:\n$query\n\n## Answer:"
)
