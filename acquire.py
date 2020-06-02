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

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
"kinverarity1/lasio",
"agile-geoscience/welly",
"akashlevy/Deep-Learn-Oil",
"Flaxbeard/ImmersivePetroleum",
"mutolisp/kh_pplines",
"mycarta/Data-science-tools-petroleum-exploration-and-production",
"GeostatisticsLessons/GeostatisticsLessonsNotebooks",
"f0nzie/rNodal",
"ICHEC/ExSeisDat",
"unifloc/unifloc_vba",
"Petroware/NpdIo",
"f0nzie/rNodal.oilwells",
"WaltXon/pytroleum",
"AnneEstoppey/EasyDataTools",
"ontop/npd-benchmark",
"mwentzWW/petrolpy",
"f0nzie/evolution_data_science_petroleum_engineering",
"f0nzie/vlp-bottomhole-algorithm",
"drceph/petroleumgenerator",
"fluidgeo/fluidgeo-simulator",
"petrocode/blackoilmsv",
"vehagn/tpg4155",
"aegis4048/Petroleum_Engineering",
"vishal-anand-1/Reservoir-recovery-prediction",
"ivarref/bp-diagrams",
"abhishekdbihani/synthetic_well-log_polynomial_regression",
"RaminMoghadasi/compsim",
"stephenjjohnson/PE_functions",
"SumedhaSingh/Petroleum-Price-Prediction-Model",
"samcot/Python-OpenServer",
"pedrolinhares/Turtle-Flow-Simulator",
"jordann124/esx_petroleum",
"ovalles/PyPetroleum",
"Ekeopara-Praise/Petroleum-Engineering",
"duwalanise/reactriot2017-fillmeup",
"danielbarr3ra/Petroleum_Enginering_Codes",
"ishita159/petroleum_review_system",
"manjunath5496/Petroleum-Engineering-Books",
"m2b/API11_1VCF",
"equinor/OpenServer",
"einar90/tpg4162",
"zentechnologygroup/libzen",
"kmcken/PetroThermo",
"rufuspollock/shell-oil-spills-niger-delta",
"oilmap/oilmap",
"swati1024/torrents",
"f0nzie/data_science_ptech",
"simulkade/peteng",
"stackyism/hpcl_support",
"Eshichi/Petroleum",
"salmansust/MachineLearning-TSF-PetroleumProduction",
"ecate/petroleum",
"jcamiloangarita/petrodc",
"gagetyrussell/petroleum_engineering",
"xinyuyao22/Petroleum_consumed",
"swethababurao/BritishPetroleum",
"navjotwarade/National-Petroleum",
"southernstatespetroleum/Southern-States-Petroleum",
"paip/dark-petroleum-atom-syntax",
"theone9807/Forecasting-Price-Petroleum-Products",
"pally-dspet/Petroleum-MachineLearning",
"rezaGIS/OpenPetroleumMVC",
"shwrthy/Petroleum-Engineering-Rock-Mechanics",
"almersawi/IPR",
"liuyibox/ML-aided-Petroleum-Production-Predictor",
"ParthKhanna07/HackFest2k19",
"SEPC/Journal-of-Petroleum-Science-Research",
"hackettma/CIRES-PETRO",
"lasma/epsg",
"kylesarre/Reverse-Auction",
"jimmyneutroon/alfajrsomix",
"anandvaibhav/FormulaDeck",
"Bingohong/PE-DataMining",
"rashidwadani/Decline_Curve_Analysis_Tool",
"MosGeo/BPSMAutoToolbox",
"doneria-anjali/genome",
"huiyi-outsourcing/diagram",
"reallysaurabh/Optimization-Problems",
"AhGhazey/DirectionalWellPlanning",
"dummybigjj/sis",
"EndangeredF1sh/upccrawler",
"EdwaRen/Black-Gold",
"ssicard/well-mapping",
"hellopteromyini/Cutting-edge-technology-RNN-introduction",
"AmDeep/Advanced-Process-Control-Project",
"stchoukeu/transport",
"lehoangha/tomo2d_HeriotWatt",
"softlandia/glasio",
"cjayidoko/AAPG_Hackaton",
"CLIRIK/Grinding-Mill",
"Ahmed-Alhosany/OPA",
"lakhanimanan111/DataAnalysis_SemanticWeb",
"automaticweatherstation/Blog",
"bcgov/mem-mmti",
"lastqxw/petroleum",
"jmarcelogimenez/petroSym",
"VFedyaev/RedPetroleum",
"RancaUpasAbisKardel/PVT",
"GitAsura/petroleum",
"UmarGCPM/Petroleum",
]

# REPOS = [
#     'CLIRIK/Grinding-Mill',
# ]

# REPOS = [
#     "gocodeup/codeup-setup-script",
#     "gocodeup/movies-application",
#     "torvalds/linux",
# ]

def make_repo_list(repos):
    REPOS = repos
    return REPOS


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

# def get_readme_download_url(files: List[Dict[str, str]]) -> str:
#     """
#     Takes in a response from the github api that lists the files in a repo and
#     returns the url that can be used to download the repo's README file.
#     """
#     readme = 'No README'
#     for file in files:
#         if file["name"].lower().startswith("readme"):
#             readme = file["download_url"]
#     return readme

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

def scrape_data_clone(REPOS):
    return [process_repo(repo) for repo in REPOS]


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)