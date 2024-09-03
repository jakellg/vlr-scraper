# VLR_Scraper_Merger
This is a program that Scrapes [VLR](https://www.vlr.gg/)

All data is per player per map to give a level of granularity to be able to calculate deeper statistics than just averages.

final_stats.csv is an example of what the data for all franchising events looks like.

# Getting Started

To run this program all you need is a link to the VLR matches page with the data you want to scan. This can be either a team, a player or tournament. For teams and players, you may also specify how many matches you want out of the last 50.

# Examples

This will scan the last 20 LOUD games, and produce a file "loud.csv":
```{python}
VLR_Stats_Scraper.py "https://www.vlr.gg/team/matches/6961/loud/" 20
```

This will scan the last 15 Zellsis games, and produce a file "zellsis.csv":
```{python}
VLR_Stats_Scraper.py "https://www.vlr.gg/player/matches/729/zellsis" 15
```

This will scan through all the matches at Champions 2024, and produces document  "valorant-champions-2024.csv":
```{python}
VLR_Stats_Scraper.py "https://www.vlr.gg/event/matches/2097/valorant-champions-2024/?series_id=all"
```

This program contains a list of all Franchised Valorant events, goes through all of them and creates a file "final_stats.csv" (included in this repository):
```{python}
VLR_Scraper_Merger.py 
```

# Missing Data

As of publishing, Riots api does not work for events held in China or for matches that crash mid game. This program will collect what data it can, but there will be quite a bit of missing data.

# Known Issues

There is currently an issue where the program cannot handle best of 1 matches

For the team & player scanners, the highest number of matches the program can go back is only 50. A fix is in the works, but for now you can manually copy links to page 2, 3... etc of the site and merge the data if you need more than 50 matches.
