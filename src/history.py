import selenium.webdriver
import time
from selenium.webdriver.chrome.options import Options
from datetime import timedelta, datetime
import time
import pandas as pd


def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " ---"


def print_custom(string_input):
    print(current_datetime(), string_input)


years = ["2015", "2016", "2017", "2018", "2019", "2020"]
# years = ["2015"]

chrome_options = Options()
chrome_options.add_argument("window-size=1920,600")

print_custom("Set up driver")

driver = selenium.webdriver.Chrome(
    executable_path=r"C:\Users\hmand\OneDrive\Documents\GitHub\butt-munchers\chromedriver.exe",
    options=chrome_options,
)

print_custom("Go to login page")
driver.get(
    "https://fantasy.espn.com/football/league/schedule?leagueId=189512&seasonId=2015"
)
time.sleep(5)

print_custom("Switch to iframe")
iframe = driver.find_element_by_xpath("//iframe[@id='disneyid-iframe']")
driver.switch_to.frame(iframe)
time.sleep(2)

print_custom("Enter login credentials")
driver.find_element_by_xpath("//input[@ng-model='vm.username']").send_keys(
    "hmandsager@yahoo.com"
)
driver.find_element_by_xpath("//input[@ng-model='vm.password']").send_keys(
    "FuckWelter16"
)
driver.find_element_by_xpath("//button[@ng-click='vm.submitLogin()']").click()
time.sleep(5)

print_custom("Switch to window")
main_page = driver.current_window_handle
driver.switch_to.window(main_page)

driver.get(
    "https://fantasy.espn.com/football/league/schedule?leagueId=189512&seasonId=2015"
)

print_custom("Loop")
games = []

for year in years:
    new_url = (
        r"https://fantasy.espn.com/football/league/schedule?leagueId=189512&seasonId="
        + year
    )
    driver.get(new_url)
    time.sleep(2)

    for game in driver.find_elements_by_class_name("matchup--table"):
        title = game.find_element_by_class_name("table-caption").text
        company = game.text
        print(title)

        for row in game.find_elements_by_class_name("Table__TR"):

            num_team_names = 0
            num_team_managers = 0
            num_scores = 0

            team_name_1 = ""
            team_name_2 = ""
            team_managers_1 = ""
            team_managers_2 = ""
            score_1 = 0
            score_2 = 0

            for td in row.find_elements_by_class_name("Table__TD"):
                try:
                    team_name = td.find_element_by_class_name("teamName").text
                    num_team_names += 1

                    if num_team_names == 1:
                        team_name_1 = team_name
                    else:
                        team_name_2 = team_name
                except:
                    err = ""

                try:
                    team_managers = td.find_element_by_class_name("team-owner-col").text
                    num_team_managers += 1

                    if num_team_managers == 1:
                        team_managers_1 = team_managers
                    else:
                        team_managers_2 = team_managers
                except:
                    err = ""

                try:
                    score = td.find_element_by_class_name("result-column").text
                    num_scores += 1

                    if num_scores == 1:
                        score_1 = score
                    else:
                        score_2 = score
                except:
                    err = ""

            if score_1 > score_2:
                result_1 = "W"
                result_2 = "L"
            else:
                result_1 = "L"
                result_2 = "W"

            games.append(
                [
                    year,
                    title,
                    team_name_1,
                    team_managers_1,
                    score_1,
                    result_1,
                    team_managers_2,
                    score_2,
                ]
            )
            games.append(
                [
                    year,
                    title,
                    team_name_2,
                    team_managers_2,
                    score_2,
                    result_2,
                    team_managers_1,
                    score_1,
                ]
            )


df = pd.DataFrame(
    games,
    columns=[
        "Year",
        "Title",
        "Team Name",
        "Managers",
        "Score",
        "Result",
        "Opponent",
        "Opponent Score",
    ],
)
# print(df)

save_name = r"C:\Users\dopland\OneDrive - Guidehouse\Desktop\ffresults.csv"

df.to_csv(save_name)

print_custom("Done")
