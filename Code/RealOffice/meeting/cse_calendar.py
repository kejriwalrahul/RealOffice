
# python imports 
import json
import schedule
import time
import datetime
from time import gmtime, strftime

# import the csv 
# read the details 
# send it to the meeting calendar
# generate meetings

def fill_calendar():
    print("Filling calendar...")
    
    date_str = strftime("%Y-%m-%d")    
    filename = date_str + ".json"
    
    #print filename
    meetings = []
    with open (filename) as f:
        for line in f:
            meetings.append(json.loads(line))
            
    num_meetings = len(meetings)
    
    for i in range( num_meetings):
        meeting_data = meetings[i]
        
        '''
        response = self.rest_client.post('/meeting/add/', {
			'name':meeting_data["name"],
			'organizer':meeting_data["organizer"],
			'venue' : meeting_data["venue"],
			'participants' : meeting_data["participants"],
			'date' : meeting_data["date"],
			'stime' : meeting_data["stime"],
			'etime' :meeting_data["etime"],
			'workflow' : meeting_data["workflow"]
		})

		self.assertEqual(response.status_code, 200)	
		if 'error' in response.content:
			self.fail("Error: " + response.data['error'])
			
		'''
         
schedule.every(2).seconds.do(fill_calendar)
schedule.every().day.at("08:00").do(fill_calendar)

while True:
    schedule.run_pending()
    time.sleep(1)


