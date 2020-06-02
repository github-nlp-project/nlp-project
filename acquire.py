"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from env import github_token, github_username
import time

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.


def get_repo_names(url):
    headers = {'User-Agent': 'manual search'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    repos = []
    for i in range(10):
        repos.append(soup.find_all('a', class_='v-align-middle')\
                 [i].text)
        time.sleep(.8)
    return repos


def acquire_repo_list(category):
    '''
    This is what to run to create a json file. It should
    be run once for every category you want to look at.
    '''
    f_category = category
    if (' ') in category:
        category = category.replace(' ','_')
        f_category = category.replace(' ','+')
    
    urls = [f'https://github.com/search?o=desc&p={i}\
    &q={f_category}+size:>100&s=stars&type=Repositories'\
    for i in range(1,11)]

    test = []
    for url in urls:
        test += get_repo_names(url)
        
    if not os.path.isfile(f'{category}.json'):  
        json.dump(test, open(f"{category}_repos.json", "w"),
                  indent=1)
    status = f'You now have a json file named {category}_repos.json.'
    return status


"""This runs to create a full list of repos of every category you 
searched for to scrape later"""
full_list = []
for file in os.listdir():
    if 'repos.json' in file:
        full_list.append(file)
item_list = []
for item in full_list:
    lm = pd.read_json(item)
    item_list += (list(lm[0]))
REPOS = item_list


headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme = get_readme_download_url(contents)
    if readme == '':
        readme_contents = 'No README'
    else:
        readme_contents = requests.get(readme).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)