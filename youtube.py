import sys
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, page, npt, isRightPage):
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

    if(isRightPage):
        print(search_response["items"])
    
    return search_response["nextPageToken"]

if __name__ == "__main__":
    query_term = sys.argv[1]
    max_results = sys.argv[2]
    page = int(sys.argv[3])
    try:
        if(page < 1):
            print("Invalid page number")
        elif(page == 1):
            npt = youtube_search(query_term, max_results, page, None, True)
        else:
            npt = youtube_search(query_term, max_results, page, None, False)
            for i in range(page - 2):
                npt = youtube_search(query_term, max_results, page, npt, False)
            youtube_search(query_term, max_results, page, npt, True)
    except HttpError as e:
        print('An HTTP error %d occurred: \n%s' % (type(e).__name__, str(e)))
