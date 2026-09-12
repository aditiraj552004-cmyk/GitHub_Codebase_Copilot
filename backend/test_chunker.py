from parser import read_code_files
from chunker import chunk_python_code


repo_path = "../data/sample_repo"

documents = read_code_files(repo_path)

all_chunks = []

for document in documents:

    if document["language"] == ".py":

        chunks = chunk_python_code(
            document["content"],
            document["file_path"]
        )

        all_chunks.extend(chunks)


print("Total chunks:", len(all_chunks))


for chunk in all_chunks:

    print("\n==============================")

    print("File:", chunk["file_path"])
    print("Name:", chunk["name"])
    print("Type:", chunk["type"])
    print(
        "Lines:",
        chunk["start_line"],
        "-",
        chunk["end_line"]
    )

    print("\nCode:")
    print(chunk["content"])
    