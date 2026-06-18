import requests

HEADERS = {
    "User-Agent": "EnableAI"
}

def github_tool(ai_name, args, username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return(f"{ai_name}: Sorry, there was an error with your request. Try again.")
    
    data = response.json()
    return (
        f"GitHub User: {data['login']}\n"
        f"Name: {data.get('name', 'N/A')}\n"
        f"Public Repos: {data['public_repos']}\n"
    )
