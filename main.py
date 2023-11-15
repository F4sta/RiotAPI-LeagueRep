
import json

from constans import *
from functions import *

from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.markdown import Markdown
from rich.text import Text

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
        
        #initalizing 
        self.summoner_name = summoner_name 
        self.region        = region 
        self.region_code   = region_code
        
        #Getting datas from ""
        self.profile = get_summoner_info_by_name(summoner_name)
        self.id            = self.profile["id"]
        self.accountId     = self.profile["accountId"]
        self.puuid         = self.profile["puuid"]
        self.summonerLevel = self.profile["summonerLevel"]
        self.profileIconId = self.profile["profileIconId"]
        self.revisionDate  = self.profile["revisionDate"]

        self.ranked_stats = get_ranked_data(self.id, self.region_code)
        
        #Getting datas for solo/duo
        self.ranked_solo = self.ranked_stats[1]
        self.solo_queueType     = self.ranked_solo["queueType"]
        self.solo_tier          = self.ranked_solo["tier"]
        self.solo_rank          = self.ranked_solo["rank"]
        self.solo_lp            = self.ranked_solo["leaguePoints"]
        self.solo_wins          = self.ranked_solo["wins"]
        self.solo_losses        = self.ranked_solo["losses"]
        
        #Getting datas for flex
        self.ranked_flex = self.ranked_stats[0]
        self.flex_queueType     = self.ranked_solo["queueType"]
        self.flex_tier          = self.ranked_flex["tier"]
        self.flex_rank          = self.ranked_flex["rank"]
        self.flex_lp            = self.ranked_flex["leaguePoints"]
        self.flex_wins          = self.ranked_flex["wins"]
        self.flex_losses        = self.ranked_flex["losses"]
        
    def check_active_game(self):
        game = get_active_game_by_user_id(self.id)
        if game:
            print("There is an active game")
        
    def get_matches(self,   
                        amount: int,
                        match_detailed_name: bool = False,
                        save: bool = False,
                        Return = False
                    ):
        
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
        if not Return:
            c = Console()
            c.print(table)
        else:
            return(table)
        
    def profile_stats(self):
        
        soloduo = Table(title="Ranked Solo/Duo")
        soloduo.add_column("Rank", justify="left", style="cyan")
        soloduo.add_column("Win / Lose", justify="center", style="cyan")
        soloduo.add_row(f"{self.solo_tier} {self.solo_rank} ({self.solo_lp})", f"{self.solo_wins} / {self.solo_losses}")
        
        flex = Table(title="Ranked Flex")
        flex.add_column("Rank", justify="left", style="cyan")
        flex.add_column("Win / Lose", justify="center", style="cyan")
        flex.add_row(f"{self.flex_tier} {self.flex_rank} ({self.flex_lp})", f"{self.flex_wins} / {self.flex_losses}")

        MARKDOWN = f"""
# {Text(f"{self.summoner_name} - {self.summonerLevel}", style="italic")}
"""
        layout = Layout()
        layout.split_column(
            Layout(renderable=Markdown(MARKDOWN)),
            Layout(name="solo/duo", renderable=soloduo),
            Layout(name="flex", renderable=flex),
            Layout(name="match-history", renderable=self.get_matches(5, Return=True))
        )
        
        return layout
    
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

asta = Summoner("Rattataaa")

c = Console()
"""
c.print(asta.get_matches(5, Return=True))
"""
save_dict(asta.ranked_stats, "stats")
a = asta.profile_stats()
c.print(a)
