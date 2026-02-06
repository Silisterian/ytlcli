# 🎵 ytl (YouTube Library Interface)

**ytl** is a lightweight, high-performance Command Line Interface (CLI) designed to search, play, and manage YouTube music and playlists directly from your terminal. 
## 🛠️ Commands

### Search
| Command | Description |
| :--- | :--- |
| `search <query>` | Search for a specific track |
| `/ <query>` | Shortcut for search |
| `search pl <url>` | Search and import a YouTube playlist via URL |

### Playback
| Command | Description |
| :--- | :--- |
| `play` | Start or resume playback |
| `play pl <name> [rnd]` | Play a saved playlist (optional: `rnd` for shuffle) |
| `pause` / `resume` | Control current playback |
| `skip` | Play the next song in queue |
| `stop` | Stop playback and close stream |
| `volume <0-100>` | Set playback volume |

### Management
| Command | Description |
| :--- | :--- |
| `ls queue` | Display current queue |
| `ls pl` | List all saved local playlists |
| `clear` | Wipe the current queue |
| `pl save <url> <name>` | Import a YT playlist to local storage |
| `pl add current <plname>` | Add the active song to a playlist |
| `pl rm <name>` | Delete a local playlist |