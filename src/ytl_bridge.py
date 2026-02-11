import json
import sys
from ytmanager import YTManager

yt = YTManager()

def handle_command(cmd):
    action = cmd.get("action")
    if action == "get_playlists":
        return list(yt.playlists.keys())
    
for line in sys.stdin:
    try:
        cmd = json.loads(line.strip())
        result = handle_command(cmd)
        print(json.dumps(result), flush=True)
    except Exception as e:
        print(json.dumps({"error": str(e)}), flush=True)