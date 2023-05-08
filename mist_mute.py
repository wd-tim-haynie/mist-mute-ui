import requests
from os import getenv
from datetime import datetime

murl = 'https://api.mist.com/api/v1'
my_headers = {"Authorization": f"Token {getenv('MIST_TOKEN')}",
              "Content-Type": "application/json"}
sesh = requests.Session()
orgid = sesh.get(f"{murl}/self", headers=my_headers).json()['privileges'][0]['org_id']

def get_sites():
    url = f"{murl}/orgs/{orgid}/sites"
    sites_list = sesh.get(url, headers=my_headers).json()
    sites_list.sort(key=lambda x: x['name'])
    return sites_list

def get_active_mutes():
    url = f"{murl}/orgs/{orgid}/alarmtemplates/suppress"
    req = sesh.get(url, headers=my_headers)
    mutes = []

    if req.json()['results']:
        for mute in req.json()['results']:
            start_time_str = epoch_to_human(mute['scheduled_time'])
            is_currently_muted = mute['scheduled_time'] < datetime.now().timestamp()
            end_time_epoch = (
                datetime.now().timestamp() + mute['duration']
                if is_currently_muted
                else mute['scheduled_time'] + mute['duration']
            )
            end_time_str = epoch_to_human(end_time_epoch)
            mute_status = (
                "Scheduled"
                if mute['scheduled_time'] > datetime.now().timestamp()
                else "Muted Now"
            )
            mutes.append({
                'site_id': mute['site_id'],
                'start_time': start_time_str,
                'end_time': end_time_str,
                'mute_status': mute_status
            })

    return mutes

def add_mute(site_id, start_time, duration):
    url = f"{murl}/orgs/{orgid}/alarmtemplates/suppress"
    my_params = {
        "duration": duration,
        "applies": {
            "site_ids": [site_id]
        }
    }

    if start_time:
        start_time_obj = datetime.fromisoformat(start_time)
        my_params["scheduled_time"] = start_time_obj.timestamp()

    sesh.post(url, headers=my_headers, json=my_params)

def epoch_to_human(epoch):
    datetime_obj = datetime.fromtimestamp(epoch)
    human_readable_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S ")
    return human_readable_time + datetime.now().astimezone().tzname()
