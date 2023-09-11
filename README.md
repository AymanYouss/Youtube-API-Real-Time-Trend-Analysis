# Youtube-API-Real-Time-Trend-Analysis

This repository contains Python code to perform an up-to-date analysis of trending YouTube videos using the YouTube API. The analysis includes various aspects of the videos such as their metadata, comments, thumbnail analysis, and more. The data is collected using the YouTube API and stored in a CSV file for further analysis.

## Prerequisites

Before running the code, make sure you have the following prerequisites installed:

- Python 3.x
- Required Python packages (you can install them using `pip`):
  - google-api-python-client
  - numpy
  - opencv-python
  - Pillow
  - requests
  - colorthief
  - colormath
  - emoji

You also need to obtain a YouTube Data API key from the [Google Developers Console](https://console.developers.google.com/).

## Getting Started

1. Clone this repository to your local machine:
git clone <repository-url>

2. Replace "YOUR_API_KEY" with your actual YouTube Data API key in the API_KEY variable in the Python code.

3. Run the Python script youtube_trending_analysis.py:
python youtube_trending_analysis.py

The script will fetch data on the top 10 trending YouTube videos in the US and perform various analyses on them.

## Features
The analysis includes the following features:

1. Video metadata, including title, duration, channel information, view count, like count, comment count, and more.
2. Comment analysis, including word frequency.
3. Thumbnail analysis, including dominant colors and mood (dark, warm, or cool).
4. Pattern symmetry analysis (horizontal or vertical).
5. Categorization of videos based on YouTube category IDs.
6. Extraction and analysis of emojis in video titles.

## Output
Output
The script will generate a CSV file named trending_videos.csv that contains the analyzed data for the top 10 trending YouTube videos in the US. The CSV file will include the following columns:

- Title
- Length of video
- Channel Name
- Channel URL
- Channel Total Subscribers
- View count
- Like count
- Comment count
- Comment Word Frequency
- Thumbnail URL
- Category
- Tags
- Published at
- Description
- Thumbnail dominant colors (hex values)
- Mood
- Pattern Symmetry
- Title Character Count
- Title Number of emojis
- Title Percentage of emojis
- Title UpperCase Count
Title Number of Capitalized words
