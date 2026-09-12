import os


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".html",
    ".css",
    ".json",
    ".md",
    ".sql",
    ".yaml",
    ".yml",
}


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
}


def read_code_files(repo_path):

    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRECTORIES
        ]

        for file in files:

            extension = os.path.splitext(file)[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content = f.read()

                relative_path = os.path.relpath(
                    file_path,
                    repo_path
                )

                documents.append({
                    "content": content,
                    "file_path": relative_path,
                    "language": extension
                })

            except Exception as e:

                print(
                    f"Could not read "
                    f"{file_path}: {e}"
                )

    return documents