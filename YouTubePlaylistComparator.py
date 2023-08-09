# API client library
import googleapiclient.discovery
import json

#returns: name of playlist, size of playlist
def getplaylistNameAndSize(apibuild, id):
    request = apibuild.playlists().list(
        part = "snippet, contentDetails",
        maxResults = 1,
        id = id)

    response = request.execute()

    return response["items"][0]["snippet"]["title"], response["items"][0]["contentDetails"]["itemCount"]

#returns: a set of all unique songs in playlist.
def getplaylist(apibuild, id):
    ###### getting playlist songs ######
    request = apibuild.playlistItems().list(
        part = "snippet",
        maxResults = 50,
        playlistId = id)

    response = request.execute()

    if response.get("nextPageToken") != None:
        nextToken = response["nextPageToken"]
    else: 
        nextToken = None

    playlist_videos = set()
    x = 0
    while x < 1000:

        for i in response["items"]:
            #response_1["items"] is a list of playlistItem, which is a json dictionary.
            playlist_videos.add(i["snippet"]["title"])

        if nextToken == None:
            break
        
        request = apibuild.playlistItems().list(
            part = "snippet",
            maxResults = 50,
            playlistId = id,
            pageToken = nextToken)

        response = request.execute()

        if response.get("nextPageToken") != None:
            nextToken = response["nextPageToken"]

        else: 
            nextToken = None
        
        x = x + 1
    
    return playlist_videos

#returns: 3 sorted lists of songs.
def playlistCompare(a , b):
    #songs that are in both playlists
    songsC = []

    #songs that are in playlist a, but not in b
    songsA = []

    for title in a:
        if title not in b:
            songsA.append(title)
        else: #if title in b:
            songsC.append(title)

    #songs that are in playlist b, but not in a
    songsB = []

    for title in b:
        if title not in a:
            songsB.append(title)
    
    #sort the playlists
    songsA.sort()
    songsB.sort()
    songsC.sort()
    
    return songsA, songsB, songsC

def printSizeofPlaylists(pl1n, pl2n, s1, s2):
    print("The size of playlist " + pl1n + " is " + str(s1))
    print("The size of playlist " + pl2n + " is " + str(s2))
    print("")

def printPlaylists(a, message):
    print(message)
    print("   ")

    for i in a:
        print(i)
        
    print("   ")
    print("   ")


def main():
    print("Find the playlist ID of your YouTube playlists.")
    print("The playlist ID are the characters after “list=” in the playlist URL.")

    ################################
    ##### getting playlist ids #####
    ################################
    playlist1_id = input("Enter playlist id of the first playlist: ")

    playlist2_id = input("Enter playlist id of the second playlist: ")


    ###################
    ##### API key #####
    ###################
    DEVELOPER_KEY = "PUT YOUR DEVELOPER KEY HERE"


    ###########################
    ##### API information #####
    ###########################
    api_service_name = "youtube"
    api_version = "v3"


    ######################
    ##### API client #####
    ######################
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)


    ############################################
    ##### getting playlists names and size #####
    ############################################
    playlist1_name, size1 = getplaylistNameAndSize(youtube, playlist1_id)
    playlist2_name, size2 = getplaylistNameAndSize(youtube, playlist2_id)


    #############################
    ##### getting playlists #####
    #############################
    playlist1 = getplaylist(youtube, playlist1_id)
    playlist2 = getplaylist(youtube, playlist2_id)


    ####################################################################
    ##### comparing the two playlists, i.e playlist1 and playlist2 #####
    ####################################################################
    songs1, songs2, songsBoth = playlistCompare(playlist1, playlist2)


    ####################################
    ##### printing out information #####
    ####################################
    printSizeofPlaylists(playlist1_name, playlist2_name, size1, size2)

    printPlaylists(songsBoth, "songs in both playlists " + playlist1_name + " and " + playlist2_name + " :")

    printPlaylists(songs1, "songs in playlist " + playlist1_name + ", but not in playlist " + playlist2_name + " :")

    printPlaylists(songs2, "songs in playlist " + playlist2_name + ", but not in playlist " + playlist1_name + " :")


if __name__ == "__main__":
    main()

##########



