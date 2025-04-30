API Calls:

# *Example Call for getting Replays of one player with Player-ID (Steam):*
curl -v -H "Authorization:2G4qWlMq3vQEFD4eMwFdx3lKwXpL5BgdiLdSGfv7" "https://ballchasing.com/api/replays?player-id=steam:76561198087548781"

# *Example Call for getting Replays of one player with Player-Name (Much more volatile -> "Hiryu" also retrieves "Hiryuu" etc.)*
curl -v -H "Authorization:2G4qWlMq3vQEFD4eMwFdx3lKwXpL5BgdiLdSGfv7" "https://ballchasing.com/api/replays?player-name=Hiryu"