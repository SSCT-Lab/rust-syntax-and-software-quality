import requests
import json
def get_issue_development_pr(owner, repo, issue_number, github_token):
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.mockingbird-preview"
    }

    # 获取 Issue 的时间线信息
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/timeline"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        timeline_events = response.json()

        # 筛选与 development PR 相关的事件
        development_pr_events = [
            event["event"]["commit_id"]
            for event in timeline_events
            if "event" in event and "commit_id" in event["event"]
        ]

        # 打印关联的 development PR 信息
        if development_pr_events:
            for commit_id in development_pr_events:
                print(f"Commit ID: {commit_id}")
        else:
            print("No development PR events found for this issue.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

# 示例：获取 GitHub Issue #123 相关的 development PR
owner = "AleoHQ"
repo = "snarkOS"
issue_number = 2102
token = "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"
get_issue_development_pr(owner, repo, issue_number, token)
