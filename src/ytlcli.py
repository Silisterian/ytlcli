
import os
import sys
import time
from random import shuffle

from ytmanager import YTManager

def clear_console():
    # Efface la console selon le système (Windows ou Unix)
    os.system('cls' if os.name == 'nt' else 'clear')


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

def draw_dashboard(current_track, queue, selected_pl, last_output=None):
    # Codes Couleurs
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    GRAY = "\033[90m"

    clear_console()
    
    ui = []
    ui.append(f"{BOLD}{CYAN}╔══════════════════ MUSIC DASHBOARD ══════════════════╗{RESET}")
    
    # Info Playlist
    pl_display = selected_pl if selected_pl else "None"
    ui.append(f"  {BOLD}SELECTED PLAYLIST:{RESET} {YELLOW}{pl_display}{RESET}")
    ui.append(f"{GRAY}╟──────────────────────────────────────────────────────╢{RESET}")
    
    # Now Playing
    ui.append(f"  {BOLD}NOW PLAYING{RESET}")
    if current_track:
        ui.append(f"  {GREEN}▶ {current_track.title}{RESET}")
    else:
        ui.append(f"  {GRAY}▶ Nothing is playing{RESET}")
    
    ui.append(f"{GRAY}╟──────────────────────────────────────────────────────╢{RESET}")
    
    # Queue
    ui.append(f"  {BOLD}UPCOMING QUEUE{RESET}")
    if queue:
        for i, track in enumerate(queue[:5], 1):
            ui.append(f"    {GRAY}{i}. {track.title}{RESET}")
        if len(queue) > 5:
            ui.append(f"    {GRAY}... and {len(queue)-5} more{RESET}")
    else:
        ui.append(f"    {GRAY}(Queue is empty){RESET}")
        
    ui.append(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════╝{RESET}")
    
    if last_output:
        ui.append(f"\n{YELLOW} YTL :{RESET} {last_output}")
    print("\n".join(ui))

def main():
    display_welcome_message()
    last_output = "welcome"
    yt_manager = YTManager()
    state = True
    while state: 
        # draw_dashboard(yt_manager.played_songs[-1] if yt_manager.played_songs else None, yt_manager.list_videos(), yt_manager.current_playlist, last_output)
        cmd = input("ytlcli> ")
        arguments = cmd.split(' ', 3)
        if arguments[0] == "help":
            display_help()
            input("\nPress Enter to return to Dashboard...")
        elif arguments[0] in ["exit", "quit", 'q']:
            state = False
        elif arguments[0] in ["search", "/"]:
            try:
                if arguments[1] in ["pl", "playlist"]:
                    query = ' '.join(arguments[2:])
                    last_output = f"Searching for playlist '{query}'..."
                    videos = yt_manager.fetch_playlist(query)
                    if not videos:
                        last_output = f"No playlists found for '{query}'."
                    else:
                        yt_manager.new_queue(videos)
                        last_output = f"playlist added to queue you can use play to start player."
                else:
                    query = ' '.join(arguments[1:])
                    last_output = f"Searching for '{query}'..."
                    videos = yt_manager.search(query)
                    if not videos:
                        last_output = "No videos found for your search."
                    else:
                        for idx, video in enumerate(videos, start=1):
                            print(f"{idx}. {video.title} - {video.duration}")
                        selection = input("Enter the number of the video to add to the queue (use 'cancel' or 'c' to skip): ")
                        if selection.lower() not in ['cancel', 'c']:
                            try:
                                selected_index = int(selection) - 1
                                if 0 <= selected_index < len(videos):
                                    yt_manager.add_video(videos[selected_index])
                                    last_output = f"Added '{videos[selected_index].title}' to the queue."
                                else:
                                    last_output = "Invalid selection. Please enter a valid number."
                            except ValueError:
                                last_output = "Invalid input. Please enter a number or 'cancel'."
            except IndexError:
                last_output = "Usage: search <query> or / <query> to search for a song. 'search pl <url>' or '/ pl <url>' to search for a playlist." 
        elif arguments[0] in ["list", "ls"]:
            try:
                if arguments[1] in ["playlist", "pl"]:
                    last_output = yt_manager.show_playlists()
                elif arguments[1] in ["queue", "q"]:
                    videos = yt_manager.list_videos()
                    if not videos:
                        last_output = "No videos in the playlist."
                    else:
                        for idx, video in enumerate(videos, start=1):
                            last_output = f"{idx}. {video.title} - {video.duration}"
                elif arguments[1] in ["played", "recent", "history"]:
                    videos = yt_manager.played_songs
                    if not videos:
                        last_output = "No songs have been played yet."
                    else:
                        for idx, video in enumerate(videos, start=1):
                            last_output = f"{idx}. {video.title} - {video.duration}"
                else:
                    last_output = f"Unknown argument: {arguments[1]}. Use 'list playlist', 'list queue', or 'list played'."
            except IndexError:
                last_output = "Usage: list <(playlist|pl)|queue|played> or ls <(playlist|pl)|queue|played>"
        elif arguments[0] in ["play"]:
            if len(arguments) == 1:
                yt_manager.play_song()
            else:
                try:
                    if arguments[1] in ["playlist", "pl"]:
                        playlist_name = arguments[2]
                        if playlist_name in yt_manager.playlists:
                            shuffle = len(arguments) > 3 and arguments[3].lower() in ["rnd", "random", "shuffle", "true"]
                            videos = yt_manager.fetch_playlistbyname(playlist_name, shuffle)
                            yt_manager.new_queue(videos)
                            yt_manager.play_song()
                            yt_manager.current_playlist = playlist_name
                        else:
                            last_output = f"no playlist named {playlist_name}. use 'ls pl' to show local playlist or create a playlist by running 'pl save <url> name'"
                    else:
                        if arguments[1] not in yt_manager.playlists:
                            last_output = f"Playlist '{arguments[1]}' not found."
                            query = ' '.join(arguments[1:])
                            last_output = f"Searching for '{query}'..."
                            videos = yt_manager.search(query)
                            if not videos:
                                last_output = "No videos found for your search."
                            else:
                                yt_manager.add_video(videos[0])
                                
                        else:
                            shuffle = len(arguments) > 2 and arguments[2] in ["rnd", "random", "shuffle", 'true']
                            videos = yt_manager.fetch_playlistbyname(playlist_name, shuffle)
                            yt_manager.new_queue(videos)
                        yt_manager.play_song()
                except IndexError:
                    last_output = "Usage: play or play <playlist_name> true(to randomize)"
        elif arguments[0] in ["volume", "vol"]:
            try:
                volume = int(arguments[1])
                yt_manager.set_volume(volume)
                last_output = f"Volume set to {volume}."
            except (IndexError, ValueError):
                last_output = "Usage: volume <0-100>"
        elif arguments[0] in ["pause"]:
            yt_manager.pause()
            last_output = "Playback paused. you can resume or skip by using the associated commands. "
        elif arguments[0] in ["stop"]:
            yt_manager.stop()
            last_output = "Playback stopped. You can start the player again with 'play' or clear the queue by using clear."
        elif arguments[0] in ["resume"]:
            yt_manager.resume()
            last_output = "Playback resumed. You can also pause, skip, or stop playback with the respective commands."
        elif arguments[0] in ["skip"]:
            yt_manager.skip()
            last_output = "Skipped to the next track. You can also pause, stop, or resume playback with the respective commands."
        elif arguments[0] in ["playlist", "pl"]:
            if arguments[1] in ["rm", "del", "delete"]:
                try:
                    playlist_name = arguments[2]
                    yt_manager.delete_playlist(playlist_name)
                except IndexError:
                    last_output = "Usage: playlist <rm|del|delete> <playlist_name>"
            elif arguments[1] in ["mk", "save"]:
                try:
                    if arguments[2] not in ["queue"]:
                        playlist_url = arguments[2]
                        playlist_name = arguments[3]
                        if not yt_manager.save_playlist(playlist_url, playlist_name):
                            last_output = f"Failed to save playlist '{playlist_name}'."
                        else:
                            last_output = f"Playlist '{playlist_name}' saved successfully."
                    else:
                        playlist_name = arguments[3]
                        videos = yt_manager.queue
                        if not videos:
                            last_output = "No videos in the queue to save."
                        else:
                            for video in videos:
                                yt_manager.add_song_to_playlist(playlist_name, video)
                            last_output = f"Playlist '{playlist_name}' saved successfully from the current queue."
                except IndexError:
                    print("Usage: playlist <mk|save> <playlist_url> <playlist_name>")
            elif arguments[1] in ["edit"]:
                print("Playlist editing is not implemented yet.")
            elif arguments[1] in ["add"]:
                try:
                    if arguments[2] in ["current", "curr"]:
                        if not yt_manager.played_songs:
                            last_output = "No video is currently playing."
                        else:
                            plname = arguments[3] if len(arguments) > 3 else "music"
                            yt_manager.add_song_to_playlist(plname, yt_manager.played_songs[-1])
                            last_output = f"Added the currently playing video to the '{plname}' playlist."
                    else:
                        last_output = "Usage: playlist add current - Add the currently playing video to a saved playlist"
                except IndexError: 
                    last_output = "Usage: playlist add current <playlist_name> - Add the currently playing video to a saved playlist"
            else:    
                last_output = "Usage: playlist <rm|del|delete> <playlist_name> or playlist <add|save> <playlist_url> <playlist_name>"   
        elif arguments[0] in ["clear"]:
            yt_manager.new_queue([])
            last_output = "Queue cleared. set a queue with 'play pl <playlist_name> true'."
        elif arguments[0] in ["rnd"]:
            queue = yt_manager.queue
            if not queue:
                last_output = f"queue is empty !"
            else:
                shuffle(queue)
                yt_manager.new_queue(queue)
                last_output = f"randomizing actual queue..."
            
        else:
           last_output = f"Unknown command: {cmd}. Type 'help' for a list of commands."
        
        
if __name__ == "__main__":
    main()
