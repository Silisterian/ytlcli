from ytmanager import YTManager

def display_welcome_message():
    print("Welcome to YTLCLI - Your YouTube Command Line Interface!")
    print("Type 'help' to see available commands.")
    print("Type 'exit' to quit the application.")
    print()


def display_help():
    # Codes couleurs ANSI
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    GRAY = "\033[90m"

    help_text = f"""
{BOLD}{CYAN}======================= 🎵 HELP MENU YTL 🎵 ======================={RESET}

  {BOLD}🔍 SEARCH{RESET}
    {BLUE}search <query>{RESET}                {GRAY}# Search for a track{RESET}
    {BLUE}/ <query>{RESET}                     {GRAY}# Search shortcut{RESET}
    {BLUE}search pl <url>{RESET}               {GRAY}# Search/Import playlist via URL{RESET}

  {BOLD}📜 QUEUE & HISTORY{RESET}
    {BLUE}ls queue{RESET}                      {GRAY}# Show current queue{RESET}
    {BLUE}ls played{RESET}                     {GRAY}# Show playback history{RESET}
    {BLUE}ls pl{RESET}                         {GRAY}# List all saved playlists{RESET}
    {BLUE}clear{RESET}                         {GRAY}# Clear the current queue{RESET}

  {BOLD}▶️  PLAYBACK{RESET}
    {BLUE}play{RESET}                          {GRAY}# Start or resume playback{RESET}
    {BLUE}play pl <name> <rnd>{RESET}          {GRAY}# Play a playlist (<rnd>: true/false){RESET}

  {BOLD}📂 PLAYLIST MANAGEMENT{RESET}
    {BLUE}pl mk <name>{RESET}                   {GRAY}# Create an empty playlist{RESET}
    {BLUE}playlist <mk|save> <url> <name>{RESET}   {GRAY}# Import/Save playlist from URL{RESET}
    {BLUE}pl add <current|queue> <plname>{RESET} {GRAY}# Add track(s) to a playlist{RESET}
    {BLUE}pl ls <name>{RESET}                   {GRAY}# View specific playlist content{RESET}
    {BLUE}pl edit <name>{RESET}                 {GRAY}# Edit/Rename a playlist{RESET}
    {BLUE}pl rm <name>{RESET}                   {GRAY}# Delete a playlist{RESET}

{BOLD}{CYAN}=================================================================={RESET}
"""
    print(help_text)



def main():
    display_welcome_message()
    yt_manager = YTManager()
    state = True
    while state: 
        cmd = input("ytlcli> ")
        arguments = cmd.split(' ', 3)
        if arguments[0] == "help":
            display_help()
        elif arguments[0] in ["exit", "quit", 'q']:
            state = False
        elif arguments[0] in ["search", "/"]:
            try:
                if arguments[1] in ["pl", "playlist"]:
                    query = ' '.join(arguments[2:])
                    print(f"Searching for playlist '{query}'...")
                    videos = yt_manager.fetch_playlist(query)
                    if not videos:
                        print("No videos found for the playlist.")
                    else:
                        for idx, video in enumerate(videos, start=1):
                            print(f"{idx}. {video.title} - {video.duration}")
                else:
                    query = ' '.join(arguments[1:])
                    print(f"Searching for '{query}'...")
                    videos = yt_manager.search(query)
                    if not videos:
                        print("No videos found for your search.")
                    else:
                        for idx, video in enumerate(videos, start=1):
                            print(f"{idx}. {video.title} - {video.duration}")
                        selection = input("Enter the number of the video to add to the queue (use 'cancel' or 'c' to skip): ")
                        if selection.lower() not in ['cancel', 'c']:
                            try:
                                selected_index = int(selection) - 1
                                if 0 <= selected_index < len(videos):
                                    yt_manager.add_video(videos[selected_index])
                                    print(f"Added '{videos[selected_index].title}' to the queue.")
                                else:
                                    print("Invalid selection. Please enter a valid number.")
                            except ValueError:
                                print("Invalid input. Please enter a number or 'cancel'.")
            except IndexError:
                print("Usage: search <query> or / <query> to search for a song. search pl <url> or / pl <url> to search for a playlist.") 
        elif arguments[0] in ["list", "ls"]:
            try:
                if arguments[1] in ["playlist", "pl"]:
                    yt_manager.show_playlists()
                elif arguments[1] in ["queue", "q"]:
                    videos = yt_manager.list_videos()
                    if not videos:
                        print("No videos in the playlist.")
                    else:
                        for idx, video in enumerate(videos, start=1):
                            print(f"{idx}. {video.title} - {video.duration}")
                elif arguments[1] in ["played", "recent", "history"]:
                    videos = yt_manager.played_songs
                    if not videos:
                        print("No songs have been played yet.")
                    else:
                        for idx, video in enumerate(videos, start=1):
                            print(f"{idx}. {video.title} - {video.duration}")
                else:
                    print(f"Unknown argument: {arguments[1]}. Use 'list playlist', 'list queue', or 'list played'.")
            except IndexError:
                print("Usage: list <playlist|queue|played> or ls <playlist|queue|played>")
        elif arguments[0] in ["play"]:
            if len(arguments) == 1:
                yt_manager.play_song()
            else:
                try:
                    if arguments[1] in ["playlist", "pl"]:
                        playlist_name = arguments[2]
                        shuffle = len(arguments) > 3 and arguments[3] in ["rnd", "random", "shuffle"]
                        videos = yt_manager.fetch_playlistbyname(playlist_name, shuffle)
                        yt_manager.new_queue(videos)
                        yt_manager.play_song()
                    else:
                        if arguments[1] not in yt_manager.playlists:
                            print(f"Playlist '{arguments[1]}' not found.")
                            query = ' '.join(arguments[1])
                            print(f"Searching for '{query}'...")
                            videos = yt_manager.search(query)
                            if not videos:
                                print("No videos found for your search.")
                            else:
                                yt_manager.add_video(videos[0])
                                
                        else:
                            shuffle = len(arguments) > 2 and arguments[2] in ["rnd", "random", "shuffle"]
                            videos = yt_manager.fetch_playlistbyname(playlist_name, shuffle)
                            yt_manager.new_queue(videos)
                        yt_manager.play_song()
                except IndexError:
                    print("Usage: play or play <playlist_name> [rnd]")
        elif arguments[0] in ["volume", "vol"]:
            try:
                volume = int(arguments[1])
                yt_manager.set_volume(volume)
                print(f"Volume set to {volume}.")
            except (IndexError, ValueError):
                print("Usage: volume <0-100>")
        elif arguments[0] in ["pause"]:
            yt_manager.pause()
        elif arguments[0] in ["stop"]:
            yt_manager.stop()
        elif arguments[0] in ["resume"]:
            yt_manager.resume()
        elif arguments[0] in ["skip"]:
            yt_manager.skip()
        elif arguments[0] in ["playlist", "pl"]:
            if arguments[1] in ["rm", "del", "delete"]:
                try:
                    playlist_name = arguments[2]
                    yt_manager.delete_playlist(playlist_name)
                except IndexError:
                    print("Usage: playlist <rm|del|delete> <playlist_name>")
            elif arguments[1] in ["mk", "save"]:
                try:
                    if arguments[2] not in ["queue"]:
                        playlist_url = arguments[2]
                        playlist_name = arguments[3]
                        if not yt_manager.save_playlist(playlist_url, playlist_name):
                            print(f"Failed to save playlist '{playlist_name}'.")
                        else:
                            print(f"Playlist '{playlist_name}' saved successfully.")
                    else:
                        playlist_name = arguments[3]
                        videos = yt_manager.queue
                        if not videos:
                            print("No videos in the queue to save.")
                        else:
                            for video in videos:
                                yt_manager.add_song_to_playlist(playlist_name, video)
                            print(f"Playlist '{playlist_name}' saved successfully from the current queue.")
                except IndexError:
                    print("Usage: playlist <mk|save> <playlist_url> <playlist_name>")
            elif arguments[1] in ["edit"]:
                print("Playlist editing is not implemented yet.")
            elif arguments[1] in ["add"]:
                try:
                    if arguments[2] in ["current", "curr"]:
                        if not yt_manager.played_songs:
                            print("No video is currently playing.")
                        else:
                            plname = arguments[3] if len(arguments) > 3 else "music"
                            yt_manager.add_song_to_playlist(plname, yt_manager.played_songs[-1])
                            print(f"Added the currently playing video to the '{plname}' playlist.")
                    else:
                        print("Usage: playlist add current - Add the currently playing video to a saved playlist")
                except IndexError: 
                    print("Usage: playlist add current <playlist_name> - Add the currently playing video to a saved playlist")
            else:    
                print("Usage: playlist <rm|del|delete> <playlist_name> or playlist <add|save> <playlist_url> <playlist_name>")   
        elif arguments[0] in ["clear"]:
            yt_manager.new_queue([])
            print("Queue cleared.")
        else:
           print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")
        
        
if __name__ == "__main__":
    main()
