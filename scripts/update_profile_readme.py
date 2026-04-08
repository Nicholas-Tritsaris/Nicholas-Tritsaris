import os
from github import Github
from datetime import datetime

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "Nicholas-Tritsaris"
TOP_N = 10
README_PATH = "README.md"

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set. Exiting.")

g = Github(GITHUB_TOKEN)
user = g.get_user(USERNAME)
repos = user.get_repos()

# Sort by latest pushed_at (most recent commit)
repos_sorted = sorted(repos, key=lambda r: r.pushed_at, reverse=True)
top_repos = repos_sorted[:TOP_N]

# Generate project list Markdown
project_lines = []
for repo in top_repos:
    repo_name = repo.name
    repo_desc = repo.description or "No description provided."
    project_lines.append(f"- **🔗 {repo_name}** — {repo_desc}")

projects_section = "## Projects Currently Working On\n\n" + "\n".join(project_lines) + "\n\n"

# Read current README
with open(README_PATH, "r", encoding="utf-8") as f:
    readme_lines = f.read()

# Replace old Featured Projects / Projects Currently Working On section
import re
pattern = r"## Projects Currently Working On.*?(?=(\n## |\Z))|## Featured Projects.*?(?=(\n## |\Z))"
new_readme = re.sub(pattern, projects_section, readme_lines, flags=re.DOTALL)

# Programming Languages Section (live tile style using shields.io)
# Collect languages for top repos
lang_counts = {}
for repo in top_repos:
    for lang, count in repo.get_languages().items():
        lang_counts[lang] = lang_counts.get(lang, 0) + count

# Sort languages by usage
sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
lang_shields = " ".join([f"![{lang}](https://img.shields.io/badge/-{lang}-blue?style=flat-square)" for lang, _ in sorted_langs])
languages_section = "## Programming Languages Used\n\n" + lang_shields + "\n\n"

# Insert programming languages section after Projects section
new_readme = new_readme.replace(projects_section, projects_section + languages_section)

# Write updated README
with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README.md updated successfully with top 10 projects and language badges.")