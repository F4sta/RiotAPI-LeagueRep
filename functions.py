
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

def get_champion_assets_link(champion: str):
    """
    Gets links for champion assets
    :return: Dictionary of assets link for a champion.
    """
    return {
        "splash_art" : f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_0.jpg",
        "loading_screen" : f"http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champion}_0.jpg",
        "square" : f"http://ddragon.leagueoflegends.com/cdn/13.21.1/img/champion/{champion}.png"
    }

def get_champion_data(champion: str):
    """
    Gets datas from an exact champion
    """

    params = {
        "api_key" : API_KEY
    }

    api_url = f"http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion/{champion}.json"
    
    return riot_request(api_url, params)

def save_all_champion_json():
    """
    Saves all the champions data
    """
    champions = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion.json").json()
    for Champion in champions["data"]:
        id = champions["data"][Champion]["id"]
        name = champions["data"][Champion]["name"]
        try:
            Champion = requests.get(f"http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion/{id}.json").json()
            save_dict(dict=Champion, name=f'{id}', save_folder="saved/Champions/")
        except:
            print(f"Couldnt save {name}.json")

def get_summoner_icon_by_id(id: int | str):
    '''
    Returns the link for a specified icon by their id
    '''
    if not id:
        id = input("Icon ID: ")
        
    api_url = f"http://ddragon.leagueoflegends.com/cdn/13.21.1/img/profileicon/{id}.png"
    
    return requests.get(api_url).json()

def get_summoner_info_by_name(summoner_name: str = None, region_code: str = DEFAULT_REGION_CODE):
    '''
    Gets infromation about a summoner by their name
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

def get_match_data_by_match_id(match_id: str, region: str = DEFAULT_REGION):
    ''' 
    Gets data from a specific match by its id
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
    Checks if a summoner is ingame by their id
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
        if res.status_code not in [403, 404]:
            print(e)
        return None

def get_ranked_data(id: str, region_code: str = DEFAULT_REGION_CODE):
    """
    Returns an summoner ranked stats by their id
    """
    
    params ={
        "api_key" : API_KEY
    }

    api_url = f"https://{region_code}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}"

    return riot_request(api_url, params)



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

