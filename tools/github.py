import requests

HEADERS = {
    "User-Agent": "EnableAI"
}

def github_tool(ai_name, user_name, username):
    if not username or not username.strip():
        return f"{ai_name}: Usage: /github <username>"
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return(f"{ai_name}: Sorry, there was an error with your request. Try again.")
    
    data = response.json()
    return (
        f"GitHub User: {data.get('login', 'N/A')}\n"
        f"Name: {data.get('name', 'N/A')}\n"
        f"Public Repos: {data.get('public_repos', 'N/A')}\n"
    )
