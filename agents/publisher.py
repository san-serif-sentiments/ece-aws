import os, subprocess, datetime, shlex

GH_OWNER = os.getenv("GH_OWNER", "san-serif-sentiments")
GH_REPO  = os.getenv("GH_REPO",  "ece-aws")
DEFAULT_BRANCH = os.getenv("DEFAULT_BRANCH","main")

def run(cmd, cwd=None, check=True):
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed ({cmd}):\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
    return res.stdout.strip()

def open_pr(path:str, content:str, title:str, body:str="Automated draft"):
    repo_dir = os.getcwd()

    # write/update file
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    # git identity
    run('git config user.name "Shailesh Rawat"')
    run('git config user.email "shailesh.rawat1403@gmail.com"')

    # sync main
    run("git fetch origin")
    run(f"git checkout {DEFAULT_BRANCH}")
    run(f"git pull origin {DEFAULT_BRANCH}")

    # new branch
    branch = "ece/" + datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    run(f"git checkout -b {branch}")

    # stage everything (so we never miss generated files)
    run("git add -A")

    # commit only if there are staged changes
    staged_dirty = subprocess.run("git diff --cached --quiet", shell=True)
    if staged_dirty.returncode != 0:
        run(f'git commit -m {shlex.quote(f"add or update {path}")}')
    # else: nothing to commit; proceed

    # push via SSH
    run(f"git push -u origin {branch}")

    # if a PR already exists, show it; else create one
    view = run("gh pr view --json url --jq .url", check=False)
    if not view:
        pr_url = run(f'gh pr create --title {shlex.quote(title)} --body {shlex.quote(body)} --base {DEFAULT_BRANCH} --head {branch}')
    else:
        pr_url = view

    print(f"✅ PR opened: {pr_url}")
