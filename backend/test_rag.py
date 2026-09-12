from rag import answer_question


repository_id = input(
    "Enter repository ID: "
).strip()


question = input(
    "Ask a question about the codebase: "
).strip()


answer, sources = answer_question(
    question,
    repository_id
)


print("\n================================")
print("GITHUB CODEBASE COPILOT")
print("================================")


print("\nAnswer:")

print(answer)


print("\nSources:")


for source in sources:

    print(
        f"- {source['file_path']} "
        f"Lines "
        f"{source['start_line']}-"
        f"{source['end_line']}"
    )
    