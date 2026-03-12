# Contributing to Global Retail Intelligence Engine

This guide explains how to contribute to the project, whether you're a new collaborator or sharing the repo with teammates.

---

## Contributing from *your* repo into the team repo

**Setup:** You do your work in **your** repo, and you want that work to end up in your colleague’s (team) repo.

| Repo | Role |
|------|------|
| **Your repo** | [https://github.com/frank-asket/global-retail-intelligence-engine](https://github.com/frank-asket/global-retail-intelligence-engine) — where you commit and push your work |
| **Team/colleague repo** | `https://github.com/COLLEAGUE_USERNAME/global-retail-intelligence-engine` — the main project; your changes go there via a Pull Request |

Replace `COLLEAGUE_USERNAME` with your colleague’s GitHub username (or the org that owns the project).

---

### Step 1: Do your work on your repo (your machine)

- Clone or open your repo locally. Your `origin` should point to your repo:
  ```bash
  git remote -v
  # origin  https://github.com/frank-asket/global-retail-intelligence-engine.git (fetch)
  # origin  https://github.com/frank-asket/global-retail-intelligence-engine.git (push)
  ```
- Create a branch, make changes, commit, and push to **your** repo:
  ```bash
  git checkout main
  git pull origin main
  git checkout -b feature/your-feature-name
  # ... edit files ...
  git add .
  git commit -m "Describe your changes"
  git push origin feature/your-feature-name
  ```
- **Why:** All your work lives in your repo on the branch you pushed. The team repo doesn’t see it yet.

---

### Step 2: Add the team repo as a remote (one-time)

- Add your colleague’s repo as a second remote so Git knows where “the team repo” is:
  ```bash
  git remote add upstream https://github.com/COLLEAGUE_USERNAME/global-retail-intelligence-engine.git
  ```
  If `upstream` is already used, pick another name (e.g. `team`) and use it in the next steps instead of `upstream`.
- Check:
  ```bash
  git remote -v
  # origin    https://github.com/frank-asket/global-retail-intelligence-engine.git
  # upstream  https://github.com/COLLEAGUE_USERNAME/global-retail-intelligence-engine.git
  ```
- **Why:** `origin` = your repo, `upstream` = their repo. You push to both from the same local clone.

---

### Step 3: Push your branch to the team repo (if you’re a collaborator)

- If your colleague **added you as a collaborator** on their repo, you can push your branch directly to their repo:
  ```bash
  git push upstream feature/your-feature-name
  ```
- **Why:** Your branch then exists on the team repo, and you’ll open a Pull Request there (Step 4).  
- If you are **not** a collaborator, skip this step and use the fork-style PR in Step 4.

---

### Step 4: Open a Pull Request *into* the team repo

- Go to the **team repo** on GitHub:  
  `https://github.com/COLLEAGUE_USERNAME/global-retail-intelligence-engine`
- **If you pushed to `upstream` (Step 3):**  
  - You’ll see a banner like “Compare & pull request” for your branch. Click it.  
  - Or: **Branches** → your branch → **New pull request**.
- **If you did not push to their repo (fork workflow):**  
  - Go to the team repo → **Pull requests** → **New pull request**.  
  - Click **“compare across forks”**.  
  - Set **base repository** = team repo, **base** = `main`.  
  - Set **head repository** = `frank-asket/global-retail-intelligence-engine`, **compare** = `feature/your-feature-name`.
- Set the PR **base** to the team’s `main`, add a title and description, then create the PR.
- **Why:** The PR is the formal request to merge your branch (from your work on your repo) into the team’s `main`.

---

### Step 5: After the PR is merged

- On your machine, switch back to `main` and pull from the **team** repo so your local `main` matches the project:
  ```bash
  git checkout main
  git pull upstream main
  git push origin main
  ```
- Optionally delete your feature branch locally and on your repo. For the next contribution, create a new branch from this updated `main` and repeat from Step 1.
- **Why:** Keeps your repo and the team repo in sync so the next contribution is based on the latest code.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Get the repository](#2-get-the-repository)
3. [Set up your environment](#3-set-up-your-environment)
4. [Create a branch for your work](#4-create-a-branch-for-your-work)
5. [Make your changes](#5-make-your-changes)
6. [Commit your changes](#6-commit-your-changes)
7. [Push and open a Pull Request](#7-push-and-open-a-pull-request)
8. [After your PR is merged](#8-after-your-pr-is-merged)

---

## 1. Prerequisites

- **Git** installed ([download](https://git-scm.com/downloads))
- **GitHub account** with access to the repository (you need to be added as a collaborator by the repo owner)
- **Python 3.10+** (see [README.md](README.md) for full stack)

**Check Git:**

```bash
git --version
```

**Configure your name and email (one-time):**

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
```

---

## 2. Get the repository

### Option A: You are a collaborator (direct access)

Clone the repo to your machine:

```bash
cd ~/Documents/GitHub   # or wherever you keep projects
git clone https://github.com/OWNER/global-retail-intelligence-engine.git
cd global-retail-intelligence-engine
```

Replace `OWNER` with the GitHub username or organization that owns the repo.

### Option B: You don’t have write access yet

1. **Fork** the repo on GitHub: click **Fork** on the repo page.
2. Clone **your fork**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/global-retail-intelligence-engine.git
   cd global-retail-intelligence-engine
   ```

3. Add the **original repo** as `upstream` (to pull updates later):

   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/global-retail-intelligence-engine.git
   ```

---

## 3. Set up your environment

- Create a virtual environment and install dependencies (see [README.md](README.md)).
- Copy `.env.example` to `.env` if the project uses one, and fill in any required values (do not commit `.env`).

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Create a branch for your work

Always work on a **branch**, not directly on `main`. This keeps `main` stable and makes review easier.

1. Make sure you’re on `main` and up to date:

   ```bash
   git checkout main
   git pull origin main
   ```

2. Create and switch to a new branch with a short, descriptive name:

   ```bash
   git checkout -b feature/your-feature-name
   ```

   Examples: `feature/add-region-filter`, `fix/chat-api-error`, `docs/update-readme`.

---

## 5. Make your changes

- Edit files in your editor.
- Run tests and the app locally to ensure nothing is broken.
- Follow any project conventions (e.g. code style, file structure) mentioned in the README or by the team.

---

## 6. Commit your changes

1. See what changed:

   ```bash
   git status
   git diff
   ```

2. Stage the files you want to commit:

   ```bash
   git add path/to/file.py
   # Or stage everything you changed:
   git add .
   ```

   Avoid staging generated files, `.env`, or unrelated changes. Use `.gitignore` to exclude them.

3. Commit with a clear message:

   ```bash
   git commit -m "Add region filter to product search API"
   ```

   Good messages: short summary, present tense (“Add …”, “Fix …”, “Update …”).

---

## 7. Push and open a Pull Request

1. Push your branch to GitHub:

   ```bash
   git push origin feature/your-feature-name
   ```

   If the branch doesn’t exist on the remote yet, Git may suggest:

   ```bash
   git push -u origin feature/your-feature-name
   ```

2. Open a **Pull Request (PR)**:

   - Go to the repo on GitHub.
   - You’ll usually see a banner: “Compare & pull request” for your branch. Click it.
   - Or: **Branches** → your branch → **New pull request**.

3. In the PR:

   - **Title:** Short summary (e.g. “Add region filter to product search”).
   - **Description:** What you changed and why; how to test it.
   - **Reviewers:** Assign teammates if your workflow uses that.

4. Address **review feedback**: push more commits to the same branch; they will appear in the PR.

5. When a maintainer approves, they will **merge** the PR (often into `main`).

---

## 8. After your PR is merged

1. Switch back to `main` and pull the latest changes:

   ```bash
   git checkout main
   git pull origin main
   ```

2. Delete your local branch (optional):

   ```bash
   git branch -d feature/your-feature-name
   ```

3. For your next contribution, repeat from [step 4](#4-create-a-branch-for-your-work): create a new branch from the updated `main`.

---

## Quick reference

| Step              | Command |
|-------------------|--------|
| Get latest `main` | `git checkout main && git pull origin main` |
| New branch        | `git checkout -b feature/name` |
| Stage changes     | `git add .` or `git add <file>` |
| Commit            | `git commit -m "Message"` |
| Push branch       | `git push origin feature/name` |
| Update branch with `main` | `git checkout main && git pull && git checkout feature/name && git merge main` |

---

## If you use a fork (Option B)

- Push to **your fork**: `git push origin feature/name`.
- Open a PR **from your fork’s branch** to the **original repo’s `main`**.
- To sync your fork with the original repo:

  ```bash
  git fetch upstream
  git checkout main
  git merge upstream/main
  git push origin main
  ```

---

## Questions?

Coordinate with the repo owner for:

- Being added as a collaborator.
- Branch naming conventions (e.g. `feature/`, `fix/`, `docs/`).
- Who reviews and merges PRs.
- Any CI/CD or extra checks before merging.

Happy contributing.
