import requests
import json

#############################################################################
## Networking

URL = 'https://api.fortnitetracker.com/v1/profile/{}/{}'
## URL =  'https://api.fortnitetracker.com/v1/challenges'

headers = {'TRN-Api-Key' : '31b3b777-f324-4650-8719-69652a8fa491'}

## Defautl Settings
keysForMainStats = ['Score', 'Matches Played','Wins', 'Kills', 'Time Played']
platforms = ['psn', 'xbl', 'pc']


platform = platforms[0]
name = 'mba_53'

## Build stats_dict
response = requests.get(URL.format(platform, name.strip()), headers=headers)
response_json = response.json()



#############################################################################
## App

class PlayerStats(object):
	"""docstring for PlayerStats"""
	
	def __init__(self, name, playerInfo, lifetimeStats, totalStats, currentSeasonStats):
		super(PlayerStats, self).__init__()
		self.name = name
		self.playerInfo = playerInfo
		self.lifetimeStats = lifetimeStats 
		self.totalStats = totalStats
		self.currentSeasonStats = currentSeasonStats

	def __str__(self):
		str = 'Name: {}"\n"'.format(self.name)
		str += 'Player Info: {}"\n"'.format(self.playerInfo)
		str += 'Lifetime Stats: {}"\n"'.format(self.lifetimeStats)
		str += 'Total Stats: {}"\n"'.format(self.totalStats)
		str += 'Currrent Season Stats: {}"\n"'.format(self.currentSeasonStats)
		return str

	

	
'''  Parse all stats from stats dictionary 
'''
def parsePlayerStats(stats):

	parsePlayerInfo(response_json)
	parseLifetimeStats(response_json)
	parseGameModesStats(response_json)


'''  Parse player info keys from stats dictionary 
'''
def parsePlayerInfo(stats):

	tmp = {}
	keysToParse = ['epicUserHandle', 'platformName', 'accountId']

	for key in keysToParse:

		if key in stats:
			tmp[key] = stats[key]
			

	return tmp


'''  Parse lifetime stats dictionary from stats dictionary 
'''
def parseLifetimeStats(stats):

	lifeTimeStats = []
	tmp = {}

	keysToParse = ['Kills', 'Score', 'Wins', 'Matches Played']

	if 'lifeTimeStats' in stats:
		lifeTimeStats = stats['lifeTimeStats']
		
		for stat in lifeTimeStats:
			
			key = stat['key']
			value = stat['value'].replace(",", "")

			if key in keysToParse:
				tmp[key] = value

	return tmp


'''  Parse all mage mode stats from stats dictionary 
'''
def parseGameModesStats(mode, stats):

	parseGameModesStats = []
	tmp = {}
	

	keysToParseTotal = []

	if mode == 'totals': 
		keysToParseTotal = ['p2', 'p10', 'p9']
	elif mode == 'current':
		keysToParseTotal = ['curr_p2', 'curr_p10', 'curr_p9']

	if 'stats' in stats:

		parseGameModesStats = stats['stats']

		## Total stats
		for key in keysToParseTotal:
			if key in parseGameModesStats:

				##print(parseGameModesStats[key])

				if key == 'p2' or 'curr_p2':
					tmp['Solos'] = parseUnits(parseGameModesStats[key], ['kills', 'score', 'matches', 'top1', 'top10', 'top25'])
				if key == 'p10' or 'curr_p10':
					tmp['Duos'] = parseUnits(parseGameModesStats[key], ['kills', 'score', 'matches', 'top1', 'top5', 'top12'])
				if key == 'p10' or 'curr_p9':
					tmp['Squads'] = parseUnits(parseGameModesStats[key], ['kills', 'score', 'matches', 'top1', 'top3', 'top6'])

	
	return tmp


def parseUnits(stats, keysToParse):

	tmp = {}

	for key in keysToParse:
		if key in stats:
			if key == 'top1':
				tmp['Wins'] = stats[key]['value']
			else:
				tmp[key.capitalize()] = stats[key]['value']

	return tmp





## App Starts Here
## Main
if __name__ == '__main__':

	player = PlayerStats("MBA_53", {}, {}, {}, {})
	## parsePlayerStats(response_json)
	player.playerInfo = parsePlayerInfo(response_json)
	player.lifetimeStats = parseLifetimeStats(response_json)
	player.totalStats = parseGameModesStats('totals', response_json)
	player.currentSeasonStats = parseGameModesStats('current', response_json)
	
	
	print(player)
	print(json.dumps(player.__dict__))
