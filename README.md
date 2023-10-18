# Scrapper, Database and Dashboard for Geostatic
> Note: The project is in 1.0 Version and in constant progress, but i already use it for my development in Geostatic game, if you want to utilize yourself remember to adjust the components to your screen
### Geostatic Analytics

This project includes a scrapper of data via screenshot of results page of geostatic games, a database for the games and a dashboard for analysis of my games and better improvement

### How it works.

-You have a bind to screenshot your screen and save it in a folder
-The screenshots are then taken to text-image recognition, and save it useful(and curious) data in databases, then move the screenshots to a backup folder
-The data is displayed in a dashboard with a country base customization

### Database

-Table of rounds
-Table of trainings
-View for analysis

![Alt text](https://prnt.sc/_Pce6kmndPyB)
![Alt text](https://prnt.sc/HWNG9gbulkOT)
![Alt text](https://prnt.sc/kbLWwsK0KYly)

## Tech
- Python
- mysql
- Tkinter
- Pandas 
- matplotlib
- seaborn
- os
- pynput
- pyautogui

## FAQ

1. Why python? It's meant to be an analytics application, so python with pandas is a great solution
2. Will the charts broke if low database inputs? It won't be useful but it won't break, it's a personal dashboard at first


```sh
pip install pyinstaller
pyinstaller screenshots.py --onefile
pyinstaller saveData.py --onefile
pyinstaller showData.py --onefile
```

## TODO
- Make charts size flexible
- Fix the change of training on the dashboard
- When the screenshot is taken, show charts of the country
- Make funny charts of the temperature and city
- Delete older chart for specific chart in the dashboard
- Show absolute numbers in percentage charts
- Show max streak for either overall and specific country
- Update in real time charts
- Create other project for distance mode in geostatic
