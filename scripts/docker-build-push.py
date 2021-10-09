from typing import List
import subprocess
from github import Github
from github.ContentFile import ContentFile

DOCKER_REPO = 'q267009886/fastapi-poetry'

github_user = 'tiangolo'
github_repo = 'uvicorn-gunicorn-fastapi-docker'
github_branch = 'master'

gh = Github()
repo = gh.get_repo('tiangolo/uvicorn-gunicorn-fastapi-docker')
files: List[ContentFile] = repo.get_contents('docker-images')

# filter
tags: List[str] = ['latest']
for file in files:
    if not file.name.lower().endswith('.dockerfile'):
        continue

    tags.append(file.name.rstrip('.dockerfile'))

print('tags:', tags)

# docker login
# subprocess.run('echo "$DOCKER_PASS" | docker login --username $DOCKER_USER --password-stdin', shell=True).check_returncode()

# docker build
for tag in tags:
    subprocess.run(
        'docker build '
        f'-t {DOCKER_REPO}:{tag} '
        f'--build-arg TAG={tag} '
        '.'
    , shell=True).check_returncode()

# docker push
subprocess.run('docker push --all-tags', shell=True).check_returncode()
