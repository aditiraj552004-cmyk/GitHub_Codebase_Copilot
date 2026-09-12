import hashlib
import re

import chromadb

from sentence_transformers import (
    SentenceTransformer
)


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


client = chromadb.PersistentClient(
    path="../data/chroma_db"
)


def normalize_repo_url(repo_url):

    repo_url = repo_url.strip()

    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]

    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]

    return repo_url.lower()


def create_repository_id(repo_url):

    normalized_url = normalize_repo_url(
        repo_url
    )

    return hashlib.md5(
        normalized_url.encode("utf-8")
    ).hexdigest()[:12]


def get_collection(repository_id):

    repository_id = repository_id.strip()

    repository_id = re.sub(
        r"[^a-zA-Z0-9_-]",
        "",
        repository_id
    )

    collection_name = (
        f"repo_{repository_id}"
    )

    return client.get_or_create_collection(
        name=collection_name
    )


def add_chunks(
    chunks,
    repository_id
):

    if not chunks:

        print("No chunks to add.")
        return

    collection = get_collection(
        repository_id
    )

    documents = []
    metadatas = []
    ids = []

    for index, chunk in enumerate(chunks):

        documents.append(
            chunk["content"]
        )

        metadatas.append({
            "file_path":
                chunk["file_path"],

            "name":
                chunk["name"],

            "type":
                chunk["type"],

            "start_line":
                chunk["start_line"],

            "end_line":
                chunk["end_line"],

            "language":
                chunk["language"],

            "repository_id":
                repository_id
        })

        raw_id = (
            f"{repository_id}_"
            f"{chunk['file_path']}_"
            f"{chunk['name']}_"
            f"{index}"
        )

        safe_id = hashlib.md5(
            raw_id.encode("utf-8")
        ).hexdigest()

        ids.append(
            safe_id
        )

    embeddings = (
        embedding_model
        .encode(documents)
        .tolist()
    )

    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(
        f"Added/updated {len(chunks)} "
        f"chunks in repository "
        f"{repository_id}."
    )


def search_code(
    query,
    repository_id,
    n_results=5
):

    collection = get_collection(
        repository_id
    )

    total_chunks = (
        collection.count()
    )

    if total_chunks == 0:

        return {
            "documents": [[]],
            "metadatas": [[]]
        }

    n_results = min(
        n_results,
        total_chunks
    )

    query_embedding = (
        embedding_model
        .encode([query])
        .tolist()
    )

    return collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )