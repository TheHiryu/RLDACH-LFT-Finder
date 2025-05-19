# RLDACH-LFT-Finder
A Data Science project to find the most suitable teammates in Rocket League, based on the Top 1000 German Players

For downloading replay data and updating the Top 1000 player list (German Players, Top 1000 2v2, Steam) start DownloadLauncher.py
Current API Limits (ballchasing.com): 4 replays/second, 5000 replays/hour

To initialize the database (for when you want to create a server) start database-init.py. It will create and init a table in the postgres database defined in docker-compose.yml based on the data in all replay files
The initialization of the database takes ~15mins 
