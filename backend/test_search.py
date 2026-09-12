from vectorstore import search_code


repository_id = input(
    "Enter repository ID: "
).strip()


query = input(
    "Ask something about the codebase: "
).strip()


results = search_code(
    query,
    repository_id,
    n_results=5
)


print("\n================================")
print("GITHUB CODEBASE COPILOT")
print("================================")


documents = results.get(
    "documents",
    [[]]
)[0]


metadatas = results.get(
    "metadatas",
    [[]]
)[0]


if not documents:

    print(
        "\nNo relevant code found."
    )


else:

    print(
        f"\nFound {len(documents)} "
        "relevant code chunks."
    )

    for i, document in enumerate(
        documents
    ):

        metadata = metadatas[i]

        print(
            "\n------------------------------"
        )

        print(
            f"Result #{i + 1}"
        )

        print(
            "File:",
            metadata["file_path"]
        )

        print(
            "Language:",
            metadata["language"]
        )

        print(
            "Type:",
            metadata["type"]
        )

        print(
            "Lines:",
            metadata["start_line"],
            "-",
            metadata["end_line"]
        )

        print("\nCode:")

        print(document)