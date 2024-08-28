import subprocess
import os
from helpers import get_git_commits
import sqlite3

con = sqlite3.connect("tutorial.db")

def execute_commands(repo_path, project, commit_hash, destination_base_folder):
    """Executes the specified shell commands."""

    # Change to the repository directory
    os.chdir(f"{repo_path}/{project}")

    # Perform git checkout
    checkout_command = f"git checkout -f {commit_hash}"
    try:
        subprocess.run(checkout_command, shell=True, check=True)
        print(f"Successfully checked out commit {commit_hash}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking out commit: {e}")
        return

    str_excludes = ("--exclude=build --exclude=__pycache__ --exclude=.pytest_cache --exclude=.idea --exclude=vendor "
                    "--exclude=var --exclude=tmp --exclude='*.sql' ")
    commands = [
        f"cd {repo_path} && tar {str_excludes} -czf source.tar.gz {project}",
        f"mkdir {destination_base_folder}/{project}",
        f"rm -rf {destination_base_folder}/{project}/{commit_hash}",
        f"mkdir {destination_base_folder}/{project}/{commit_hash}",
        f"chmod 777 -R {destination_base_folder}",
        f"cd {repo_path} && tar -xzf source.tar.gz -C {destination_base_folder}/{project}/{commit_hash} --strip-components=1",
        f"cd {repo_path} && rm -rf source.tar.gz",
    ]

    for command in commands:
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print(f"Command '{command}' executed successfully.")
            # Optionally print the output for debugging
            # print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command '{command}': {e.stderr}")

    # Return the main branch
    checkout_command = f"git checkout -f main"
    try:
        subprocess.run(checkout_command, shell=True, check=True)
        print(f"Successfully checked out commit main")
    except subprocess.CalledProcessError as e:
        print(f"Error checking out commit: {e}")
        return


if __name__ == "__main__":
    #base_dir = os.getcwd()
    base_dir = "/api/tmp/gemini"
    repo_path = base_dir + '/repos'
    project = 'text-2-query'
    destination_base_folder = base_dir + '/storage'

    git_dir = f"{repo_path}/{project}"
    commits = get_git_commits(git_dir, num_commits=5)

    for commit in commits:
        commit_hash = commit.get('hash')
        execute_commands(repo_path, project, commit_hash, destination_base_folder)



