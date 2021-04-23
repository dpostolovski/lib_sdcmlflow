import requests
import os
class Github:
    def add_comment_in_pr(self, pr, message):
        return requests.post(f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/issues/{pr}/comments",
                                 headers={"Accept": "application/vnd.github.v3+json",
                                          "Authorization": f"token {os.environ['GITHUB_TOKEN']}"},
                                 json={"body": message}
        )