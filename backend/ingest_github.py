from github_loader import (
    clone_github_repo,
    cleanup_repository
)

from parser import read_code_files

from chunker import chunk_code

from vectorstore import (
    add_chunks,
    create_repository_id
)


def ingest_github_repo(repo_url):

    repo_url = repo_url.strip()

    print(
        "\n=============================="
    )

    print(
        "GITHUB REPOSITORY INGESTION"
    )

    print(
        "=============================="
    )

    repository_id = (
        create_repository_id(
            repo_url
        )
    )

    print(
        "Repository ID:",
        repository_id
    )

    repo_path = clone_github_repo(
        repo_url
    )

    try:

        print(
            "\nReading code files..."
        )

        documents = read_code_files(
            repo_path
        )

        print(
            "Files found:",
            len(documents)
        )

        all_chunks = []

        for document in documents:

            print(
                "Processing:",
                document["file_path"],
                document["language"]
            )

            chunks = chunk_code(
                document["content"],
                document["file_path"],
                document["language"]
            )

            all_chunks.extend(
                chunks
            )

        print(
            "\nTotal chunks:",
            len(all_chunks)
        )

        if all_chunks:

            add_chunks(
                all_chunks,
                repository_id
            )

            print(
                "\nRepository successfully "
                "added to ChromaDB."
            )

        else:

            print(
                "\nNo code chunks found."
            )

        return {
            "repository_id":
                repository_id,

            "files":
                len(documents),

            "chunks":
                len(all_chunks)
        }

    finally:

        cleanup_repository(
            repo_path
        )