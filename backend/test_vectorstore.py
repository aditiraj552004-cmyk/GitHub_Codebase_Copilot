from parser import read_code_files
from chunker import chunk_python_code
from vectorstore import add_chunks


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


add_chunks(all_chunks)