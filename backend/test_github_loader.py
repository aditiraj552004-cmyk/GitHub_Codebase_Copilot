from github_loader import clone_github_repo


repo_url = input("Enter GitHub repository URL: ")

repo_path = clone_github_repo(repo_url)

print("\nRepository path:")
print(repo_path)