# Add comment here
from googleapiclient.discovery import build
import csv
import googleapiclient.discovery
import urllib.request
import json
import cv2
import numpy as np
from PIL import Image
import numpy as np
import requests
import json
from PIL import Image
from collections import Counter
from googleapiclient.discovery import build
import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import cv2
import emoji

def extract_emojis(s):
  return ''.join(c for c in s if c in emoji.EMOJI_DATA.keys())

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def analyze_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url)
    image = Image.open(BytesIO(response.content))
    image.save("imageToAnalyze.jpg")
    color_thief = ColorThief("imageToAnalyze.jpg")
    color_palette = color_thief.get_palette(color_count=5)

    hex_colors = []
    for color in color_palette:
        r, g, b = color
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        hex_colors.append(hex_color)

    return hex_colors

def analyze_color_mood(hex_colors):
    moods = []
    for hex_color in hex_colors:
        rgb = sRGBColor.new_from_rgb_hex(hex_color)
        lab = convert_color(rgb, LabColor)
        if lab.lab_l <= 60:
            mood = "dark"
        elif lab.lab_a >= 0 and lab.lab_b >= 0:
            mood = "warm"
        else:
            mood = "cool"
        moods.append(mood)

    return moods

def analyze_pattern_symmetry(thumbnail_url):
    response = requests.get(thumbnail_url)
    image = Image.open(BytesIO(response.content))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, maxLineGap=50)
    if lines is None:
        return "none"

    horizontal_lines = 0
    vertical_lines = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if y1 == y2:
            horizontal_lines += 1
        elif x1 == x2:
            vertical_lines += 1

    if horizontal_lines > vertical_lines:
        return "horizontal"
    elif vertical_lines > horizontal_lines:
        return "vertical"

def transformCategory(number):
    if number == "1":
  	    return "Film & Animation"
    if number == "2":
	    return "Autos & Vehicles"
    elif number == "10":
    	return "Music"
    elif number == "15":
	    return "Pets & Animals"
    elif number == "17":
	    return "Sports"
    elif number == "18":
	    return "Short Movies"
    elif number == "19":
	    return "Travel & Events"
    elif number == "20":
	    return "Gaming"
    elif number == "21":
	    return "Videoblogging"
    elif number == "22":
	    return "People & Blogs"
    elif number == "23":
	    return "Comedy"
    elif number == "24":
	    return "Entertainment"
    elif number == "25":
	    return 'News & Politics'
    elif number == "26":
	    return "Howto & Style"
    elif number == "27":
    	return "Education"
    elif number == "28":
    	return "Science & Technology"
    elif number == "29":
    	return "Nonprofits & Activism"
    elif number == "30":
    	return "Movies"
    elif number == "31":
    	return "Anime/Animation"
    elif number == "32":
    	return "Action/Adventure"
    elif number == "33":
    	return "Classics"
    elif number == "34":
    	return "Comedy"
    elif number == "35":
    	return "Documentary"
    elif number == "36":
	    return "Drama"
    elif number == "37":
	    return "Family"
    elif number == "38":
	    return "Foreign"
    elif number == "39":
	    return "Horror"
    elif number == "40":
	    return "Sci-Fi/Fantasy"
    elif number == "41":
	    return "Thriller"
    elif number == "42":
        return "Shorts"
    elif number == "43":
	    return "Shows"
    elif number == "44":
	    return "Trailers"
    return "Category not found"

















    
   








API_KEY = "AIzaSyDmoxboia-mJ-KIoT9in7YQU9oyUSKHhRw"
youtube = build("youtube", "v3", developerKey=API_KEY)

request = youtube.videos().list(
    part="snippet,statistics,contentDetails",
    chart="mostPopular",
    maxResults=10,
    regionCode="US"
)

response = request.execute()

cur = 0
with open("trending_videos.csv", "w", encoding='utf-8', newline='') as file:
    fieldnames = ["Title", "Length of video","Channel Name","Channel URL","Channel Total Subscribers", "View count", "Like count", "Comment count", "Comment Word Frequency","Thumbnail URL", "Category", "Tags", "Published at", "Description","Thumbnail dominant colors (hex values)","Mood","Pattern Symmetry","Title Character Count","Title Number of emojis","Title Percentage of emojis","Title UpperCase Count","Title Number of Capitalized words"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    
    for video in response["items"]:
        
        print("Video "+str(cur+1)+" done")
        video_thumbnail_url = video["snippet"]["thumbnails"]["default"]["url"]
        # Read the original image
        response2 = requests.get(video_thumbnail_url)
        image = Image.open(BytesIO(response2.content))
        image.save("thumbnail"+str(cur)+".jpg")
        img = cv2.imread("thumbnail"+str(cur)+".jpg") 

        
        # Convert to graycsale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Blur the image for better edge detection
        img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
        


        
        # Canny Edge Detection
        edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
        # Display Canny Edge Detection Image




        image_todraw = np.array(edges)


        image_tosave = Image.fromarray(image_todraw.astype(np.uint8))
        image_tosave.save('EdgeDetection-video'+str(cur)+'.jpg')
        cur += 1
        cv2.destroyAllWindows()
        
        comment_list = youtube.commentThreads().list(part = 'snippet', maxResults = 50, videoId = video['id'], order = 'relevance').execute()
        comments = [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in comment_list["items"]]

        comString = ''.join(comments)
        comStringList = comString.split()
        
        wordfreq = [comStringList.count(w) for w in comStringList] # a list comprehension

        freqDict = dict(list(zip(comStringList,wordfreq)))
        sortedDict = {}
        for k, v in sorted(freqDict.items(), key=lambda x: x[1]):
            sortedDict[k] = v
        
        

        subsRequest = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/channels?id='+video["snippet"]["channelId"]+'&key='+API_KEY+'&part=statistics').read()

        noOfSubscribers = json.loads(subsRequest)["items"][0]["statistics"]["subscriberCount"]
        try:
            temp = video["statistics"]["likeCount"]
        except:
            video["statistics"]["likeCount"] = "hidden"
                
        try:
            temp2 = video["statistics"]["commentCount"]
        except:
            video["statistics"]["commentCount"] = "hidden"

        try:
            temp3 = video["snippet"]["tags"]
        except:
            video["snippet"]["tags"] = "no tag"
        
        emos = extract_emojis(video["snippet"]["title"])
        hex_colors = analyze_thumbnail(video_thumbnail_url)
        writer.writerow({
            "Title": video["snippet"]["title"],
            "Length of video": video["contentDetails"]["duration"],
            "Channel Name": video["snippet"]["channelTitle"],
            "Channel URL": "https://www.youtube.com/channel/" + video["snippet"]["channelId"],
            "Channel Total Subscribers": noOfSubscribers,
            "Like count": video["statistics"]["likeCount"],
            "View count": video["statistics"]["viewCount"],
            "Comment count": video["statistics"]["commentCount"],
            "Comment Word Frequency": sortedDict,
            "Thumbnail URL": video["snippet"]["thumbnails"]["default"]["url"],
            "Category": transformCategory(video["snippet"]["categoryId"]),
            "Tags": video["snippet"]["tags"],
            "Published at": video["snippet"]["publishedAt"],
            "Description": video["snippet"]["description"],
            "Thumbnail dominant colors (hex values)":hex_colors,
            "Mood": analyze_color_mood(hex_colors),
            "Pattern Symmetry":analyze_pattern_symmetry(video_thumbnail_url),
            "Title Character Count" : dict(Counter(video["snippet"]["title"])),
            "Title Number of emojis" : len(emos),
            "Title Percentage of emojis" : str(round(len(emos)/len(video["snippet"]["title"])*100,2))+"%",
            "Title UpperCase Count": sum(1 for char in video["snippet"]["title"] if char.isupper()),
            "Title Number of Capitalized words" : len([i for i in video["snippet"]["title"] if i[0].isupper()])
        })