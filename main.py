from sys import argv
import json

from constans import *
from functions import *

from shutil import get_terminal_size
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.markdown import Markdown
from rich.text import Text

class Summoner():

    def __init__(self,  summoner_name: str,
                        region: str = DEFAULT_REGION,
                        region_code: str = DEFAULT_REGION_CODE
                ):
        
        #initalizing 
        self.summoner_name = summoner_name 
        self.region        = region 
        self.region_code   = region_code
        
        #Getting datas from ""
        self.profile = get_summoner_info_by_name(self.summoner_name)
        self.id            = self.profile["id"]
        self.accountId     = self.profile["accountId"]
        self.puuid         = self.profile["puuid"]
        self.summonerLevel = self.profile["summonerLevel"]
        self.profileIconId = self.profile["profileIconId"]
        self.revisionDate  = self.profile["revisionDate"]

        #Getting datas about the summoner ranked performance
        self.ranked_stats = get_ranked_data(self.id, self.region_code)
        for i in range(2):
            try:
                self.data = self.ranked_stats[i]
                
                if self.data["queueType"] == "RANKED_SOLO_5x5":
                    self.solo_queueType     = self.data["queueType"]
                    self.solo_tier          = self.data["tier"]
                    self.solo_rank          = self.data["rank"]
                    self.solo_lp            = self.data["leaguePoints"]
                    self.solo_wins          = self.data["wins"]
                    self.solo_losses        = self.data["losses"]
                    
                elif self.data["queueType"] == "RANKED_FLEX_SR":
                    self.flex_queueType     = self.data["queueType"]
                    self.flex_tier          = self.data["tier"]
                    self.flex_rank          = self.data["rank"]
                    self.flex_lp            = self.data["leaguePoints"]
                    self.flex_wins          = self.data["wins"]
                    self.flex_losses        = self.data["losses"]
            except:continue
            
        try:
            if self.solo_queueType == "RANKED_SOLO_5x5":pass
        except:
            self.solo_queueType     = ""
            self.solo_tier          = ""
            self.solo_rank          = ""
            self.solo_lp            = ""
            self.solo_wins          = ""
            self.solo_losses        = ""
                
        try:
            if self.flex_queueType == "RANKED_FLEX_SR":pass
        except:
            self.flex_queueType     = ""
            self.flex_tier          = ""
            self.flex_rank          = ""
            self.flex_lp            = ""
            self.flex_wins          = ""
            self.flex_losses        = ""
        
    def check_active_game(self):
        if get_active_game_by_user_id(self.id) != None:return True
        else: return False
        
    def get_matches_stats(self,   
                        amount: int,
                        save: bool = False,
                        return_rich_table = False
                    ):
        
        #Store match datas into list
        match_ids = get_match_ids_by_summoner_puuid(self.puuid, amount)
        match_infos = []
        
        for match_id in match_ids:
            match = get_match_data_by_match_id(match_id)
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
                    "farm"             :(int(match["info"]["participants"][Index]["totalMinionsKilled"]) +
                                        int(match["info"]["participants"][Index]["totalAllyJungleMinionsKilled"]) +
                                        int(match["info"]["participants"][Index]["totalEnemyJungleMinionsKilled"])),
                    "totalDamageDealt" : match["info"]["participants"][Index]["totalDamageDealt"],    
                    "visionScore"      : match["info"]["participants"][Index]["visionScore"],
                    "win"              : match["info"]["participants"][Index]["win"]
                }
            )
        
        if save:
            save_dict(match_infos, f"{self.summoner_name}_{amount}_match_history")
            
        if return_rich_table:
            #create rich table
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
            return table
            
        else:
            return(match_infos)
        
    def profile_stats(self):
        MARKDOWN = f"""
# {Text(f"{self.summoner_name} - {self.summonerLevel}", style="italic")}
"""
        markdown = Markdown(MARKDOWN)  
        
        soloduo = Table(title="Ranked Solo/Duo")
        soloduo.add_column("Rank", justify="left", style="cyan")
        soloduo.add_column("Win / Lose", justify="center", style="cyan")
        soloduo.add_row(f"{self.solo_tier} {self.solo_rank} ({self.solo_lp})", f"{self.solo_wins} / {self.solo_losses}")
        
        flex = Table(title="Ranked Flex")
        flex.add_column("Rank", justify="left", style="cyan")
        flex.add_column("Win / Lose", justify="center", style="cyan")
        flex.add_row(f"{self.flex_tier} {self.flex_rank} ({self.flex_lp})", f"{self.flex_wins} / {self.flex_losses}")

        return (markdown, soloduo, flex)
    
    def save_some_data(self):
        
        profile = get_summoner_info_by_name(self.summoner_name)
        match_ids = get_match_ids_by_summoner_puuid(profile["puuid"], 100)
        match_info = get_match_data_by_match_id(match_ids[0])
        items = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/item.json").json()
        champions = requests.get("http://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion.json").json()
        active_game = get_active_game_by_user_id(profile["id"])
        
        save_dict(profile, "profile")
        save_dict(match_ids, "match_ids")
        save_dict(match_info, "match_info")
        save_dict(items, "items")
        save_dict(champions, "champions")
        save_dict(active_game, "active_game")

try:
    summoner = Summoner(str(argv[1]))
except:
    summoner = Summoner(input("Summoner name: "))

c = Console()
summoner.save_some_data()
a = summoner.profile_stats()
for o in a:
    c.print(o)
