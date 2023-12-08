import os
import re
import subprocess
from enum import Enum
repo_dict = {
    "egui" : "emilk/egui",
    "meilisearch": "meilisearch/meilisearch",
    "rust-analyzer": "rust-lang/rust-analyzer",
    "snarkOS" : "AleoHQ/snarkOS",
    "tikv": "tikv/tikv",
    "tokio": "tokio-rs/tokio",
}

class State(Enum):
    EMPTY = 0,
    TESTFILE = 1,
    TESTMOD = 2,
    TESTFUNC = 3,

def get_diff_content(diff_content):
    #print(diff_content)

    # Split the diff into lines
    diff_lines = diff_content.split('\n')

    # Flag to indicate whether we are currently inside a test function block
    added_lines = 0
    deleted_lines = 0
    
    state = State.EMPTY
    # Iterate through the lines of the diff
    for x in diff_lines:
        line : str = x
        # Check if the line matches the test function pattern
        # 文件首行
        if line.startswith("diff --git"):
            if line.find("test") != -1:
                state = State.TESTFILE
        elif line.startswith("@@"):
            if line.find("mod test") != -1 or (line.find("test") != -1 and line.find("fn") != -1): 
                print(line)
                state = State.TESTMOD
            else:
                state = State.EMPTY
        else:
            if state == State.TESTMOD:
                if line.startswith("+"):
                    added_lines = added_lines + 1
                elif line.startswith('-'):
                    deleted_lines = deleted_lines + 1    
    #print(added_lines)
    #print(deleted_lines)
    return added_lines, deleted_lines

def get_test_changes(commit_sha, repo_path):
    # Run git diff command
    print(commit_sha)
    git_show_cmd = f'git -C {repo_path} diff {commit_sha}^ {commit_sha} -- "*.rs"'
    file_content = subprocess.check_output(git_show_cmd, shell=True, text=True)
    ##print(file_content)
    return get_diff_content(file_content)


if __name__ == "__main__":
    dir_name = "./results/corpus"
    with os.scandir(dir_name) as entries:
        for entry in entries:
            with os.scandir(os.path.join(dir_name, entry.name)) as corpus:
                for corpu in corpus:
                    with os.scandir(os.path.join(dir_name, entry.name, corpu.name) ) as commits:
                        for commit in commits:
                            #print(os.path.join(dir_name, entry.name, corpu.name, commit.name))
                            print(corpu.name, " ", commit.name)
                            added_lines, deleted_lines = get_test_changes(commit.name, "cloned-repos/" + repo_dict.get(corpu.name))
                            print(added_lines, deleted_lines)
                            file = open(os.path.join(dir_name, entry.name, corpu.name, commit.name, "class.txt"), 'w')
                            file.write(str(deleted_lines))
                            file.write(" ")
                            file.write(str(added_lines))
                            #exit(0)

    
    commit_sha = "5a9d8fa"
    #added_lines, deleted_lines = get_test_changes(commit_sha)

    #print(f"Added test lines: {added_lines}")
    #print(f"Deleted test lines: {deleted_lines}")
