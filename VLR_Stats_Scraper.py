import sys
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings

#warnings formatting
def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return '%s:%s\n' % (category.__name__, message)

warnings.formatwarning = warning_on_one_line

#detects whether correct number of arguments inputted, spits error if not
###TODO max number 50
if (len(sys.argv) < 2):
    print("Invalid number of arguments, please input an appropriate vlr.gg link")
    print('For example: ' + sys.argv[0] + ' "https://www.vlr.gg/team/matches/6961/loud/" 20')
    exit()

trueurl = str(sys.argv[1])

#adds https if user forgets
if (trueurl[:10] == "www.vlr.gg"):
    trueurl = "https://" + trueurl

#error for when wrong website
if (trueurl[:18] != "https://www.vlr.gg"):
    print("Error: url should begin with https://www.vlr.gg")
    print("For example: " + sys.argv[0] + ' "https://www.vlr.gg/team/matches/6961/loud/" 20')
    exit()

#figures out if user inputs team, player or event or spits out error if its none
type = trueurl.split("/")[3]
if(type == "team")|(type == "player"):
    page = 0
elif(type == "event"):
    page = 1
else:
    print("Error: Wrong type of input, must either be a teampage, player or an event")
    print("A teampage example would be: " + sys.argv[0] + ' "https://www.vlr.gg/team/matches/6961/loud/" 20')
    print("A player example would be: " + sys.argv[0] + ' "https://www.vlr.gg/player/matches/729/zellsis" 20')
    print("An event example would be: " + sys.argv[0] + ' "https://www.vlr.gg/event/matches/2097/valorant-champions-2024/?series_id=all"\n')
    exit()

#warns about looking at just playoffs in links
if ((trueurl[-3:] != "all")&(page == 1)):
    warnings.warn("\nYour link does not end in 'series_id=all' and therefore may only contain stats from just the group stage or playoffs of the tournament. To fix, make sure you select all stages under the matches page when copying the link. If this is intended, simply ignore this message\n")

#Downloads and parses through the main page
generalresult = requests.get(trueurl).text
generaldoc = BeautifulSoup(generalresult, "html.parser")

#Remembers which tournament it was to later rename the final file
pagename = trueurl.split("/")[6]

#basically finding the links for all the individual matches, needs to be done twice, page = 0 is for looking at team pages, page = 1 is for tournament pages
if page == 0:
    links = generaldoc.find_all('a', class_ = "wf-card fc-flex m-item")
    if(len(sys.argv) < 3):
        warnings.warn("\nDid not specify number of matches for the team/player, will default to: 50")
        gamenumber = 50
    elif(int(sys.argv[2]) > 50):
        warnings.warn("\nSpecified number of matches for the team/player is too high, will default to: 50\nIf you need more matches, just copy the link for the team / player on page 2 and add that data.\nFix coming soon \n")
        gamenumber = 50
    else:
        gamenumber = int(sys.argv[2])
else:
    #figures out accent color for each match 
    link_text = (str(generaldoc.find(class_ = "wf-card", style="margin-bottom: 30px; overflow: visible")).split("mod-first")[0]).split('a class="')[1].strip()
    
    links = (generaldoc.find_all('a', class_ = (link_text + " mod-first")) + generaldoc.find_all('a', class_ = link_text))
    gamenumber = len(links)

#getting the correct link for overwiew & economy
urllist = []
urllist2 = []

mode = 0

if mode == 0:
    for k in links:
        urllist.append("https://www.vlr.gg" + k.get("href"))
        urllist2.append("https://www.vlr.gg" + k.get("href") + "/?game=all&tab=economy")

#legacy code
elif mode == 1:
    for k in links:
        urllist.append("https://www.vlr.gg" + k.get("href") + "/?game=all&tab=performance")

#list of all stats that are being tracked
if (mode == 0):
    namelist = []
    teamlist = []
    agentlist = []
    all_rating = []
    attack_rating = []
    defense_rating = []
    all_kills = []
    attack_kills = []
    defense_kills = []
    all_deaths = []
    attack_deaths = []
    defense_deaths = []
    all_assists = []
    attack_assists = []
    defense_assists = []
    all_KAST = []
    attack_KAST = []
    defense_KAST= []
    all_ADR = []
    attack_ADR = []
    defense_ADR = []
    all_FK = []
    attack_FK = []
    defense_FK = []
    all_FD = []
    attack_FD = []
    defense_FD = []
    mapname = []
    team_a_name = []
    team_b_name = []
    team_a_score = []
    team_b_score = []
    team_a_attack_score = []
    team_b_attack_score = []
    team_a_defense_score = []
    team_b_defense_score = []
    match_datetime = []
    map_pick = []
    team_a_pistols_won = []
    team_b_pistols_won = []
    team_a_ecos_won = []
    team_b_ecos_won = []
    team_a_ecos_played = []
    team_b_ecos_played = []
    team_a_semi_ecos_won = []
    team_b_semi_ecos_won = []
    team_a_semi_ecos_played = []
    team_b_semi_ecos_played = []
    team_a_semi_buy_won = []
    team_b_semi_buy_won = []
    team_a_semi_buy_played = []
    team_b_semi_buy_played = []
    team_a_full_buy_won = []
    team_b_full_buy_won = []
    team_a_full_buy_played = []
    team_b_full_buy_played = []
    patch_played_on = []

    statlist = [namelist, teamlist, agentlist, all_rating, attack_rating, defense_rating, all_kills, attack_kills, defense_kills, all_deaths, attack_deaths,
                defense_deaths, all_assists, attack_assists, defense_assists, all_KAST, attack_KAST, defense_KAST, all_ADR, attack_ADR, defense_ADR, 
                all_FK, attack_FK, defense_FK, all_FD, attack_FD, defense_FD, mapname, team_a_name, team_b_name, team_a_score, team_b_score, team_a_attack_score, 
                team_b_attack_score, team_a_defense_score, team_b_defense_score, match_datetime, map_pick,  team_a_pistols_won, 
                team_b_pistols_won, team_a_ecos_won, team_b_ecos_won, team_a_ecos_played, team_b_ecos_played, team_a_semi_ecos_won, team_b_semi_ecos_won,
                team_a_semi_ecos_played, team_b_semi_ecos_played, team_a_semi_buy_won, team_b_semi_buy_won, team_a_semi_buy_played, team_b_semi_buy_played, 
                team_a_full_buy_won, team_b_full_buy_won, team_a_full_buy_played, team_b_full_buy_played, patch_played_on]

#legacy code  
elif (mode == 1):
    namelist = []
    aces = []
    
    statlist1 = [namelist, aces]

#function that finds a specific stat (must be given sufficient restrictions for unique) and the stat wanted, 
#then also returns a string with no superfluous spaces
def statfinder(div, stat):
    temp = div.find(class_ = stat)
    if(temp is None):
        return "N/A"
    else:
        return str(temp.string).strip()

j = 0

#function that cleans a specific type of string that appears in the economy tab
def strsimp(strings, set):
    if(set == 1):
        return strings.string.strip().split("\t")[0]
    else:
        return (strings.string.strip().split("\t"))[-1].strip("()")

#begin of iterative loop, will go to each number on the page
while (j < gamenumber):

    #looks at latest url in the page
    url = urllist[j]
    url2 = urllist2[j]
    j=j+1

    #looks at match page, parses through all the html
    result = requests.get(url).text

    doc = BeautifulSoup(result, "html.parser")

    #list of specific map ids
    idlist = []

    #slects whether you are looking at detail from the basic map tab or the performance tab
    if(mode == 0):
        gameid = str(doc.find(class_ = "vm-stats-gamesnav-container")).split('data-game-id="')
    elif(mode == 1):
        gameid = str(doc.find(class_ = "vm-stats-container")).split('data-game-id="')

    #???
    for ele in gameid:
        idlist.append(ele.split('"')[0])

    #incase it wasn't a real match, ie a showmatch
    if(len(idlist) < 3):
        print("Error, Match is a bo1 and this is not supported, to filter out showmatches. If this match is a showmatch you may ignore this message")
        continue

    #find the datetime of match
    temp30 = doc.find(class_ = "match-header-date")
    matchdatetime = str(temp30).split('data-utc-ts="')[1].split('"')[0]
    #patch = temp30.find(style = "font-style: italic;").get_text().split("atch")[1].strip()
    #print(patch)
    #finding which patch is being played on
    patchtemp = temp30.find(style = "font-style: italic;")
    if patchtemp is None:
        patch = "n/a"
    else:
        patch = patchtemp.get_text().split("atch")[1].strip()

    #gets rid of first 2 elements in idlist, which are not the actual gameids (bs4 thing)
    idlist.pop(0)
    idlist.pop(0)

    map_num_tracker = 0

    team_first_pick = str(doc.find(class_ = "match-header-note" )).split("\t\t\t")[1].split("ban")[0].strip()

    result2 = requests.get(url2).text
    doc2 = BeautifulSoup(result2, "html.parser")

    #looks for the stat of specific maps within a match
    for mapids in idlist:

        map_num_tracker = map_num_tracker + 1
        #selects the correct html for the match
        hey = doc.select("[data-game-id='" + mapids + "']")
        hey2 = doc2.select("[data-game-id='" + mapids + "']")

        #checks whether map was actually played, or if it was just selected (ie map 3 in bo3 in a 2-0)
        if (len(hey) > 1)&(mode == 0):

            res = hey[1]
            res2 = hey2[1]

            #restring the bs4 search
            otherdiv = res.find(class_ = "map")

            #sometimes there is a remake during the actual match (ie map server crashed) and the match stats aren't really available
            if(otherdiv is None):
                print("BROKEN STATS, CHECK MANUALLY")
            else:
                #finds the map name
                mapd = otherdiv.find(style = "position: relative;")
                map2 = str(mapd).split("span")
                map3 = map2[1].split("\t")
                
                #narrowing the stats down to just the "left" team and "right" team
                otherdiv2 = res.find(class_ = "team")
                otherdiv3 = res.find(class_ = "team mod-right")
                
                otherdiv4 = str(res.find(class_ = "vlr-rounds-row-col")).split('"/>')                
                teama = otherdiv4[1].split("</")[0].strip()
                teamb = otherdiv4[2].split("</")[0].strip()

                #findling teams overall map rounds
                teamascore = int(statfinder(otherdiv2, "score"))
                teambscore = int(statfinder(otherdiv3, "score"))

                #find teams attack rounds
                teamaattack = int(statfinder(otherdiv2, "mod-t"))
                teambattack = int(statfinder(otherdiv3, "mod-t"))

                #finding teams defense rounds
                teamadefense = int(statfinder(otherdiv2, "mod-ct"))
                teambdefense = int(statfinder(otherdiv3, "mod-ct"))

                #econdata, how many pistol rounds, low buys etc won by each team...
                econ_data = res2.find_all(class_ = "stats-sq")
                if(len(econ_data) == 0):
                    teama_pistols_won = teama_ecos_won = teama_ecos_played = teama_semi_ecos_won = "n/a"
                    teama_semi_ecos_played = teama_semi_buy_won = teama_semi_buy_played = teama_full_buy_won = teama_full_buy_played = "n/a"
                    teamb_pistols_won = teamb_ecos_won = teamb_ecos_played = teamb_semi_ecos_won = teamb_semi_ecos_played = "n/a"
                    teamb_semi_buy_won = teamb_semi_buy_played = teamb_full_buy_won = teamb_full_buy_played = "n/a"
                else:
                    teama_pistols_won = int(econ_data[0].string.strip())
                    teama_ecos_won = strsimp(econ_data[1], 1)
                    teama_ecos_played = strsimp(econ_data[1], 2)
                    teama_semi_ecos_won = strsimp(econ_data[2], 1)
                    teama_semi_ecos_played = strsimp(econ_data[2], 2)
                    teama_semi_buy_won = strsimp(econ_data[3], 1)
                    teama_semi_buy_played = strsimp(econ_data[3], 2)
                    teama_full_buy_won = strsimp(econ_data[4], 1)
                    teama_full_buy_played = strsimp(econ_data[4], 2)

                    teamb_pistols_won = int(econ_data[5].string.strip())
                    teamb_ecos_won = strsimp(econ_data[6], 1)
                    teamb_ecos_played = strsimp(econ_data[6], 2)
                    teamb_semi_ecos_won = strsimp(econ_data[7], 1)
                    teamb_semi_ecos_played = strsimp(econ_data[7], 2)
                    teamb_semi_buy_won = strsimp(econ_data[8], 1)
                    teamb_semi_buy_played = strsimp(econ_data[8], 2)
                    teamb_full_buy_won = strsimp(econ_data[9], 1)
                    teamb_full_buy_played = strsimp(econ_data[9], 2)

                #Prints progress updates to terminal for diagnosing failures and to see progress
                print(map3[7] + ":")
                print(teama + " " + str(teamascore) + "-" + str(teambscore) + " " + teamb + "\n")

                #restricting search to the player data tab
                mydivs = res.find_all(class_ = "mod-player")

                #basic player info
                for element in mydivs:
                    #player name
                    statlist[0].append(statfinder(element, "text-of"))

                    #player org
                    statlist[1].append(statfinder(element, "ge-text-light"))

                    #player match datetime
                    statlist[36].append(matchdatetime)

                    #patch playerd on
                    statlist[56].append(patch)

                    #actually appending map
                    statlist[27].append(map3[7])

                    #map pick
                    if(((map_num_tracker == 1)&(teama == team_first_pick))|((map_num_tracker == 2)&(teamb == team_first_pick))):
                        map_pick.append(1)
                    elif(((map_num_tracker == 2)&(teama == team_first_pick))|((map_num_tracker == 1)&(teamb == team_first_pick))):
                        map_pick.append(2)
                    else:
                        map_pick.append(3)

                    #appending team scores and econs to each individual player
                    statlist[28].append(teama)
                    statlist[29].append(teamb)
                    statlist[30].append(teamascore)
                    statlist[31].append(teambscore)
                    statlist[32].append(teamaattack)
                    statlist[33].append(teambattack)
                    statlist[34].append(teamadefense)
                    statlist[35].append(teambdefense)
                    statlist[38].append(teama_pistols_won)
                    statlist[39].append(teamb_pistols_won)
                    statlist[40].append(teama_ecos_won)
                    statlist[41].append(teamb_ecos_won)
                    statlist[42].append(teama_ecos_played)
                    statlist[43].append(teamb_ecos_played)
                    statlist[44].append(teama_semi_ecos_won)
                    statlist[45].append(teamb_semi_ecos_won)
                    statlist[46].append(teama_semi_ecos_played)
                    statlist[47].append(teamb_semi_ecos_played)
                    statlist[48].append(teama_semi_buy_won)
                    statlist[49].append(teamb_semi_buy_won)
                    statlist[50].append(teama_semi_buy_played)
                    statlist[51].append(teamb_semi_buy_played)
                    statlist[52].append(teama_full_buy_won)
                    statlist[53].append(teamb_full_buy_won)
                    statlist[54].append(teama_full_buy_played)
                    statlist[55].append(teamb_full_buy_played)

                #agent played
                mydivs1 = res.find_all(class_ = "mod-agents")

                for element in mydivs1:
                    #cannot use statfinder func due to the fact agent isn't actually shown, just an image
                    potato = str(element.find(class_ = "stats-sq mod-agent small")).split('title="')
                    potato2 = potato[1].split('"/></s')
                    statlist[2].append(potato2[0])
                
                #restring to the real numbers
                mydivs2 = res.find_all(class_ = "mod-stat")

                i = 0
                while i < len(mydivs2):
                    x = i % 12
                    #finding vlr rating and kills for overall, attack and defense x = 0, x =2
                    if((x == 0)|(x == 2)):
                        statlist[int(3 + (1.5 * x))].append(statfinder(mydivs2[i], "side mod-side mod-both"))
                        statlist[int(4 + (1.5 * x))].append(statfinder(mydivs2[i], "side mod-side mod-t"))
                        statlist[int(5 + (1.5 * x))].append(statfinder(mydivs2[i], "side mod-side mod-ct"))
                    #finding deaths and assists for overall, attack and defense
                    if((x == 3)|(x == 4)):
                        statlist[x * 3].append(statfinder(mydivs2[i], "side mod-both"))
                        statlist[x * 3 + 1].append(statfinder(mydivs2[i], "side mod-t"))
                        statlist[x * 3 + 2].append(statfinder(mydivs2[i], "side mod-ct"))
                    #finding KAST and adr for overall, attack and defense
                    if((x == 6)|(x == 7)):
                        statlist[x * 3 - 3].append(statfinder(mydivs2[i], "side mod-both"))
                        statlist[x * 3 - 2].append(statfinder(mydivs2[i], "side mod-t"))
                        statlist[x * 3 - 1].append(statfinder(mydivs2[i], "side mod-ct"))

                    #finding FK and FD for overall, attack and defense
                    if((x == 9)|(x == 10)):
                        statlist[x * 3 - 6].append(statfinder(mydivs2[i], "side mod-both"))
                        statlist[x * 3 - 5].append(statfinder(mydivs2[i], "side mod-t"))
                        statlist[x * 3 - 4].append(statfinder(mydivs2[i], "side mod-ct"))

                    i = i + 1
        
        #doing the loop for performance mode, legacy code
        elif(len(hey) > 1)&(mode == 1):
            
            res = hey[1]

            temp0 = res.find(class_="wf-table-inset mod-adv-stats")
            x = 0
            if(temp0 is None):
                x = x + 1
            else:

                temp1 = temp0.select("tr")
                i = 1
                while(i < len(temp1)):
                    temp2 = temp1[i].find(class_ = "stats-sq wf-popable vm-perf-notable mod-a")
                    temp3 = temp1[i].find(class_ = "team-tag ge-text-faded")
                    print(str(temp3.string).strip())
                    if (temp2 is None):
                        x = x + 1
                    else:
                        statlist1[0].append(str(temp3.string).strip())
                        temp10 = str(temp2).split('mod-a">')
                        temp11 = temp10[1].split('<div')
                        statlist1[1].append(temp11[0].strip())

                    i = i + 1
    
            

#put all the stats into a big table            
if (mode == 0):
    data = {'Player':  statlist[0],
            'Team': statlist[1],
            'Map': statlist[27],
            'Match Datetime': statlist[36],
            'Patch': statlist[56],
            'Team A Name': statlist[28],
            'Team B Name': statlist[29],
            'Team A Score': statlist[30],
            'Team B Score': statlist[31],
            'Team A Attack Score': statlist[32],
            'Team B Attack Score': statlist[33],
            'Team A Defense Score': statlist[34],
            'Team B Defense Score': statlist[35],
            'Agent': statlist[2],
            'Overall VLR rating': statlist[3],
            'Attack VLR rating': statlist[4],
            'Defense VLR rating': statlist[5],
            'Overall Kills': statlist[6],
            'Attack Kills': statlist[7],
            'Defense Kills': statlist[8],
            'Overall Deaths': statlist[9],
            'Attack Deaths': statlist[10],
            'Defense Deaths': statlist[11],
            'Overall Assists': statlist[12],
            'Attack Assists': statlist[13],
            'Defense Assists': statlist[14],
            'Overall KAST': statlist[15],
            'Attack KAST': statlist[16],
            'Defense KAST': statlist[17],
            'Overall ADR': statlist[18],
            'Attack ADR': statlist[19],
            'Defense ADR': statlist[20],
            'Overall FK': statlist[21],
            'Attack FK': statlist[22],
            'Defense FK': statlist[23],
            'Overall FD': statlist[24],
            'Attack FD': statlist[25],
            'Defense FD': statlist[26],
            'Map_Pick': map_pick,
            'Team A Pistol Wins': statlist[38],
            'Team B Pistol Wins': statlist[39],
            'Team A Eco Wins': statlist[40],
            'Team B Eco Wins': statlist[41],
            'Team A Eco Played': statlist[42],
            'Team B Eco Played': statlist[43],
            'Team A Semi-Eco Wins': statlist[44],
            'Team B Semi-Eco Wins': statlist[45],
            'Team A Semi-Eco Played': statlist[46],
            'Team B Semi-Eco Played': statlist[47],
            'Team A Semi-Buy Wins': statlist[48],
            'Team B Semi-Buy Wins': statlist[49],
            'Team A Semi-Buy Played': statlist[50],
            'Team B Semi-Buy Played': statlist[51],
            'Team A Full-Buy Wins': statlist[52],
            'Team B Full-Buy Wins': statlist[53],
            'Team A Full-Buy Played': statlist[54],
            'Team B Full-Buy Played': statlist[55],
            }

#legacy code    
elif (mode == 1):
    data = {'Team': statlist1[0],
            'Aces': statlist1[1]}

#helper function that figures out wether it was the current players map pick or not
def team_map(row):
    if (row['Team A Name'] == row['Team']):
        if(row['Map_Pick'] == 1):
            return "Team Pick"
        elif(row['Map_Pick'] == 2):
             return "Opponent Pick"
        else:
            return "Decider"
    else:
        if(row['Map_Pick'] == 1):
            return "Opponent Pick"
        elif(row['Map_Pick'] == 2):
             return "Team Pick"
        else:
            return "Decider"


df = pd.DataFrame(data)

df['Map Pick'] = df.apply(team_map, axis = 1)

#helper function that switches data from "team a" and "team b" to current team and opposing team correctly
def column_fix(Result_name, Team_a_name, Team_b_name, Opponent_Result_name):
    df[Result_name] = np.where(df['Team'] == df['Team A Name'], df[Team_a_name], np.where(df['Team'] == df['Team B Name'], df[Team_b_name], np.nan))
    df[Opponent_Result_name] = np.where(df['Team'] == df['Team B Name'], df[Team_a_name], np.where(df['Team'] == df['Team A Name'], df[Team_b_name], np.nan))


df['Opponent Team'] = np.where(df['Team'] == df['Team A Name'], df['Team B Name'], np.where(df['Team'] == df['Team B Name'], df['Team A Name'], np.nan))

column_fix('Team Score', 'Team A Score', 'Team B Score', 'Opponent Team Score')
column_fix('Team Attack Score', 'Team A Attack Score', 'Team B Attack Score', 'Opponent Team Attack Score')
column_fix('Team Defense Score', 'Team A Defense Score', 'Team B Defense Score', 'Opponent Team Defense Score')
column_fix('Team Pistol Wins', 'Team A Pistol Wins', 'Team B Pistol Wins', 'Opponent Team Pistol Wins')
column_fix('Team Eco Wins', 'Team A Eco Wins', 'Team B Eco Wins', 'Opponent Team Eco Wins')
column_fix('Team Eco Played', 'Team A Eco Played', 'Team B Eco Played', 'Opponent Team Eco Played')
column_fix('Team Semi-Eco Wins', 'Team A Semi-Eco Wins', 'Team B Semi-Eco Wins', 'Opponent Team Semi-Eco Wins')
column_fix('Team Semi-Eco Played', 'Team A Semi-Eco Played', 'Team B Semi-Eco Played', 'Opponent Team Semi-Eco Played')
column_fix('Team Semi-Buy Wins', 'Team A Semi-Buy Wins', 'Team B Semi-Buy Wins', 'Opponent Team Semi-Buy Wins')
column_fix('Team Semi-Buy Played', 'Team A Semi-Buy Played', 'Team B Semi-Buy Played', 'Opponent Team Semi-Buy Played')
column_fix('Team Full-Buy Wins', 'Team A Full-Buy Wins', 'Team B Full-Buy Wins', 'Opponent Team Full-Buy Wins')
column_fix('Team Full-Buy Played', 'Team A Full-Buy Played', 'Team B Full-Buy Played', 'Opponent Team Full-Buy Played')

def victory(row):
    if row['Team Score'] > row['Opponent Team Score']:
        return True
    else:
        return False
df['Victory?'] = df.apply(victory, axis = 1)

df = df.drop(['Team A Name', 'Team B Name', 'Team A Score', 'Team B Score', 'Team A Attack Score', 'Team B Attack Score', 'Team A Defense Score', 'Team B Defense Score',
              'Team A Pistol Wins', 'Team B Pistol Wins', 'Team A Eco Wins', 'Team B Eco Wins', 'Team A Eco Played', 'Team B Eco Played', 'Team A Semi-Eco Wins', 
              'Team B Semi-Eco Wins', 'Team A Semi-Eco Played', 'Team B Semi-Eco Played', 'Team A Semi-Buy Wins', 'Team B Semi-Buy Wins', 'Team A Semi-Buy Played', 
              'Team B Semi-Buy Played', 'Team A Full-Buy Wins', 'Team B Full-Buy Wins', 'Team A Full-Buy Played', 'Team B Full-Buy Played', 'Map_Pick'], axis=1)

#exports to csv based on statspage
df.to_csv(pagename + ".csv")
print(df)

