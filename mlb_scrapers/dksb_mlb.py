import requests

from datetime import datetime
from bs4 import BeautifulSoup
from utils.utils import Webpage


class ScrapeDKBases():
    """
    A class of functions to scrape MLB lines and odds on DraftKings Sportsbook.
    """

    def soup_setup(self, url):
        """
        Create a BeautifulSoup object from the given url.
        Should return <Response [200]>, unless there is an error.
        """
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup

    def team_cleanup(self, tm_name):
        """
        Takes an MLB team name from DraftKings and converts it to FanGraphs' format.
        """
        annoying = {'WAS Nationals': 'WSN', 'CHI White Sox': 'CHW', 'CHI Cubs': 'CHC'}
        names = tm_name.split()
        if tm_name in annoying:
            city = annoying[tm_name]
        elif len(names[0]) == 2:
            city = f'{names[0]}{names[1][0]}'
        else:
            city = names[0]

        return city

    def mlb_ws(self):
        """
        Scrapes current World Series odds.
        
        Returns
        -------
        lamarca : nested dictionaries in the form of
        {<team abbreviation>: {'odds':<odds>, 'date_time':<datetime object with the current date and time>}, ...}

        """
        soup_today = self.soup_setup(
            f"https://sportsbook.draftkings.com/leagues/baseball/2003?category=team-futures&subcategory=world-series-2021")

        teams = []
        team_soup = soup_today.findAll('span', {'class': 'sportsbook-outcome-cell__label'})
        for i in team_soup:
            # Teams are listed on DK as <city abbreviation> <team nickname> so
            # we want to format team abbreviations to match FanGraphs' convention:
            city = self.team_cleanup(i.text)
            # Once the abbrevations are cleaned up, add them to a list:
            teams.append(city)

        odds = []
        odds_soup = soup_today.findAll('span', {'class': 'sportsbook-odds american default-color'})
        for i in odds_soup:
            odd = i.text
            odd = int(odd.replace('+', ''))
            # Once odds have been cleaned up, convert them to percentages (easier to understand and/or plot):
            if odd > 0:
                pct = round(1 / ((odd / 100) + 1), 4)
            else:
                pct = round(1 - (1 / ((-1 * odd / 100) + 1)), 4)
            # Add percentages to a list:
            odds.append(pct)

        # Add team abbreviations, odds and the current date and time to nested dictionaries:
        lamarca = {}
        # Of course, World Series winners probably aren't celebrating with $14 bottles of lamarca but it's some damn
        # good prosecco.
        for i in range(len(teams)):
            lamarca[teams[i]] = {'odds': odds[i], 'date_time': datetime.now()}

        return lamarca

    def mlb_games(self):
        """
        Scrapes current MLB game odds.

        Returns
        -------
        games : dictionary containing teams, moneylines, totals, runlines and opponents.

        """

        markets = Webpage('mlb').pull_data()

        games = {}
        for i in markets:
            away_team = self.team_cleanup(i[2]['outcomes'][0]['label'])
            home_team = self.team_cleanup(i[2]['outcomes'][1]['label'])

            if away_team not in games:
                games[away_team] = {}
                try:
                    games[away_team]['moneyline'] = i[2]['outcomes'][0]['oddsAmerican']
                    games[away_team]['moneyline_decimal'] = i[2]['outcomes'][0]['oddsDecimal']
                    games[away_team]['moneyline_fractional'] = i[2]['outcomes'][0]['oddsFractional']
                except Exception as e:
                    print(f"error with moneyline {e} in game {home_team} vs {away_team}")
                try:
                    games[away_team]['runline'] = [i[0]['outcomes'][0]['line'],
                                                   i[0]['outcomes'][0]['oddsAmerican']]
                    games[away_team]['runline_decimal'] = [i[0]['outcomes'][0]['line'],
                                                           i[0]['outcomes'][0]['oddsDecimal']]
                    games[away_team]['runline_fractional'] = [i[0]['outcomes'][0]['line'],
                                                              i[0]['outcomes'][0]['oddsFractional']]
                except Exception as e:
                    print(f"error with run line {e} in game {home_team} vs {away_team}")
                try:
                    games[away_team]['over'] = [i[1]['outcomes'][0]['line'],
                                                i[1]['outcomes'][0]['oddsAmerican']]
                    games[away_team]['over_decimal'] = [i[1]['outcomes'][0]['line'],
                                                        i[1]['outcomes'][0]['oddsDecimal']]
                    games[away_team]['over_fractional'] = [i[1]['outcomes'][0]['line'],
                                                           i[1]['outcomes'][0]['oddsFractional']]
                except Exception as e:
                    print(f"error with over {e} in game {home_team} vs {away_team}")
                try:
                    games[away_team]['under'] = [i[1]['outcomes'][1]['line'],
                                                 i[1]['outcomes'][1]['oddsAmerican']]
                    games[away_team]['under_decimal'] = [i[1]['outcomes'][1]['line'],
                                                         i[1]['outcomes'][1]['oddsDecimal']]
                    games[away_team]['under_fractional'] = [i[1]['outcomes'][1]['line'],
                                                            i[1]['outcomes'][1]['oddsFractional']]
                except Exception as e:
                    print(f"error with under {e} in game {home_team} vs {away_team}")

                games[away_team]['opponent'] = home_team

            if home_team not in games:
                games[home_team] = {}
                try:
                    games[home_team]['moneyline'] = i[2]['outcomes'][1]['oddsAmerican']
                    games[home_team]['moneyline_decimal'] = i[2]['outcomes'][1]['oddsDecimal']
                    games[home_team]['moneyline_fractional'] = i[2]['outcomes'][1]['oddsFractional']
                except Exception as e:
                    print(f"error with moneyline {e} in game {home_team} vs {away_team}")
                try:
                    games[home_team]['runline'] = [i[0]['outcomes'][1]['line'],
                                                   i[0]['outcomes'][1]['oddsAmerican']]
                    games[home_team]['runline_decimal'] = [i[0]['outcomes'][1]['line'],
                                                           i[0]['outcomes'][1]['oddsDecimal']]
                    games[home_team]['runline_fractional'] = [i[0]['outcomes'][1]['line'],
                                                              i[0]['outcomes'][1]['oddsFractional']]
                except Exception as e:
                    print(f"error with run line {e} in game {home_team} vs {away_team}")
                try:
                    games[home_team]['over'] = [i[1]['outcomes'][0]['line'],
                                                i[1]['outcomes'][0]['oddsAmerican']]
                    games[home_team]['over_decimal'] = [i[1]['outcomes'][0]['line'],
                                                        i[1]['outcomes'][0]['oddsDecimal']]
                    games[home_team]['over_fractional'] = [i[1]['outcomes'][0]['line'],
                                                           i[1]['outcomes'][0]['oddsFractional']]
                except Exception as e:
                    print(f"error with over {e} in game {home_team} vs {away_team}")
                try:
                    games[home_team]['under'] = [i[1]['outcomes'][1]['line'],
                                                 i[1]['outcomes'][1]['oddsAmerican']]
                    games[home_team]['under_decimal'] = [i[1]['outcomes'][1]['line'],
                                                         i[1]['outcomes'][1]['oddsDecimal']]
                    games[home_team]['under_fractional'] = [i[1]['outcomes'][1]['line'],
                                                            i[1]['outcomes'][1]['oddsFractional']]
                except Exception as e:
                    print(f"error with under {e} in game {home_team} vs {away_team}")

                games[home_team]['opponent'] = away_team

        return games


def main():
    scrape = ScrapeDKBases()
    games = scrape.mlb_games()
    print(games)


if __name__ == '__main__':
    main()
