from fastapi import APIRouter, Response, Depends, HTTPException, status, Query
from fastapi import Request, Header
from app.service import git_service
import json
from dotenv import load_dotenv
import os
import httpx
from app.service.agent_service import AgentService
from fastapi import BackgroundTasks

router = APIRouter(prefix='', tags=["app_routes"])

@router.post("/gh-webhook", status_code=status.HTTP_200_OK)
async def receive_webhook(
    response: Response,
    x_github_event: str = Header(..., alias="X-GitHub-Event"),
    request: Request = None
):
    """
    Receive GitHub webhook events.
    """
    if git_service.get_event_name(x_github_event) != 'pull_request':
        raise HTTPException(
            status_code=status.HTTP2,
            detail="This endpoint only handles pull request events."
        )
    """ payload = request.json()

    background_tasks = BackgroundTasks()
    background_tasks.add_task(AgentService.process_webhook, payload , AgentService(), git_service)
    return {"message": "Processing started"} """
    payload = await request.json()
    agent_service = AgentService()
    url = f'{payload['pull_request']['url']}/files'
    diff = await git_service.get_diff(payload['pull_request']['url'])
    commit_id = payload['pull_request']['head']['sha']
    review = await agent_service.get_pr_review(diff)
    comments = []
    for suggestion in json.loads(review):
        for comment in suggestion['suggested_change']:
            comments.append({
                'body': f' **Criticality: {comment['criticality']}**\n\n> {comment['comment_message']}\n\n```python\n{comment['code_suggestion']}\n```',
                'commit_id': suggestion['sha'],
                'path': suggestion['filename'],
                'commit_id': commit_id,
                'line': comment['comment_metadata']['line'],
                'side': comment['comment_metadata']['side'],    
            })
 
    for comment in comments:
        await git_service.create_comment(payload['pull_request']['url'], comment)
        
    return {"message": "Webhook received successfully", "event": x_github_event, "comments": comments}