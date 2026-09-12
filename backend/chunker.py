import ast


def chunk_generic_code(
    content,
    file_path,
    language,
    chunk_size=50
):

    chunks = []

    lines = content.splitlines()

    if not lines:
        return chunks

    for start in range(
        0,
        len(lines),
        chunk_size
    ):

        end = min(
            start + chunk_size,
            len(lines)
        )

        code = "\n".join(
            lines[start:end]
        )

        if not code.strip():
            continue

        chunk_number = (
            start // chunk_size
        ) + 1

        chunks.append({
            "content": code,
            "file_path": file_path,
            "name":
                f"{file_path}_chunk_{chunk_number}",
            "type": "code_block",
            "start_line": start + 1,
            "end_line": end,
            "language": language
        })

    return chunks


def chunk_python_code(
    content,
    file_path
):

    chunks = []

    try:

        tree = ast.parse(content)

    except SyntaxError:

        return chunk_generic_code(
            content,
            file_path,
            ".py"
        )

    lines = content.splitlines()

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef
            )
        ):

            start_line = node.lineno

            end_line = getattr(
                node,
                "end_lineno",
                start_line
            )

            code = "\n".join(
                lines[start_line - 1:end_line]
            )

            chunks.append({
                "content": code,
                "file_path": file_path,
                "name": node.name,
                "type": type(node).__name__,
                "start_line": start_line,
                "end_line": end_line,
                "language": ".py"
            })

    # Python scripts that contain only
    # top-level code still need indexing
    if not chunks:

        return chunk_generic_code(
            content,
            file_path,
            ".py"
        )

    return chunks


def chunk_code(
    content,
    file_path,
    language
):

    if language == ".py":

        return chunk_python_code(
            content,
            file_path
        )

    return chunk_generic_code(
        content,
        file_path,
        language
    )