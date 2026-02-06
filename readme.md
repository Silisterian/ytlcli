# 🎵 ytl (YouTube Library Interface)

**ytl** is a lightweight, high-performance Command Line Interface (CLI) designed to search, play, and manage YouTube music and playlists directly from your terminal. 

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Silisterian/ytl.git](https://github.com/silisterian/ytl.git)
    cd ytl
    ```

2.  **Install dependencies:**
    
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application from the directory**
    ```bash
    python main.py
    ```


3. **Run YTL from anywhere**

        ```bash
    pip install -e .
    ```

    open a new CMD

        ```bash
    ytl
        ```



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