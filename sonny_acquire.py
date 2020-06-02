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
    "lucaseustaquio/ams-2013-2014-solar-energy",
    "renewables-ninja/gsee",
    "ColasGael/Machine-Learning-for-Solar-Energy-Prediction",
    "owenzhang/kaggle_AMS_2013_14_solar",
    "meltaxa/solariot",
    "3KUdelta/Solar_WiFi_Weather_Station",
    "zygmuntz/kaggle-solar",
    "SolarTherm/SolarTherm",
    "iat-cener/tonatiuh",
    "aladdine/Essential-Solar-Energy-and-Storage-Software-Resources",
    "abdullah2891/solar_energy_calculator",
    "CynthiaKoopman/Forecasting-Solar-Energy",
    "djgagne/solar_energy_prediction_contest",
    "CodeForFoco/solar-scorecard",
    "openpvtools/openpvtools",
    "glouppe/kaggle-solar-energy",
    "Edivad99/SolarGeneration",
    "ropensci/nasapower",
    "Scalextrix/ELCC",
    "davit-gh/Solar-Energy-Prediction-Contest",
    "Sp1l/PhotoVoltaic",
    "LibreSolar/learn.libre.solar",
    "RE-volv/revolv",
    "JamieMBright/BrightSolarModel",
    "YaleOpenLab/opensolar",
    "calblueprint/revolv",
    "repolicy/csp-guru",
    "sibyjackgrove/SolarPV-DER-simulation-utility",
    "SolarNetwork/solarquant",
    "aqreed/solarpy",
    "perkier/Perkier.Energy",
    "iobroker-community-adapters/ioBroker.solarlog",
    "adelekuzmiakova/CS229-machine-learning-solar-energy-predictions",
    "acep-solar/ACEP_solar",
    "ahdinosaur/solarmonk",
    "OffGridEnergy/offgrid-solar-power-system",
    "SolarNetwork/solarnetwork",
    "MillerTechnologyPeru/EnergyKit",
    "pierre-haessig/solarhome-control-bench",
    "andres-leon/solar-system",
    "foxriver76/ioBroker.sonnen",
    "mit-dci/SmartSolar",
    "salil-gtm/EBS-Chain",
    "initrc/sharedsolar-android",
    "AAyet/analog-solar-forecasting",
    "jrpespisa/Solaredge-converter",
    "samaras/RaspberryPiSolarLogger",
    "rockclimber112358/solar-energy-forecasting",
    "Dinfangion/solar-output",
    "jcjones/eSolarMonitor",
    "gautamk/SolarEnergyCalculator",
    "Gillou38/Drying-open-source-solution",
    "Fancystacks/sun-scraper",
    "asking28/Solar-forecast",
    "StevenReitsma/sonnet",
    "nikkozzblu/100-percent-renewables",
    "sibyjackgrove/gym-SolarPVDER-environment",
    "markditsworth/Microgrid-Optimization",
    "JachyLikeCoding/SolarEnergy_Chier",
    "palmerjh/Solar-Decathlon-Summer-Internship",
    "thjaeger/msp430-solar-boost",
    "meltaxa/mySolarForecast",
    "gvo34/energy-solar",
    "GerryZhang7/Solar-Tracker",
    "mikegrb/EnergyView.app",
    "glfp/SolarEnergyMonitorInfluxGrafanaDocker",
    "aladdine/solar-energy-market",
    "vipperofvip/solarwidget",
    "shriyanshbele/solar",
    "TheGroundZero/EnergyID_Webhook-Izen",
    "dynamic-and-active-systems-lab/SAM",
    "amruthaha/Sun-Tracking-solar-panel",
    "nrgsim/nrgsim",
    "sulik/solar-farm-dashboard",
    "clare44macharia/Solar",
    "josefjahn/energydisplay-m5",
    "josefjahn/energydisplay",
    "gcunhase/GeneticAlgorithm-SolarCells",
    "johnf/smart_energy_group",
    "yakmoh/Green-Energy",
    "oganesManasian/solar",
    "btasma/EnergySolar",
    "jhlawana/SolarizeEnergy",
    "BillyGun27/SolarEnergy",
    "MarcvdSluys/SolarEnergy",
    "johnf/green_eye_monitor_collector",
    "rafburzy/SolarEnergy",
    "laksh22/Hack4ClimateOracle",
    "johnfortnitekennedy/SolarEnergy",
    "MarjorieBru/SolarEnergy",
    "syii0003/solarEnergy",
    "OrangeBoston/SolarEnergy",
    "hsenot/solarosm",
    "GigaJunky/TeslaSolarChart",
    "Ramogi/solarCalc",
    "GigaJunky/TeslaSolarChart",
    "nicolasfguillaume/3D-Solar-Tracker-IoT-Arduino",
    "iobroker-community-adapters/ioBroker.vedirect",
    "deepakatl/blockchain-energy-live",
    "shaunramsey/SolarEnergyPlanner",
    ]

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
    readme_contents = requests.get(get_readme_download_url(contents)).text
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