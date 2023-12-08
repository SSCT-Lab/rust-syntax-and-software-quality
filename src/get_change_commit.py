import subprocess

repo_list = [
    "AleoHQ/snarkOS",
    "AleoHQ/snarkVM",
    """
    "zellij-org/zellij",
    "yewstack/yew",
    "AppFlowy-IO/AppFlowy",
    "bytecodealliance/wasmtime",
    "datafuselabs/databend",
    "foundry-rs/foundry",
    "gfx-rs/gfx",
    "helix-editor/helix",
    """
    "MaterializeInc/materialize",
    "meilisearch/meilisearch",
    "pola-rs/polars",
    "surrealdb/surrealdb",
    "swc-project/swc",
    "rust-lang/rust-clippy",
    "extrawurst/gitui",
    "FuelLabs/fuels-rs",
]

def get_change_commits(repo_path):
    # 切换到仓库目录
    #subprocess.run(['git', 'checkout', repo_path])

    # 获取所有提交的哈希值
    commit_hashes = subprocess.check_output(["git", "-C", repo_path, 'log', '--format=%H']).decode('utf-8', errors='ignore').splitlines()
    print(len(commit_hashes))
    #change_commits = []
    change_commits = 0
    # 遍历每个提交
    for commit_hash in commit_hashes:
        # 获取提交的diff
        try:
            # Attempt to execute the Git command
            diff_lines = subprocess.check_output(['git', '-C', repo_path, 'diff', commit_hash + '^', commit_hash], stderr=subprocess.STDOUT).decode('utf-8', errors='ignore').splitlines()
            
            # ... (rest of your script)
        except subprocess.CalledProcessError as e:
            # Print the error output
            #print(f"Error executing Git command: {e.output.decode('utf-8', errors='ignore')}")
            a = 1
         # 检查是否有 .rs 文件的前一行有 '-' 后一行有 '+' 修改
        # print(diff_lines)
        rs_file_changed = False
        for i in range(1, len(diff_lines)):
            if diff_lines[i].startswith(('+++', '---')):
                rs_file_changed = diff_lines[i].endswith('.rs')
            elif rs_file_changed and diff_lines[i-1].startswith('-') and diff_lines[i].startswith('+'):
                change_commits = change_commits + 1
                #print(diff_lines[i - 1],"\n", diff_lines[i])
                break  # 只要检测到一个 change commit，就跳出循环

    return change_commits
#exit(0)

    return change_commits

if __name__ == "__main__":
    # 请替换为你的本地仓库路径
    repo_path = "./cloned-repos/"
    for repo_name in repo_list:
      change_commits = get_change_commits(repo_path + repo_name)
      print(f"Change Commits Num of {repo_name} is {change_commits}")
    #for commit in change_commits:
    #    print(commit)