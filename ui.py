import flet as ft
from main import *

def main(page: ft.Page):
    
    page.title = "LeagueRep"
    page.window_resizable = False
    page.window_width = 800
    page.window_height = 600
    page.window_center()
    page.window_to_front()

    searchbar = ft.TextField(hint_text="Summoner name")
    elavetadbutton = ft.ElevatedButton(text="get")
    
    page.add(
        ft.Row(
            [
                searchbar, elavetadbutton
            ]
        )
    )
    
    def generate_matchhistory(e, summoner: Summoner):
        matches_in_table = []
        matches = summoner.get_matches_stats(5)
        for match in matches:
            
            i = matches.index(match)
                
            champion = match["champion"]
            champLevel = match["champLevel"]
            kills = int(match["kills"])
            deaths = int(match["deaths"])
            assists = int(match["assists"])
            farm = match["farm"]
            totalDamageDealtToChampions = match["totalDamageDealtToChampions"]
            visionScore = match["visionScore"]
        
            if not deaths == 0:
                kda = (kills + assists) / deaths
            else:
                kda = (kills + assists)
            kda = round(kda, 2)
            
            matches_in_table.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f'({i + 1})')),
                        ft.DataCell(ft.Text(f'({champLevel}) {champion}')),
                        ft.DataCell(ft.Text(f'{kills} / {deaths} / {assists}')),
                        ft.DataCell(ft.Text(f'{farm}')),
                        ft.DataCell(ft.Text(f'{totalDamageDealtToChampions}')),
                        ft.DataCell(ft.Text(f'{farm}')),
                    ]
                )
            )
        return matches_in_table
            
    def getProfile(e):
        if searchbar.value != "":
            
            summoner = Summoner(searchbar.value)
            dataRows = generate_matchhistory(e=None , summoner=summoner)
            
            page.add(
                
                ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Match")),
                            ft.DataColumn(ft.Text("Champion")),
                            ft.DataColumn(ft.Text("KDA")),
                            ft.DataColumn(ft.Text("CS")),
                            ft.DataColumn(ft.Text("Total Dmg Dealt")),
                            ft.DataColumn(ft.Text("Vision")),
                        ],
                        rows=dataRows,
                        
                )
            )
            searchbar.value = ""
            page.update()
                
    elavetadbutton.on_click = getProfile
    page.update()


if __name__ == "__main__":
    ft.app(main)
    
    