import urllib.request
import urllib.parse
import re

def get_team_name( s ):
    # input an html line and get the name of the team
    # returns 'no team name!' if the value is empty
    try:
        first = '<title>'
        last = ' Statistics'
        start = s.index( first ) + len( first ) + 5
        end = s.index( last, start )
        if start >= end:
          return 'no team name!'
        else:
          return s[start:end]
    except ValueError:
        return ""

def get_player_name( s ):
    # input an html line and get the name of player
    # returns 'no name!' if the value is empty
    try:
        first = 'htm\">'
        last = '</a'
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        if start == end:
          return 'no name!' 
        else:
          return s[start:end]
    except ValueError:
        return ""

def find_html_value( s ):
    # input an html line and get the int value from that line
    # returns 0 if the value is empty
    try:
        first = ' >'
        last = '</td'
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        if start == end:
          return 0
        else:
          return int(s[start:end])
    except ValueError:
        return ""

# define the wholePage of teams
teams = ['nwe', 'mia', 'buf', 'nyj', 'nyg', 'dal', 'phi', 'was', 'chi', 'crd', 'atl', 'rav', 'car', 'cle', 'cin', 'den', 'det', 'gnb', 'htx', 'clt', 'jax', 'min', 'nor', 'rai', 'pit', 'sdg', 'sfo', 'sea', 'ram', 'tam', 'oti']

# testing out teams without running through the whole thing
#teams = ['nyj','nyg']

# define an empty wholePage where you will put all the teams that fit your criteria
answers = []

# define a "section" bit which tells you whether you have entered the correct section of the html
#  (otherwise you may pick up stats from tables you did not intend)
section = False

# Double for loop to go through all the teams and years you want to check
for team in teams:
  for year in range(2011,2014):
    
    # reset teamname
    teamname = ''

    # built the url for each team page
    url = 'http://www.pro-football-reference.com/teams/' + team + '/' + str(year) + '.htm'

    # found this was a good place to test if you are getting the right urls
    # print(url)
    
    # open the url
    html = urllib.request.urlopen(url)
    
    # read the html into a single string, then decode, get the total newlines, then put each line into a wholePage of strings
    raw = html.read()
    raw = raw.decode()
    n = raw.count('\n')
    wholePage = raw.split('\n')

    # check to see if this is actually a page (there is no 1983 Jackonsville Jaguars team!)
    #  if not, then just skip this section and move on to the next team
    if 'File Not Found' not in wholePage[5]: 

      # define a list of WR
      wrList = []

      # sequentially go through each line in the file
      for x in range(0,n):

        # get the team name
        if "<title>" in wholePage[x]:
          teamname = get_team_name(wholePage[x])

        # set our "section" bit value based on where we are in the file
        #   I suppose it would be a bit more efficient to use the string matching here to actually define start and end points
        #   as that would avoid parsing the entire page, at least from the end point to the end of the page
        if "stw clear_both\" id=\"all_rushing_and_receiving" in wholePage[x]:
          section = True
        if "stw clear_both\" id=\"all_returns" in wholePage[x]:
          section = False

        # check to see if we are in the section, and whether the player is defined as a WR
        #   if so, add his yardage and name to the WR list
        #     yardage is 11 lines down from WR line, so that's why there is a +11 offset 
        #     the name is 2 lines above the WR line, so that's why there is a -2 offset
        if section and ("<td align=\"left\" >wr</td>" in wholePage[x] or "<td align=\"left\" >WR</td>" in wholePage[x] or  "<td align=\"left\" >PR/WR</td>" in wholePage[x]):
          wrList.append([find_html_value(wholePage[x+11]),get_player_name(wholePage[x-2])])

      # some pages had one WR or even none, so check to make sure there are at least 2
      if len(wrList) >= 2:

        # this was another good point to print out your progress in testing
        # print(wrList)

        # create a 2 value list of the top 2 receivers, then add their yardage together
        top2 = sorted(wrList, reverse=True)[:2]
        total = top2[0][0] + top2[1][0]

        # set the yardage cut off you want to use, then add all the data to the answers list
        if total > 2700:
          answers.append([total,url,teamname,top2,year])


# Sort the answers based off total, then display the list in a readable format
sortAnswers = sorted(answers, reverse=True)
for x in range(0,len(sortAnswers)):
  print(str(x+1) + '. ' + str(sortAnswers[x][0]) + ', ' + sortAnswers[x][3][0][1] + ' - ' + sortAnswers[x][3][1][1] + ' (' + str(sortAnswers[x][4]) + ' ' + sortAnswers[x][2] + ')')
