import os
import pandas as pd

#List of all official VCT Franchised events as of 2024, feel free to add more
list_of_links = ["https://www.vlr.gg/event/matches/1188/champions-tour-2023-lock-in-s-o-paulo/?series_id=all",
                 "https://www.vlr.gg/event/matches/1189/champions-tour-2023-americas-league/?series_id=all",
                 "https://www.vlr.gg/event/matches/1190/champions-tour-2023-emea-league/?series_id=all",
                 "https://www.vlr.gg/event/matches/1191/champions-tour-2023-pacific-league/?series_id=all",
                 "https://www.vlr.gg/event/matches/1494/champions-tour-2023-masters-tokyo/?series_id=all",
                 "https://www.vlr.gg/event/matches/1658/champions-tour-2023-americas-last-chance-qualifier/?series_id=all",
                 "https://www.vlr.gg/event/matches/1659/champions-tour-2023-emea-last-chance-qualifier/?series_id=all",
                 "https://www.vlr.gg/event/matches/1660/champions-tour-2023-pacific-last-chance-qualifier/?series_id=all",
                 "https://www.vlr.gg/event/matches/1657/valorant-champions-2023/?series_id=all",
                 "https://www.vlr.gg/event/matches/1923/champions-tour-2024-americas-kickoff/?series_id=all",
                 "https://www.vlr.gg/event/matches/1926/champions-tour-2024-china-kickoff/?series_id=all",
                 "https://www.vlr.gg/event/matches/1925/champions-tour-2024-emea-kickoff/?series_id=all",
                 "https://www.vlr.gg/event/matches/1924/champions-tour-2024-pacific-kickoff/?series_id=all",
                 "https://www.vlr.gg/event/matches/1921/champions-tour-2024-masters-madrid/?series_id=all",
                 "https://www.vlr.gg/event/matches/2004/champions-tour-2024-americas-stage-1/?series_id=all",
                 "https://www.vlr.gg/event/matches/2006/champions-tour-2024-china-stage-1/?series_id=all",
                 "https://www.vlr.gg/event/matches/1998/champions-tour-2024-emea-stage-1/?series_id=all",
                 "https://www.vlr.gg/event/matches/2002/champions-tour-2024-pacific-stage-1/?series_id=all",
                 "https://www.vlr.gg/event/matches/1999/champions-tour-2024-masters-shanghai/?series_id=all",
                 "https://www.vlr.gg/event/matches/2095/champions-tour-2024-americas-stage-2/?series_id=all",
                 "https://www.vlr.gg/event/matches/2096/champions-tour-2024-china-stage-2/?series_id=all",
                 "https://www.vlr.gg/event/matches/2094/champions-tour-2024-emea-stage-2/?series_id=all",
                 "https://www.vlr.gg/event/matches/2005/champions-tour-2024-pacific-stage-2/?series_id=all",
                 "https://www.vlr.gg/event/matches/2097/valorant-champions-2024/?series_id=all"
                 ]

filelist = []

#runs vlr_scraper for each one of those links
for link in list_of_links:
    string = 'python3 VLR_Stats_Scraper.py "' + link + '"'
    os.system(string)
    string2 = link.split("/")[6] + ".csv"
    filelist.append(string2)

#combines all the individual csv's from each instance into one big csv
df_list = []
i = 0
while(i < len(filelist)):
    df_list.append(pd.read_csv(filelist[i]))
    i = i + 1

merged = pd.concat(df_list)
merged.to_csv("final_stats.csv")
print("completed successfully")
