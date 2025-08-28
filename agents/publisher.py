import os, datetime
from github import Github
from dotenv import load_dotenv

load_dotenv()
GH_TOKEN = os.getenv("GH_TOKEN")
GH_OWNER = os.getenv("GH_OWNER")
GH_REPO  = os.getenv("GH_REPO")
DEFAULT_BRANCH = os.getenv("DEFAULT_BRANCH","main")

def open_pr(path: str, content: str, title: str, body: str = "Automated draft"):
    g = Github(GH_TOKEN)
    repo = g.get_repo(f"{GH_OWNER}/{GH_REPO}")
    base = repo.get_git_ref(f"heads/{DEFAULT_BRANCH}")
    branch = f"ece/{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    repo.create_git_ref(ref=f"refs/heads/{branch}", sha=base.object.sha)

    try:
        existing = repo.get_contents(path, ref=branch)
        repo.update_file(existing.path, f"update {path}", content, existing.sha, branch=branch)
    except Exception:
        repo.create_file(path, f"add {path}", content, branch=branch)

    pr = repo.create_pull(title=title, body=body, head=branch, base=DEFAULT_BRANCH)
    print(f"✅ PR opened: {pr.html_url}")
