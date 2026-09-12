import subprocess
import tempfile
import shutil


def clone_github_repo(repo_url):

    temp_dir = tempfile.mkdtemp(
        prefix="github_repo_"
    )

    try:

        print("Cloning repository...")
        print("Repository:", repo_url)

        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                repo_url,
                temp_dir
            ],
            check=True
        )

        print(
            "Repository cloned successfully."
        )

        print(
            "Location:",
            temp_dir
        )

        return temp_dir

    except subprocess.CalledProcessError:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise


def cleanup_repository(repo_path):

    shutil.rmtree(
        repo_path,
        ignore_errors=True
    )