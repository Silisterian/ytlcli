import requests
import re
import os
import sys
import json
from dataclasses import dataclass
from urllib.parse import quote_plus, parse_qs, unquote



@dataclass
class YTLSearch:
    def __init__(self, user_search=None,max_results=10, proxy={}, retries=3, music_only=False):
        self.user_search = user_search
        self.max_result= max_results
        self.retries=retries
        self.timeout=10
        self.proxy=proxy
        self.videos = []


    def search(self, srch):
        enc = quote_plus(srch)
        yturl = f"https://youtube.com/results?search_query={enc}"

        print("searching..")
        atmpt = 1
        response = requests.get(yturl, proxies=self.proxy, timeout=self.timeout).text
        while "ytInitialData" not in response and atmpt <= self.retries:
            response = requests.get(yturl, proxies=self.proxy, timeout=self.timeout).text
        
        json_text = re.search(r'var ytInitialData = (\{.*?\});', response)
        if not json_text:
            return "Could not find ytInitialData. YouTube might be blocking the request."
        
        data = json.loads(json_text.group(1))
        
        try:
            sections = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
            
            video_urls = []
            
            for section in sections:
                if "itemSectionRenderer" in section:
                    items = section["itemSectionRenderer"]["contents"]
                    # print(items[-1])
                    for item in items:
                        if "videoRenderer" in item:
                            rsult = {}
                            rsult["url"] =f'https://www.youtube.com/watch?v={item["videoRenderer"]["videoId"]}'
                            rsult["title"] = item["videoRenderer"]["title"]["runs"][0]['text']
                            rsult["duration"] = self.convert_to_sec(item["videoRenderer"]["lengthText"]['simpleText'])
                            rsult['img'] = item['videoRenderer']['thumbnail']['thumbnails'][0]['url']
                            rsult['OP'] = item['videoRenderer']['longBylineText']['runs'][0]['text']
                            viewcount = item['videoRenderer']['viewCountText']['simpleText'].replace('\xa0', ' ').replace('\u202f', '').lower()
                            match = re.search(r'([\d,\.]+)\s*(k|m|md)?', viewcount)
                            if match:
                                nombre_str = match.group(1).replace(',', '.')
                                suffixe = match.group(2)
                                try:
                                    valeur = float(nombre_str)
                                    
                                    # Application du multiplicateur
                                    if suffixe == 'k':
                                        valeur *= 1_000
                                    elif suffixe == 'm':
                                        valeur *= 1_000_000
                                    elif suffixe == 'md':
                                        valeur *= 1_000_000_000
                                    rsult["views"] = int(valeur)
                                except ValueError as e:
                                    return f"Structure changed or key not found: {e}"
                                    
                            
                            
                            video_urls.append(rsult)
                    return video_urls
        except KeyError as e:
            return f"Structure changed or key not found: {e}"
    
    def convert_to_sec(self, duration):
        time = duration.split(":",2)
        return int(time[0])*60 + int(time[1])

    
    def to_dict(self, clear_cache=True):
        result = self.videos
        if clear_cache:
            self.videos = ""
        return result

    def to_json(self, clear_cache=True):
        result = json.dumps({"videos": self.videos})
        if clear_cache:
            self.videos = ""
        return result
    
