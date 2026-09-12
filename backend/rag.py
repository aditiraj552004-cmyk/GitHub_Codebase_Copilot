from vectorstore import search_code
from llm import generate_answer


def answer_question(
    question,
    repository_id
):

    results = search_code(
        question,
        repository_id,
        n_results=5
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    if not documents:

        return (
            "No indexed code was found "
            "for this repository.",
            []
        )

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            f"""
SOURCE FILE:
{metadata['file_path']}

LANGUAGE:
{metadata['language']}

TYPE:
{metadata['type']}

LINES:
{metadata['start_line']}-{metadata['end_line']}

CODE:
{document}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are GitHub Codebase Copilot.

You are an AI software engineering assistant
that analyzes source-code repositories.

Answer the question using ONLY the repository
context supplied below.

Do not invent files, functions, libraries,
features, or architecture that are not visible
in the supplied context.

Explain the answer clearly.

Whenever possible mention:
- relevant files
- functions or classes
- important implementation details
- relationships between components

If the retrieved context is insufficient,
say that clearly.

REPOSITORY CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    answer = generate_answer(
        prompt
    )

    return answer, metadatas