import sys
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, npt, isRightPage):
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
        print()
    
    return search_response["nextPageToken"]    

if __name__ == "__main__":
    query_term = sys.argv[1]
    max_results = sys.argv[2]
    start_page = int(sys.argv[3])
    end_page = int(sys.argv[4])

    try:
        if(end_page < start_page):
            print("Start page must be less than end page")
        if(start_page < 1):
            print("Invalid page number")
        elif(start_page == 1):
            # 1st page--print
            npt = youtube_search(query_term, max_results, None, True)
            # print these pages
            for x in range(end_page - start_page):
                npt = youtube_search(query_term, max_results, npt, True)
        else:
            # 1st page--don't print
            npt = youtube_search(query_term, max_results, None, False)
            # don't print these pages
            for i in range(start_page - 2): # -2 because we do 1 call before loop and 1 after
                npt = youtube_search(query_term, max_results, npt, False)
            # 1st page to print
            npr = youtube_search(query_term, max_results, npt, True)
            # print these pages
            for y in range(end_page - start_page):
                npt = youtube_search(query_term, max_results, npt, True)
    except HttpError as e:
        print('An HTTP error %d occurred: \n%s' % (type(e).__name__, str(e)))
