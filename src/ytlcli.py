from ytmanager import YTManager

def display_welcome_message():
    print("Welcome to YTLCLI - Your YouTube Command Line Interface!")
    print("Type 'help' to see available commands.")
    print("Type 'exit' to quit the application.")
    print()



def main():
    display_welcome_message()
    yt_manager = YTManager()
    state = True
    while state: 
        cmd = input("ytlcli> ")
        if cmd == "exit":
            state = False
        elif cmd == "help":
            print("Available commands:")
            print("  help - Show this help message")
            print("  exit - Exit the application")
            print("  pl | playlist - Add a playlist")
            print("  show playlist - Show all saved playlists")
            print("  show queue - Show all videos in the current queue")
            print("  play - Play the first video in the queue")
            print("  play <playlist_name> [rnd] - Play a saved playlist, optionally shuffled with 'rnd'")
            print("  save <playlist_url> <playlist_name> - Save a playlist with a given name")
            print("  del <playlist_name> - Delete a saved playlist")
            print("  pause - Pause playback")
            print("  stop - Stop playback")
            print("  volume <0-100> - Set volume level")
        elif cmd == "pl" or cmd == "playlist":
            playlist_url = input("Enter playlist URL: ")
            videos = yt_manager.fetch_playlist(playlist_url)
            yt_manager.add_videos(videos)
            print(f"Added {len(videos)} videos from the playlist.")
        elif cmd.startswith("save"):
            try:
                arguments = cmd.split()[1:]
                if len(arguments) != 2:
                    print("Usage: save <playlist_url> <playlist_name>")
                    continue
                playlist_name, playlist_url = arguments
                if not yt_manager.save_playlist(playlist_url, playlist_name):
                    print(f"Failed to save playlist '{playlist_name}'.")
                print(f"Playlist '{playlist_name}' saved successfully.")
            except IndexError:
                print("Usage: save <playlist_url> <playlist_name>")
        elif cmd.startswith("del"):
            try:
                playlist_name = cmd.split()[1]
                yt_manager.delete_playlist(playlist_name)
            except IndexError:
                print("Usage: del <playlist_name>")
        elif cmd.startswith("show"):
            try:
                arguments = cmd.split()[1]
                if arguments == "playlist" or arguments == "pl":
                    yt_manager.show_playlists()
                elif arguments == "queue":
                    videos = yt_manager.list_videos()
                    if not videos:
                        print("No videos in the playlist.")
                    else:
                        for idx, video in enumerate(videos, start=1):
                            print(f"{idx}. {video.title} - {video.duration}")
                else:
                    print(f"Unknown argument: {arguments}. Use 'show playlist' or 'show queue'.")
            except IndexError:
                print("Usage: show <playlist|queue>")
        #CONTROLS PLAYER
        elif cmd == "play":
            yt_manager.play_song()
        elif cmd.startswith("play"):
            try:
                arguments = cmd.split()[1:]
                if len(arguments) > 1:
                    playlist_name, shuffle = arguments
                    if shuffle == 'rnd':
                        shuffle = True 
                else:
                    playlist_name = arguments[0]
                    shuffle = False
                    
                videos = yt_manager.fetch_playlistbyname(playlist_name, shuffle)
                yt_manager.new_queue(videos)
                yt_manager.play_song()
            except IndexError:
                print("Usage: play <playlist_name>")
        elif cmd.startswith("volume") or cmd.startswith("vol"):
            try:
                volume = int(cmd.split()[1])
                yt_manager.set_volume(volume)
                print(f"Volume set to {volume}.")
            except (IndexError, ValueError):
                print("Usage: volume <0-100>")
        elif cmd == "pause":
            yt_manager.pause()
        elif cmd == "skip":
            yt_manager.skip()
        elif cmd == "stop":
            yt_manager.stop()
        else:
           print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")
        
        
if __name__ == "__main__":
    main()
