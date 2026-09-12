from chunker import chunk_code


# ------------------------------------------
# Python top-level script
# ------------------------------------------

python_code = """
import cv2

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    cv2.imshow("Camera", frame)
"""


# ------------------------------------------
# JavaScript
# ------------------------------------------

javascript_code = """
const express = require("express");

const app = express();

app.get("/", (req, res) => {
    res.send("Hello World");
});

app.listen(3000);
"""


# ------------------------------------------
# Test Python
# ------------------------------------------

python_chunks = chunk_code(
    python_code,
    "camera.py",
    ".py"
)


print("\n==============================")
print("PYTHON CHUNKS")
print("==============================")


for chunk in python_chunks:

    print(
        "\nName:",
        chunk["name"]
    )

    print(
        "Type:",
        chunk["type"]
    )

    print(
        "Lines:",
        chunk["start_line"],
        "-",
        chunk["end_line"]
    )

    print(chunk["content"])


# ------------------------------------------
# Test JavaScript
# ------------------------------------------

js_chunks = chunk_code(
    javascript_code,
    "server.js",
    ".js"
)


print("\n==============================")
print("JAVASCRIPT CHUNKS")
print("==============================")


for chunk in js_chunks:

    print(
        "\nName:",
        chunk["name"]
    )

    print(
        "Type:",
        chunk["type"]
    )

    print(chunk["content"])