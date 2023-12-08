import os
import subprocess
import shutil



commits_path = "results/commits"
ans = []

for p in os.listdir(commits_path):
  repo = p.split(".txt")[0]
  with open(os.path.join(commits_path, p)) as f:
    items = [eval(line) for line in f.read().strip().split("\n") if line != ""]
  ans.append((p, items))
  
ans.sort(key = lambda x:len(x[1]))

for a in ans:
  print(a[0], len(a[1]))