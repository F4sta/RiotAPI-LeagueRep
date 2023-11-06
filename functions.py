
import requests, json
from urllib.parse import urlencode

from constans import *    

def save_dict(dict: dict, name: str, save_folder: str = "saved/"):
    open(save_folder + f"{name}.json", "w").write(json.dumps(dict, indent=4))

def riot_request(api_url: str, params:dict):
    try:
        res = requests.get(api_url, params=urlencode(params))
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
def get_champion_info(champion: str):
    try:
        res = requests.get(f"http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion/{champion}.json")
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        return None

def get_champion_assets_link(champion: str):
    return {
        "splash_art" : f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_0.jpg",
        "loading_screen" : f"http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champion}_0.jpg",
        "square" : f"http://ddragon.leagueoflegends.com/cdn/13.21.1/img/champion/{champion}.png"
    }

def get_user_info_by_name(summoner_name: str = None, region_code: str = DEFAULT_REGION_CODE):
    '''
    Gets infromation about a summoner by their name
    :return: Information about the summoner or None if there is an issue
    '''
    if not summoner_name:
        summoner_name = input("Enter summoner namme: ")
        
    params = {
        "api_key" : API_KEY
    }
    
    api_url = f"https://{region_code}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    
    return riot_request(api_url, params)
    
def get_match_ids_by_summoner_puuid(puuid: str, matches_count: int = 20, region: str = DEFAULT_REGION):
    '''
    Gets summoner's match ids by their puuid
    
    Args:
        puuid (str): The PUUID of the summoner.
        region (str): The region where the summoner located.
        matches_count (int = 0-100): The number of match ids to return.
        
    Returns:
        List | None: List of match IDs if succesful, None if there is an issue.
    
    Example:
        get_match_ids_by_summoner_puuid(sample_puuid, 100, "europe")
    
    '''
    if not puuid:
        puuid = input("Enter summoner PUUID: ")
        
    params = {
        "api_key" : API_KEY,
        "count" : matches_count
    }
    
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    
    return riot_request(api_url, params)

def get_match_info_by_match_id(match_id: str, region: str = DEFAULT_REGION):
    ''' 
    
    '''

    if not match_id:
        match_id = input("Enter match ID: ")
        
    params = {
        "api_key" : API_KEY
    }
    
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    
    return riot_request(api_url, params)

def get_active_game_by_user_id(id: str, region_code: str = DEFAULT_REGION_CODE):
    '''
    
    '''
    
    if not id:
        id = input("Enter user ID: ")
        
    params = {
        "api_key" : API_KEY
    }

    api_url = f"https://{region_code}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}"
    
    try:
        res = requests.get(api_url, params=urlencode(params))
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        return None

def get_summoner_icon_by_id(id: int | str):
    '''
    
    '''
    
    if not id:
        id = input("Icon ID: ")
        
    api_url = f"http://ddragon.leagueoflegends.com/cdn/13.21.1/img/profileicon/{id}.png"
    
    return requests.get(api_url).json()










''' profile = get_user_info_by_name("Rattataaa")
save_dict(profile, "profile")

match_ids = get_match_ids_by_summoner_puuid(profile["puuid"], 100)
save_dict(match_ids, "match_ids")

match_info = get_match_info_by_match_id(match_ids[1])
save_dict(match_info, "match_info")

items = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/item.json").json()
save_dict(items, "items")

champions = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion.json").json()
save_dict(champions, "champions")

active_game = get_active_game_by_user_id(profile["id"])
save_dict(active_game, "active_game") '''

''' for Champion in champions["data"]:
    id = champions["data"][Champion]["id"]
    name = champions["data"][Champion]["name"]
    try:
        Champion = requests.get(f"http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion/{id}.json").json()
        save_dict(dict=Champion, name=f'{id}', save_folder="saved/Champions/")
    except:
        raise Exception
'''

'''

​https://127.0.0.1:2999/liveclientdata/activeplayer - data from active game localy 

https://127.0.0.1:2999/liveclientdata/playerscores?summonerName=

​https://127.0.0.1:2999/liveclientdata/playersummonerspells?summonerName=

https://127.0.0.1:2999/liveclientdata/playeritems?summonerName=

https://127.0.0.1:2999/liveclientdata/eventdata

https://static.developer.riotgames.com/docs/lol/queues.json

https://static.developer.riotgames.com/docs/lol/maps.json

https://static.developer.riotgames.com/docs/lol/gameModes.json

https://static.developer.riotgames.com/docs/lol/gameTypes.json

'''

