```
public
 |----- repos.py                =定义GitHub仓库及各仓库bug相关标签列表
 |----- commit_crawler.py       =从GitHub根据issue标签爬取bug相关的commit hash
 |----- commit_filter.py        =根据文件后缀名为rs、文件修改行数不超过8这两个标准过滤commit hash，生成改动文件列表(checklists)
 |----- checklists_merge.py     =合并不同来源的改动文件列表(见示意图的箭头颜色)
 |----- checklist_filter.py     =根据非测试代码、非typo修复这两个标准过滤掉checklists中的部分文件
 |----- generate_corpus.py      =根据checklists生成语料库
```

