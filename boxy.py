import requests
import csv
import datetime
import os

def fetch_nfl_box_scores():
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def parse_box_scores(data):
    box_scores = []
    events = data.get('events', [])
    
    for event in events:
        competition = event.get('competitions', [])[0]
        status = competition.get('status', {}).get('type', {}).get('description', 'N/A')
        
        for competitor in competition.get('competitors', []):
            team = competitor.get('team', {})
            score = competitor.get('score', '0')
            
            scores_by_quarter = {
                'Q1': competitor.get('linescores', [{}])[0].get('value', '0') if len(competitor.get('linescores', [])) > 0 else '0',
                'Q2': competitor.get('linescores', [{}])[1].get('value', '0') if len(competitor.get('linescores', [])) > 1 else '0',
                'Q3': competitor.get('linescores', [{}])[2].get('value', '0') if len(competitor.get('linescores', [])) > 2 else '0',
                'Q4': competitor.get('linescores', [{}])[3].get('value', '0') if len(competitor.get('linescores', [])) > 3 else '0',
            }
            
            box_scores.append({
                'Team': team.get('displayName', 'N/A'),
                'Score': score,
                'Q1': scores_by_quarter['Q1'],
                'Q2': scores_by_quarter['Q2'],
                'Q3': scores_by_quarter['Q3'],
                'Q4': scores_by_quarter['Q4']
            })
    
    return box_scores

def write_box_scores_to_csv(box_scores, filename='nfl_box_scores.csv'):
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        fieldnames = ['Team', 'Score', 'Q1', 'Q2', 'Q3', 'Q4']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for box_score in box_scores:
            writer.writerow(box_score)

def update_weekly_box_scores():
    data = fetch_nfl_box_scores()
    if data:
        box_scores = parse_box_scores(data)
        write_box_scores_to_csv(box_scores)

if __name__ == "__main__":
    # Schedule this script to run weekly, e.g., using cron or Windows Task Scheduler
    update_weekly_box_scores()