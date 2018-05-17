import datetime, requests, json, os
from bs4 import BeautifulSoup

class Matches:
    def __init__(self):
        self.matchstatus = []
        self.matchlinks_um = []
        self.matchlinks_lm = []
        self.matchlinks_rts = []
        self.teamNames = []
        self.dates = []
        self.events = []
        self.clocks = []
        self.bestof = []
        self.teamLogos = []
        self.match = {}
    def source (self, link):
        self.r = requests.get(link)
        self.sauce = self.r.content
        self.soup = BeautifulSoup(self.sauce, 'lxml')

    def matchdump (self):

        self.match[str(self.teamA[self.number]) + 'vs' + str(self.teamB[self.number])] = {
            'matches': [
                {
                    'team1': str(self.teamA[self.number]),
                    'team2': str(self.teamB[self.number]),
                    'eventname': str(self.events[self.number]),
                    'date': str(self.dates[self.number]),
                    'clock': str(self.clocks[self.number]),
                    'team1logo': str(self.teamAlogo[self.number]),
                    'team2logo': str(self.teamBlogo[self.number]),
                    'bo': str(self.bestof[self.number]),
                    'status': str(self.matchstatus[self.number])
                }
        ]
        }

        self.dump = json.dumps(self.match[str(self.teamA[self.number]) + 'vs' + str(self.teamB[self.number])], indent=2)
        with open(os.getcwd() + '/match.txt', 'a') as self.f:
            self.f.write(self.dump)

    def todaymatches(self):
        print('\nTHESE ARE TODAY\'S UPCOMING MATCHES\n')
        self.source('https://hltv.org/matches')

        for self.links in self.soup.find(class_="standard-headline",
                                         text=(datetime.date.today())).find_parent().find_all(class_="upcoming-match"):
            if self.links is None:
                print('There isn\'t any upcoming match.')
            else:
                self.matchlinks_um.append('https://hltv.org' + self.links.get('href'))
        self.lenlist = len(self.matchlinks_um)
        if self.lenlist >= 1:
            for self.x in range(len(self.matchlinks_um)):
                self.source(self.matchlinks_um[self.x])
                self.time_class = self.soup.find('div', class_='time')['data-unix']
                self.clock = datetime.datetime.fromtimestamp(int(self.time_class[:10])).time()
                if str(self.clock) != '00:00:00':
                    for self.tn in self.soup.find_all('div', class_='teamName'):
                        self.teamNames.append(self.tn.text)
                    self.date = self.soup.find('div', class_='date').text
                    self.dates.append(self.date)
                    self.eventname = self.soup.find('div', class_='event text-ellipsis').text
                    self.events.append(self.eventname)
                    self.clocks.append(self.clock)
                    for self.lg in self.soup.find_all('img', class_='logo'):
                        self.teamLogos.append(self.lg.get('src'))
                    self.maps = self.soup.find('div', class_='padding preformatted-text').text
                    self.bestof.append(self.maps[:9])
                    self.matchstatus.append('UPCOMING')
                else:
                    pass

            self.teamA = self.teamNames[0::2]
            self.teamB = self.teamNames[1::2]
            self.teamAlogo = self.teamLogos[0::2]
            self.teamBlogo = self.teamLogos[1::2]

            for self.number in range(len(self.dates)):
                print(self.teamA[self.number], 'vs', self.teamB[self.number], 'on', self.dates[self.number], 'at',
                      self.clocks[self.number], self.events[self.number], self.bestof[self.number])
                self.matchdump()
            print('All matches are dumped. You can pull the match infos from txt file.')
            print('Matches are dumped as dictionary.')
        else:
            pass
    def livematches(self):
        print('\nTHESE ARE LIVE MATCHES\n')
        self.source('https://hltv.org/matches')

        for self.links in self.soup.find('div', class_='live-matches').find_all('a'):
            if self.links is None:
                print('There isn\'t any live match.')
            else:
                self.matchlinks_lm.append('https://hltv.org' + self.links.get('href'))
        self.lenlist = len(self.matchlinks_lm)
        if self.lenlist >= 1:
            for self.x in range(len(self.matchlinks_lm)):
                self.source(self.matchlinks_lm[self.x])
                self.time_class = self.soup.find('div', class_='time')['data-unix']
                self.clock = datetime.datetime.fromtimestamp(int(self.time_class[:10])).time()
                for self.tn in self.soup.find_all('div', class_='teamName'):
                    self.teamNames.append(self.tn.text)
                self.date = self.soup.find('div', class_='date').text
                self.dates.append(self.date)
                self.eventname = self.soup.find('div', class_='event text-ellipsis').text
                self.events.append(self.eventname)
                self.clocks.append(self.clock)
                for self.lg in self.soup.find_all('img', class_='logo'):
                    self.teamLogos.append(self.lg.get('src'))
                self.maps = self.soup.find('div', class_='padding preformatted-text').text
                self.bestof.append(self.maps[:9])
                self.matchstatus.append('LIVE')

            self.teamA = self.teamNames[0::2]
            self.teamB = self.teamNames[1::2]
            self.teamAlogo = self.teamLogos[0::2]
            self.teamBlogo = self.teamLogos[1::2]

            for self.number in range(len(self.dates)):
                print(self.teamA[self.number], 'vs', self.teamB[self.number], 'on', self.dates[self.number], 'at',
                      self.clocks[self.number], self.events[self.number], self.bestof[self.number])
                self.matchdump()
            print('All matches are dumped. You can pull the match infos from txt file.')
            print('Matches are dumped as dictionary.')
        else:
            pass

    def results(self):
        print('\nTHESE ARE LAST 1 DAY\'S MATCH RESULTS\n')
        self.source('https://hltv.org/results')

if os.path.isfile(os.getcwd() + '/match.txt'):
    os.remove(os.getcwd() + '/match.txt')
else:
    pass
Matches().livematches()
Matches().todaymatches()