import subprocess
import tempfile
import os

base_dict = './cloned-repos/'
repo_list = ["egui"]
repo_dict = {
  "egui" : "emilk/egui",
}

def get_commit_changes(commit_hash, repo):
    # 获取改动前后的文件列表
    files_changed = subprocess.check_output(['git', '-C', f'{base_dict + repo_dict[repo]}', 'diff', f'{commit_hash}^', commit_hash, '--name-only'], text=True).splitlines()

    return files_changed

def save_before_after_content_to_temp_files(files_changed, commit_hash, repo):
    temp_files = {}

    for file_name in files_changed:
        # 获取改动前的文件内容
        before_content = subprocess.check_output(['git', '-C', f'{base_dict + repo_dict[repo]}', 'show', f'{commit_hash}^:{file_name}'], text=True)

        # 获取改动后的文件内容
        after_content = subprocess.check_output(['git', '-C', f'{base_dict + repo_dict[repo]}', 'show', f'{commit_hash}:{file_name}'], text=True)

        # 创建临时文件
        temp_file_before = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp_file_after = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        # 更新 (文件名, 临时文件名) 键值对
        temp_files.update({file_name : [temp_file_before.name, temp_file_after.name]})
        
        # 写入改动前和改动后的文件内容
        with open(temp_file_before.name, 'w') as f_before:
            f_before.write(before_content)

        with open(temp_file_after.name, 'w') as f_after:
            f_after.write(after_content)

    return temp_files

def get_map(file):
  result_dict = {}
  for line in file:
    # 提取行号和对应的zero-indexed值
    line_number = int(line.split(':')[0])
    zero_indexed_values = [int(value.split(' ')[1].split()[0]) for value in line.split('LineNumber:')[1:]]
    # 将解析的结果添加到字典中
    result_dict[line_number] = zero_indexed_values
      
  return result_dict

def get_list(res):
  numbers_list = []
  for line in res:
      # Remove double quotes and then convert to integer
    number = int(line.strip('"\n'))
    numbers_list.append(number)


  # 打印列表
  print(numbers_list)
  return numbers_list

def get_addition(file1, file2):
  res = subprocess.check_output(['./difft', '--get-addtions', file1, file2], text=True).splitlines()
  return get_list(res)

def get_deletion(file1, file2):
  res = subprocess.check_output(['./difft', '--get-deletions', file1, file2], text=True).splitlines()
  return get_list(res)

def get_line_map(file1, file2):
  print(file1, file2)
  res = subprocess.check_output(['./difft', '--get_line_map', file1, file2], text=True).splitlines()
  if res[1] == 'No changes.':
    return {}
  return get_map(res)

def git_rev_list(commit, file_path, repo):
    command = ['git', '-C', f'{base_dict + repo_dict[repo]}', 'rev-list', commit, '--', file_path]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        commit_hashes = result.stdout.strip().split('\n')
        return commit_hashes
    else:
        print(f"Error: {result.stderr}")
        return None

# 返回两个列表是否有交集
def is_intersection(a : list, b : list):
  print(a,"\n", b)
  for itema in a:
    for itemb in b:
      if itema == itemb:
        return  True
      
  return False

# 前后版本文件列表，以及相应文件的deletions和additions
def has_intersection(file1, file2, deletions, additions):
  obj = []
  line_map : dict = get_line_map(file1, file2)
  
  for line in additions:
    if line_map.get(line) != None:
      obj.extend(line_map.get(line))
  
  if is_intersection(obj, deletions):
    return True
  
  return False

def get_bug_introduce_commits(bug_fix_commits, repo):
  fix_introduce_map = {}
  # 这里写入你的主要代码逻辑
  for bug_fix_commit in bug_fix_commits:
    # 修bug改动的文件
    introducing_commits = []
    bug_fix_files : dict = save_before_after_content_to_temp_files(get_commit_changes(bug_fix_commit, repo), bug_fix_commit , repo)
    
    for file_name in bug_fix_files.keys():
      # 获取改动过当前文件的commit，验证是否有交叉，如果有，则证明是引入bug的commit
      bug_introducing_commits : list = git_rev_list(bug_fix_commit, file_name, repo)
      for bug_introducing_commit in bug_introducing_commits:
        # assert(not empty)
        bug_introducing_file = save_before_after_content_to_temp_files([file_name], bug_introducing_commit ,repo)[file_name]
        print(f"{bug_fix_files[file_name][0]}, {bug_fix_files[file_name][1]}")
        deletion = get_deletion(bug_fix_files[file_name][0], bug_fix_files[file_name][1])
        print(f"{bug_introducing_file[0]}, {bug_introducing_file[1]}")
        addition = get_addition(bug_introducing_file[0], bug_introducing_file[1])
        if has_intersection(bug_fix_files[file_name][0], bug_introducing_file[1], deletion, addition):
          print(True)
          introducing_commits.append(bug_introducing_commit)
        else:
          print(False)
    
    fix_introduce_map.update({bug_fix_commit: introducing_commits})
  #print(fix_introduce_map)
  return fix_introduce_map

def generate_bug_introducing(repo):
  dir_name = "./results/corpus"
  with os.scandir(dir_name) as entries:
    for entry in entries:
      with os.scandir(os.path.join(dir_name, entry.name)) as corpus:
        for corpu in corpus:
          with os.scandir(os.path.join(dir_name, entry.name, corpu.name) ) as commits:
            bug_fix_commits = []
            for commit in commits:
              bug_fix_commits.append(commit.name)
            ret_map = get_bug_introduce_commits(bug_fix_commits, corpu.name)
            ##print(ret_map)       

if __name__ == "__main__":
    for repo in repo_list:
      generate_bug_introducing(repo)
