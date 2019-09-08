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
    
    resp_dict = {}

    resp_dict['fetch_time'] = str(datetime.now())
    resp_dict['rank_value'] = q["ranks"][0]["rank"]
    resp_dict['username']   = q["ranks"][0]["username"]
    
    if resp_dict['rank_value'] > rank_threshold:
        resp_dict['season_reset'] = False
    else:
        resp_dict['season_reset'] = True 
    
    return resp_dict

def web_season_status():
    resp_dict = get_season_status()

    web_page_str = '''
    <html>
        <body>
            <h3>Season reset status : {}</h3><br><br>
            Trophies : {}<br>
            Name : {}<br>
            Rank : {}<br>
            Data fetch time : {}<br>
            Timezone : {}
        </body>
    </html>
    '''.format(resp_dict['season_reset'], resp_dict['rank_value'], resp_dict['username'], 1, resp_dict['fetch_time'], time.tzname[1])

    return web_page_str

def show_default_page():
    web_page_str = '''
    <html>
        <body>
            YES, THIS PAGE WORKS TOO, UNLIKE CHEETAH<br>
            --xavier666
        </body>
    </html>
    '''
    return web_page_str
def main():
    bottle.route("/", method='GET')(show_default_page)
    bottle.route("/season_status", method='GET')(web_season_status)
    
    bottle.run(host = "0.0.0.0", port = int(os.environ.get("PORT", 10000)), debug = False)

if __name__ == '__main__':
    main()
