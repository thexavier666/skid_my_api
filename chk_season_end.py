#!/usr/bin/env python3

import time
import json
import requests
import os
import bottle

from datetime import datetime

def get_season_status():
	
	url_str = 'http://api.skidstorm.cmcm.com/v2/rank/list/1-1/ALL'
	rank_threshold = 11000
	
	p = requests.get(url_str)
	q = json.loads(p.text)
	
	rank_val = q["ranks"][0]["rank"]
	
	resp_dict = {'season_reset':'','current_time':str(datetime.now())}
	
	if rank_val > rank_threshold:
		resp_dict['season_reset'] = False
	else:
		resp_dict['season_reset'] = True 
	
	return resp_dict

def main():
	bottle.route("/season_status", method='GET')(get_season_status)

	if os.environ.get('APP_LOCATION') == 'heroku':
		print("At heroku")
		bottle.run(host = "0.0.0.0", port = int(os.environ.get("PORT", 5000)))
	else:
		bottle.run(host = "localhost", port = 8888, debug = True)

if __name__ == '__main__':
	main()
