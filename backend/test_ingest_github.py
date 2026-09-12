from ingest_github import ingest_github_repo


repo_url = input("Enter GitHub repository URL: ")

result = ingest_github_repo(repo_url)

print("\n==============================")
print("INGESTION COMPLETE")
print("==============================")

print("Repository:", result["repo_path"])
print("Files:", result["files"])
print("Chunks:", result["chunks"])