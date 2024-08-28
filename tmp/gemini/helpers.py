import subprocess

def get_git_commits(git_dir, num_commits=5):
    # Command to get the last 'num_commits' commits with their hash, author, date, and message
    command = f'git log -n {num_commits} --pretty=format:"%H;%an;%ad;%s" --date=iso'

    try:
        # Execute the command in the context of the specified .git directory
        result = subprocess.check_output(command, shell=True, cwd=git_dir).decode('utf-8').strip()
        commits = result.split('\n')
        commit_list = []

        for commit in commits:
            hash, author, date, message = commit.split(';', 3)
            commit_list.append({
                'hash': hash,
                'author': author,
                'date': date,
                'message': message
            })

        return commit_list
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None
