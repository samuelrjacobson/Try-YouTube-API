import sys
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, npt):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.List method to retrieve results matching the specified query term.
    if(npt == None):
        search_response = youtube.search().list(
            q = query_term,
            part = 'id,snippet',
            maxResults = max_results,
        ).execute()
    else:
        search_response = youtube.search().list(
            q = query_term,
            part = 'id,snippet',
            maxResults = max_results,
            pageToken = npt,
        ).execute()

    print(search_response["items"])
    print("\t")
    
    return search_response["nextPageToken"]

if __name__ == "__main__":
    query_term = sys.argv[1]
    max_results = sys.argv[2]
    try:
        npt = youtube_search(query_term, max_results, None)
        youtube_search(query_term, max_results, npt)
    except HttpError as e:
        print('An HTTP error %d occurred: \n%s' % (type(e).__name__, str(e)))
