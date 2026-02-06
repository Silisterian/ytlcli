import time, os
import threading
from random import shuffle
import warnings

import json
import yt_dlp
import vlc
from youtube_search import YoutubeSearch

from dataclasses import dataclass
from typing import List, Optional

warnings.filterwarnings("ignore")

@dataclass
class VideoInfo:
    title: str
    url: str
    duration: Optional[int] = None  # Duration in seconds
    description: Optional[str] = None
    tags: Optional[List[str]] = None



class YTManager:
    def __init__(self):
        self.opts = {
            'quiet': True,
            'extract_flat': True,
            'format': 'bestaudio',
            'force_generic_extractor': True,
            'no_warnings': True,
        }
        self.queue = []
        self.played_songs = []
        self.current_playlist = None
        if not os.path.exists("playlist.json"):
            with open("playlist.json", 'w') as f:
                json.dump({}, f)
        self.playlists = self.load_playlist()

        ### VLC player initialization
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        self.is_playing = False
        
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_song_end)
        

###### Search management ######
    def search(self, query: str, isplaylist: bool = False) -> List[VideoInfo]:
        try:
            results = YoutubeSearch(query, max_results=20).to_dict()
            print(f"Search results for '{query}':")
            fetched_videos = []
            for entry in results:
                video = VideoInfo(
                        title=entry.get('title'),
                        url="https://www.youtube.com" + entry.get('url_suffix').split('&')[0],  # Remove playlist parameter if present
                        duration=entry.get('duration'),
                        description=entry.get('description'),
                        tags=entry.get('tags')
                    )
                fetched_videos.append(video)
            return fetched_videos
        except Exception as e:
            print(f"Error during search: {e}")
            return []



###### Playlists management ###### 
    def save_playlist(self, url: str, name: str):
        try:
            if name in self.playlists:
                print(f"Playlist '{name}' already exists. Overwriting.")    
            self.playlists[name] = {"playlist": url}
            print(self.playlists)
            with open("playlist.json", 'w') as f:
                json.dump(self.playlists, f)
            return True
        except Exception as e:
            print(f"Error saving playlist: {e}")
            return False

    def delete_playlist(self, name: str):
        if name in self.playlists:
            del self.playlists[name]
            with open("playlist.json", 'w') as f:
                json.dump(self.playlists, f)
            print(f"Playlist '{name}' deleted successfully.")
        else:
            print(f"Playlist '{name}' not found.")
    
    def load_playlist(self):
        try:
            with open("playlist.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Fichier JSON corrompu, création d'un nouveau")
        return {}

    def show_playlists(self):
        if not self.playlists:
            print("No playlists available.")
            return
        print("Available playlists:")
        for name, url in self.playlists.items():
            print(f"{name}: {url}")

    def add_song_to_playlist(self, playlist_name: str = None, video: VideoInfo = None):
        if not playlist_name:
            playlist_name = self.current_playlist
        old_entity = self.playlists
        if not old_entity:
            print(f"Playlist '{playlist_name}' not found.")
            return
        if type(old_entity[playlist_name]) == str:

            old_entity[playlist_name] = {"playlist": old_entity[playlist_name],
                      "songs": [
                          {"id": 1,"url": video.url, "title": video.title}
                      ]}
        else:
            lcount = len(old_entity[playlist_name]["songs"])
            old_entity[playlist_name]["songs"].append({"id": lcount + 1, "url": video.url, "title": video.title})
        self.playlists = old_entity
        with open("playlist.json", 'w') as f:
                json.dump(self.playlists, f)


### These methods are used to fetch videos from a playlist, either by name or by URL. The fetch_playlistbyname method looks up the local playlist based on the provided name and then calls fetch_playlist to retrieve the video information. If the sh parameter is set to True, it shuffles the list of videos before returning it. The fetch_playlist method uses yt_dlp to extract information about each video in the playlist and returns a list of VideoInfo objects containing details about each video.
### fetched video are added to queue

    def fetch_playlistbyname(self, name: str, sh: bool = False) -> List[VideoInfo]:
        url = None
        songs = []
        if type(self.playlists[name]) == str:
            url = self.playlists[name]
        else:
            url = self.playlists[name]['playlist']
            songs = self.playlists[name]['songs']
        if not url:
            print(f"Playlist '{name}' not found.")
            return []
        vids = self.fetch_playlist(url)
        if songs:
            for song in songs:
                vids.append(VideoInfo(title=song['title'], url=song['url']))
        if not sh:
            return vids
        shuffle(vids)
        return vids

    def fetch_playlist(self, playlist_url: str) -> List[VideoInfo]:
        try:    
            with yt_dlp.YoutubeDL(self.opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False, process=True)
                fetched_videos = []
                for entry in info.get('entries', []):
                    video = VideoInfo(
                        title=entry.get('title'),
                        url=entry.get('url'),
                        duration=entry.get('duration'),
                        description=entry.get('description'),
                        tags=entry.get('tags')
                    )
                    fetched_videos.append(video)

            return fetched_videos
        except Exception as e:
            print(f"Error fetching playlist: {e}")
            return []   
    

###### Queue management ######

    def add_video(self, video: VideoInfo):
        self.queue.append(video)

    def add_videos(self, videos: List[VideoInfo]):
        self.queue.extend(videos)

    def new_queue(self, videos: List[VideoInfo]):
        self.queue = videos

    def list_videos(self) -> List[VideoInfo]:
        return self.queue


###### Player management ######


    def get_url_song(self, url) -> str:
        with yt_dlp.YoutubeDL(self.opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return info['url']

    def pause(self):
        self.player.pause()
    
    def stop(self):
        self.player.stop()

    def resume(self):
        self.player.play()
    
    def set_volume(self, volume):
        """Volume entre 0 et 100"""
        self.player.audio_set_volume(volume)

    def skip(self):
        self.player.stop()
        self.play_song()

    def play_song(self):
        current_song = self.queue.pop(0) if self.queue else None
        if not current_song:
            print("No songs in the queue to play.")
            return None
        url = self.get_url_song(current_song.url)
        
        old_media = self.player.get_media()
        if old_media:
            old_media.release()
            
        media = self.instance.media_new(url)
        
        self.player.set_media(media)
        
        self.player.play()

        self.played_songs.append(current_song)
        
        time.sleep(1)
        
        display_title = current_song.title if current_song.title else "Unknown Title"
        print(f"Now playing: {display_title}")
        
        if self.queue:
            next_song = self.queue[0]
            next_title = next_song.title if next_song.title else "Unknown Title"
            print(f"Up next: {next_title}")
        
        return self.player, self.instance
    
    def on_song_end(self, event):
        if self.queue:
            print(f"Next song: {self.queue[0].title}")
            # Lancer play_song dans un thread séparé pour éviter le deadlock
            threading.Thread(target=self.play_song, daemon=True).start()
        else:
            print("Queue is empty. Stopping playback.")