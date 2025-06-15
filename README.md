# proj_chitragupt
An AI PR reviewer


## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
    - Windows: `venv\Scripts\activate`
    - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

## Configuration

* Create a `.env` by copying and renaming `.env-example` file in the root directory.

## `.env` Credentials
* `AI_MODEL_NAME` : API key from your AI model (eg. Anthropic, OpenAI, etc) 
* `AI_MODEL_API_KEY` : Name of the mdoel (eg. `claude-sonnet-4-20250514`)
* `GIT_WEBHOOK_SECRET` : Github webhook secret (this is secret you can create as you like to provide it as a secret while setting up github webhook on github)
* `GITHUB_API_ACESS_TOKEN` : Github API access token, refer [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens){:target="_blank"}.
* `GIT_REPO_NAME` : eg. `owner_name/repository_name`
