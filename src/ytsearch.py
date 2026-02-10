import requests
import re
import json
from dataclasses import dataclass
from urllib.parse import quote_plus 
from ytmanager import VideoInfo
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
                    
                    for item in items:
                        if "videoRenderer" in item:
                            # print(item["videoRenderer"]["title"]["runs"][0]['text'])
                            length = self.convert_to_sec(item["videoRenderer"]["lengthText"]['simpleText'])
                            newvid = VideoInfo(title=item["videoRenderer"]["title"]["runs"][0]['text'],
                                               url=f'https://www.youtube.com/watch?v={item["videoRenderer"]["videoId"]}',
                                               duration=length
                                               )
                            print(item["videoRenderer"])
                            
                            video_urls.append(newvid)
                    print(video_urls)
            

        except KeyError as e:
            return f"Structure changed or key not found: {e}"
    
    def convert_to_sec(self, duration):
        time = duration.split(":",2)
        return int(time[0])*60 + int(time[1])

def main():
    yt_search = YTLSearch()
    yt_search.search("vald")



if __name__=="__main__":
    main()