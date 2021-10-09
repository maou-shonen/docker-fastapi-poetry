from typing import List
import logging, subprocess
from github import Github
from github.ContentFile import ContentFile

DOCKER_REPO = 'q267009886/fastapi-poetry'

logging.basicConfig(format='%(asctime)s [%(levelname)s]%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)

gh = Github()
repo = gh.get_repo('tiangolo/uvicorn-gunicorn-fastapi-docker')
files: List[ContentFile] = repo.get_contents('docker-images')

# filter
tags: List[str] = ['latest']
for file in files:
    if not file.name.lower().endswith('.dockerfile'):
        continue

    tags.append(file.name.rstrip('.dockerfile'))

logging.info(f'tags: {tags}')

# docker build
for tag in tags:
    try:
        subprocess.run(
            'docker build '
            f'-t {DOCKER_REPO}:{tag} '
            f'--build-arg TAG={tag} '
            '.'
        , shell=True).check_returncode()
    except Exception as e:
        logging.exception(f'build fail tag: {tag}')

# docker push
subprocess.run(f'docker push --all-tags {DOCKER_REPO}', shell=True).check_returncode()
