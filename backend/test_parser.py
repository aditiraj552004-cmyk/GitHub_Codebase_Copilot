from parser import read_code_files

repo_path = "../data/sample_repo"

documents = read_code_files(repo_path)

print("Total files:", len(documents))

for document in documents[:5]:
    print("\n----------------------")
    print("File:", document["file_path"])
    print("Language:", document["language"])
    print("Characters:", len(document["content"]))