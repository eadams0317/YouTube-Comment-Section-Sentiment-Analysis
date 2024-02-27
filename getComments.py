import googleapiclient.discovery
import googleapiclient.errors
import json

with open('.env/keys.json', 'r') as f:
    keys = json.load(f)

api_key = keys.get('googleKey')


def execute(id, commentCount):

    api_service_name = "youtube"
    api_version = "v3"
    key = api_key

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=key
    )

    request = youtube.commentThreads().list(
    part="snippet",
    videoId = id,
    maxResults=100
    )
    response = request.execute()

    json_array = []

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        date = item['snippet']['topLevelComment']['snippet']['publishedAt']
        temp = {"comment": comment, "date": date}
        json_array.append(temp)

    
    while (1 == 1):
        try:
            nextPageToken = response['nextPageToken']
        except KeyError:
            break
        nextPageToken = response['nextPageToken']
        # Create a new request object with the next page token.
        nextRequest = youtube.commentThreads().list(part="snippet", videoId=id, maxResults=100, pageToken=nextPageToken)
        # Execute the next request.
        response = nextRequest.execute()
        # Get the comments from the next response.
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            temp = {"comment": comment, "date": date}
            json_array.append(temp)

    
    #For the sake of CPU usage and overheating, decimate array down to 200 entries 
    entries = len(json_array)
    decimateIndex = round(entries/commentCount)
    print(decimateIndex)
    decimatedArray = json_array[::decimateIndex]

    file_path = "data.json"

    with open(file_path, "w") as json_file:
        json.dump(decimatedArray, json_file, indent=4)
