
import json

import decimal
from decimal import Decimal

from constans import *
from functions import *

from rich.console import Console
from rich.table import Table

def save_all_champion_json():
    
    champions = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion.json").json()
    for Champion in champions["data"]:
        id = champions["data"][Champion]["id"]
        name = champions["data"][Champion]["name"]
        try:
            Champion = requests.get(f"http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion/{id}.json").json()
            save_dict(dict=Champion, name=f'{id}', save_folder="saved/Champions/")
        except:
            print(f"Couldnt save {name}.json")

class Summoner():

    def __init__(self,  summoner_name: str,
                        region: str = DEFAULT_REGION,
                        region_code: str = DEFAULT_REGION_CODE
                ):
        
        self.summoner_name = summoner_name 
        self.region        = region 
        self.region_code   = region_code
        
        self.profile = get_user_info_by_name(summoner_name)
        
        self.id            = self.profile["id"]
        self.accountId     = self.profile["accountId"]
        self.puuid         = self.profile["puuid"]
        self.summonerLevel = self.profile["summonerLevel"]
        self.profileIconId = self.profile["profileIconId"]
        self.revisionDate  = self.profile["revisionDate"]
        
    def check_active_game(self):
        
        game = get_active_game_by_user_id(self.id)
        
        if game:
            print("There is an active game")
        
    def get_matches(self, amount: int, match_detailed_name: bool = False, save: bool = False):
        
        match_ids = get_match_ids_by_summoner_puuid(self.puuid, amount)
        match_infos = []
        
        for match_id in match_ids:
            match = get_match_info_by_match_id(match_id)
            participants: list = match["metadata"]["participants"]
            Index = participants.index(self.puuid)
            
            match_infos.append(
                {
                    "matchId"          : match["metadata"]["matchId"],
                    "champion"         : match["info"]["participants"][Index]["championName"],
                    "champLevel"       : match["info"]["participants"][Index]["champLevel"],
                    "kills"            : match["info"]["participants"][Index]["kills"],
                    "deaths"           : match["info"]["participants"][Index]["deaths"],
                    "assists"          : match["info"]["participants"][Index]["assists"],
                    "farm"             :   (int(match["info"]["participants"][Index]["totalMinionsKilled"]) +
                                            int(match["info"]["participants"][Index]["totalAllyJungleMinionsKilled"]) +
                                            int(match["info"]["participants"][Index]["totalEnemyJungleMinionsKilled"])),
                    "totalDamageDealt" : match["info"]["participants"][Index]["totalDamageDealt"],    
                    "visionScore"      : match["info"]["participants"][Index]["visionScore"],
                    "win"              : match["info"]["participants"][Index]["win"]
                }
            )
            
        if save:
            save_dict(match_infos, f"{self.summoner_name}_{amount}_match_history")
            
        table = Table(title=f"{self.summoner_name} - Match History")

        table.add_column("Match", justify="center", style="green", no_wrap=True)
        table.add_column("Champion", justify="right", style="cyan")
        table.add_column("Kda", justify="center", style="cyan")
        table.add_column("-- II --", justify="center", style="cyan")
        table.add_column("Creep Score", justify="center", style="cyan")
        table.add_column("Total Dmg Dealt", justify="center", style="cyan")
        table.add_column("Vision", justify="center", style="green")
        
        for match in match_infos:
            
            i = match_infos.index(match)
            color = "green"
            
            if not match["win"]:
                color = "red"
            
            match_id = match["matchId"]
            champion = match["champion"]
            champLevel = match["champLevel"]
            kills = int(match["kills"])
            deaths = int(match["deaths"])
            assists = int(match["assists"])
            farm = match["farm"]
            totalDamageDealt = match["totalDamageDealt"]
            visionScore = match["visionScore"]
            
            if not deaths == 0:
                kda = (kills + assists) / deaths
            else:
                kda = (kills + assists)
            kda = round(kda, 2)
            
            if not match_detailed_name:
                table.add_row(
                    f'({i + 1})',
                    f'({champLevel}) {champion}',
                    f'{kills} / {deaths} / {assists}',
                    f'({kda})',
                    f'{farm}',
                    f'{totalDamageDealt}',
                    f'{visionScore}'
                    ,style=color
                )
            else:
                table.add_row(
                    f'({i + 1}) {match_id}',
                    f'({champLevel}) {champion}',
                    f'{kills} / {deaths} / {assists}',
                    f'({kda})',
                    f'{farm}',
                    f'{totalDamageDealt}',
                    f'{visionScore}'
                    ,style=color
                )

        console = Console()
        console.print(table)
    
    def save_some_data(self):
        
        profile = get_user_info_by_name(self.summoner_name)
        match_ids = get_match_ids_by_summoner_puuid(profile["puuid"], 100)
        match_info = get_match_info_by_match_id(match_ids[0])
        items = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/item.json").json()
        champions = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion.json").json()
        active_game = get_active_game_by_user_id(profile["id"])
        
        save_dict(profile, "profile")
        save_dict(match_ids, "match_ids")
        save_dict(match_info, "match_info")
        save_dict(items, "items")
        save_dict(champions, "champions")
        save_dict(active_game, "active_game")


    

asta = Summoner("Rattataaa")
asta.get_matches(10)
asta.check_active_game()
