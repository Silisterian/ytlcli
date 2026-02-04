import time, os
from random import shuffle

import json
import yt_dlp
import vlc 

from dataclasses import dataclass
from typing import List, Optional

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
        }
        self.queue = []
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        if not os.path.exists("playlist.json"):
            with open("playlist.json", 'w') as f:
                json.dump({}, f)
        self.playlists = self.load_playlist()
    
    def save_playlist(self, url: str, name: str):
        try:
            if name in self.playlists:
                print(f"Playlist '{name}' already exists. Overwriting.")
                
            self.playlists[name] = url
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
        
        # Si le fichier n'existe pas ou est corrompu
        return {}

    def show_playlists(self):
        if not self.playlists:
            print("No playlists available.")
            return
        print("Available playlists:")
        for name, url in self.playlists.items():
            print(f"{name}: {url}")

    def add_video(self, video: VideoInfo):
        self.queue.append(video)

    def add_videos(self, videos: List[VideoInfo]):
        self.queue.extend(videos)

    def new_queue(self, videos: List[VideoInfo]):
        self.queue = videos

    def fetch_playlistbyname(self, name: str, sh: bool = False) -> List[VideoInfo]:
        url = self.playlists.get(name)
        if not url:
            print(f"Playlist '{name}' not found.")
            return []
        vids = self.fetch_playlist(url)
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
    
    def list_videos(self) -> List[VideoInfo]:
        return self.queue

    def get_url_song(self, url) -> str:
        with yt_dlp.YoutubeDL(self.opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(info['url'])
            return info['url']

    def pause(self):
        self.player.pause()
    
    def stop(self):
        self.player.stop()
    
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
        # print(current_song)
        media = self.instance.media_new(url)
        self.player.set_media(media)

        self.player.play()
        time.sleep(1)  # Wait for the player to start
        return self.player, self.instance
        