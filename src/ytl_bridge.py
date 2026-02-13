import json
import sys
import os
from ytmanager import YTManager

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))


yt = YTManager()

def get_data_dir():
    if os.name == 'nt':  # Windows
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:  # Linux/Mac
        base = os.path.join(os.path.expanduser('~'), '.config')
    
    data_dir = os.path.join(base, 'ytl-player')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_playlist_path():
    return os.path.join(get_data_dir(), 'playlist.json')

# Charger ou créer
def load_playlists():
    path = get_playlist_path()
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump({}, f)
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def handle_command(cmd):
    action = cmd.get("action")
    data = None
    if cmd.get('data'):
        data=cmd.get('data')
    returnlist = {}
    returnlist['action']= action
    if action == "get_playlists":
        returnlist['data'] = list(yt.playlists)
        print(returnlist)
        return returnlist
    elif action == "get_media_pl":
        videos = list(yt.fetch_playlistbyname(data))
        returnlist['data'] = yt.videoInfoToJson(videos)
        return returnlist
    



# to test run in cmd : echo '{"action": "get_playlists"}' | python src/ytl_bridge.py
for line in sys.stdin:
    try:
        cmd = json.loads(line.strip())
        result = handle_command(cmd)
        print(json.dumps(result), flush=True)
    except Exception as e:
        print(json.dumps({"error": str(e)}), flush=True)