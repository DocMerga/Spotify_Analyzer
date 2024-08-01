import requestToken
import dumpPlaylistData
import database
import playlistToMainDB
import streamsToMainDB
import updateMainDB
import updateLocations
import checkPlaycount

#TODO: 
#Export of all Track(with album, artist,...) data in csv? or save in extra DB?
#Error Exceptions (for Database Managment and others) if tables are not created
#5917 artists with missing location data
#5278
#4801
#2386
# Get Location using: https://python-musicbrainzngs.readthedocs.io/en/v0.7.1/api/#musicbrainzngs.search_artists
###206598 city unknown playcounts --> 102404
###161457 city & country unknown playcounts  --> 54704

#For sub programm that deletes unknown location attributions --> set musicbrainz retrieved =0
#Update playcounts per subprogram

# for musicbrainz import --> if not Unknown but Null in current country --> should use mb result
#399161



access_token = None

while True:
    ###User chooses the Task
    print("""Options:
                - Request Spotify Token - Enter 1
                - Import Spotify playlist (\dump) and parse Data - Enter 2 
                - Read in Streaming History (\streams) - Enter 3
                - Update main database - Enter 4
                - Locations Managment - Enter 5
                - Database Managment - Enter 6
                - Exit application - Enter 7""")
    options = 11 #number of options

    while True:   #loop is continued until User enters valid number
        
        user_input = input("Choose Task: ")

        try:
            user_input = int(user_input)
            if user_input < 1 or user_input > options:
                print("Error: Please enter valid number")
                continue
            else:
                break
        except:
            print("Error: Only integer input allowed")
            continue

    ###Task selection based on the user input
    if user_input == 1:
        access_token = requestToken.requestToken()
        print("Spotify Token retrieved")               
    
    elif user_input == 2:
        if access_token is None: 
            print("Error: No access token generated yet.")
            continue
        spotify_playlist_id = input("Enter spotify playlist ID: ") #Test-Playlist: "6bZQf3FIsrC1uQ66swFrLg"        
        spotify_playlist_name = input("Enter name of the playlist (cannot be changed once given to an id): ")
        dumpPlaylistData.dump(access_token, spotify_playlist_id)    
        playlistToMainDB.parse_playlist(spotify_playlist_id, spotify_playlist_name)

    elif user_input == 3:
        streamsToMainDB.streamsToMainDB()

    elif user_input == 4:
        if access_token is None: 
            print("Error: No access token generated yet.")
            continue       

        while True:
            missing = updateMainDB.updateNumbers()
            print("Choose Task:")
            print("    - Tracks with info missing:", missing[0], "- for track update enter: t" )
            print("    - Albums with info missing:", missing[1], "- for album update enter: a" )
            print("    - Artists with info missing:", missing[2], "- for album update enter: r" )
            print("    - Tracks with Audio-Features missing:", missing[3], "- for album update enter: f" )
            print("    - Exit Update Selection: x")
            update_selection = input("Select Update Task: ")
            if update_selection == "t":
                try:
                    number_tracks = int(input("How many Tracks should be updated (+-50 steps): "))
                except:
                    print("Enter valid integer")
                    continue
                if number_tracks < 1:
                    print("Enter a integer >0")
                    continue
                updateMainDB.updateTracks(access_token, number_tracks)
                continue
            if update_selection == "a":
                try:
                    number_albums = int(input("How many Albums should be updated (+-20 steps): "))
                except:
                    print("Enter valid integer")
                    continue
                if number_albums < 1:
                    print("Enter a integer >0")
                    continue
                updateMainDB.updateAlbums(access_token, number_albums)
                continue
            if update_selection == "r":
                try:
                    number_artists = int(input("How many Albums should be updated (+-50 steps): "))
                except:
                    print("Enter valid integer")
                    continue
                if number_artists < 1:
                    print("Enter a integer >0")
                    continue
                updateMainDB.updateArtists(access_token, number_artists)
                continue
            if update_selection == "f":
                try:
                    number_tracks = int(input("How many Track Audio Feautres should be updated (+-50 steps): "))
                except:
                    print("Enter valid integer")
                    continue
                if number_tracks < 1:
                    print("Enter a integer >0")
                    continue
                updateMainDB.updateAudioFeatures(access_token, number_tracks)
                continue
            if update_selection == "x":
                break

            else:
                print("ERROR: no valid selection")
                continue

    elif user_input == 5:         
            while True:
                missing = updateLocations.locationNumbers()
                print(f"\n{missing[0]} artists with missing location data")
                print(f"\n{missing[1]} locations with missing coordinates")
                print(f"\n{missing[2]} artists with missing musicbrainz validation")
                print("""Options:
                            - Update from existing csv - c
                            - Update from ChatGPT API - a
                            - Update from musicbrainz API - m
                            - Delete Unknown locations - d
                            - Get coordinates from Google Maps API - g
                            - Export locations as csv - e
                            - Exit Selection - x""")
                location_selection = input("Select Update Task: ")
                if location_selection == "c":
                    updateLocations.updateFromCSV()
                    continue

                elif location_selection == "a":
                    try:
                        iterations = int(input("How many iterations do you want to run (+-50 steps): "))
                    except:
                        print("Enter valid integer")
                        continue
                    if iterations < 1:
                        print("Enter a integer >0")
                        continue
                    updateLocations.updateLocationChatGPT(iterations)
                    continue

                elif location_selection == "m":
                    try:
                        number_artists_mb = int(input("How many artists do you want to update: "))
                    except:
                        print("Enter valid integer")
                        continue
                    if number_artists_mb < 1:
                        print("Enter a integer >0")
                        continue
                    updateLocations.updateLocationWithMusicbrainz(number_artists_mb)
                    continue

                elif location_selection == "d":
                    updateLocations.deleteUnknownLoc()
                    continue
                    
                elif location_selection == "g":
                    try:
                        number_locations = int(input("Of how many locations do you want to get the coordinates: "))
                    except:
                        print("Enter valid integer")
                        continue
                    if number_locations < 1:
                        print("Enter a integer >0")
                        continue
                    updateLocations.updateCoordinates(number_locations)
                    continue

                elif location_selection == "e":
                    updateLocations.exportLocations()
                    continue

                elif location_selection == "x":
                    break

                else:
                    print("ERROR: no valid selection")
                    continue

    elif user_input ==6:
        while True:
            print("""Options:   
                        - Generate main database - Enter g
                        - Drop all tables from main database - Enter d
                        - Recalculate playcount - Enter r
                        - Check playcounts - Enter c
                        - Exit selection - Enter x""")
            db_selection = input("Enter selection: ")

            if db_selection == "g":
                database.generate_db()
                print("All Tables of main_database.sqlite generated if not already existed.")
                continue

            elif db_selection == "d":
                confirm = input("Do you really want do drop all tables from the main database with all data (y/n)? ")
                if confirm == "y":
                    database.drop_db()
                    print("All database tables were dropped.")
                elif confirm == "n":
                    print("Task stopped")
                    continue
                else:
                    print("Unexpected user input")
                    continue

            elif db_selection == "r":
                streamsToMainDB.recalculatePlaycounts()
                
            elif db_selection == "c":
                checkPlaycount.calculateOverallPlaycount("Track")
                checkPlaycount.calculateOverallPlaycount("Isrc")
                checkPlaycount.calculateOverallPlaycount("Artist")
                checkPlaycount.calculateOverallPlaycount("Album")
                checkPlaycount.calculateOverallPlaycount("Genre")
                checkPlaycount.calculateOverallPlaycount("Location")
                checkPlaycount.calculateOverallPlaycount("Country")
                checkPlaycount.calculateOverallPlaycount("CountryList")

            elif db_selection == "x":
                break

            else:
                print("ERROR: no valid selection")
                continue
    

    elif user_input == 7:
        print("--Application terminated--")
        exit()

