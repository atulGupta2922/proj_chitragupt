from github import Github
from fastapi import HTTPException
import httpx
import os, json
from dotenv import load_dotenv

def get_event_name(event: str) -> str:
    event_name = event.split('/')[-1]
    return event_name

def get_pull_request():
    GITHUB_API_ACESS_TOKEN = os.getenv('GITHUB_API_ACESS_TOKEN')
    g = Github(GITHUB_API_ACESS_TOKEN)
    pr = g.get_repo('atulGupta2922/tex2sql').get_pull(2)
    return pr

async def get_diff(pr_url):
    load_dotenv()
    GITHUB_ACESS_TOKEN = os.getenv('GITHUB_API_ACESS_TOKEN')
    url = f'{pr_url}/files'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f'Bearer {GITHUB_ACESS_TOKEN}',
        "X-GitHub-Api-Version": "2022-11-28"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch PR diff: {e}")
        
async def create_comment(pr_url, body):
    load_dotenv()
    GITHUB_ACESS_TOKEN = os.getenv('GITHUB_API_ACESS_TOKEN')
    url = f'{pr_url}/comments'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f'Bearer {GITHUB_ACESS_TOKEN}',
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=body, headers=headers)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to create review comment: {e}")