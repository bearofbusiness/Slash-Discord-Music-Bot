from discord import Embed, ButtonStyle


class Pages:
    main_page = {
        "title": "Ma Help", "description": "",
        "fields": [
            {"name": "General Help", "value": "General tips and tricks for using MaBalls"},
            {"name": "Adding Songs", "value" : "Commands for adding one or many songs to the queue"},
            {"name": "Removing Songs", "value" : "Commands for removing one or many songs from the queue"},
            {"name": "Queue Management", "value" : "Commands for modifying the queue"},
            {"name": "Other Commands", "value" : "Miscellaneous commands that don't fit into to any category"},
        ]
    }
    categories = {
        "General Help": { 
            "page" : {
                "title": "General Help", "description": "",
                "fields": [
                    {"name": "Permissions", "value": "This bot utilizes a permission system that uses **Song Authority** and **Discretionary Authority**, below are in-depth explanations for these terms."},
                    {"name": "Song authority", "value": "What categorizes **Song Authority** and what you can do with it."},
                    {"name": "Discretionary authority", "value": "What categorizes **Discretionary Authority** and what you can do with it."}
                ]
            },
            "buttons" : ["Permissions", "Song authority", "Discretionary authority"],
            "cat_style": ButtonStyle.primary
        },
        "Adding Songs": {
            "page" : {
                "title": "Adding Songs", "description": "",
                "fields": [
                    {"name": "play", "value": "Plays a song or adds it to the queue"},
                    {"name": "playlist", "value": "Adds all songs in a YouTube playlist to the queue"},
                    {"name": "search", "value": "Searches for a song and allows you to add it to the queue"},
                ]
            },
            "buttons" : ["play", "playlist", "search"],
            "cat_style": ButtonStyle.success
        },
        "Removing Songs": {
            "page" : {
                "title": "Removing Songs", "description": "",
                "fields": [
                    {"name": "remove index", "value": "Removes a song from the queue by its index"},
                    {"name": "remove user", "value": "Removes all songs from the queue that was added by a given user"},
                    {"name": "remove duplicates", "value": "Remove all duplicate songs from the queue"},
                ]
            },
            "buttons" : ["remove index", "remove user", "remove duplicates"],
            "cat_style": ButtonStyle.danger
        },
        "Queue Management": {
            "page" : {
                "title": "Queue Management", "description": "",
                "fields": [
                    {"name": "queue", "value": "Lists all of the songs in the queue"},
                    {"name": "clear", "value": "Clears the queue"},
                    {"name": "shuffle", "value": "Shuffles the queue"},
                    {"name": "loop single", "value": "Loops the current song"},
                    {"name": "loop queue", "value": "Loops the queue"},
                    {"name": "loop true", "value": "A third, more sinister looping option"},
                    {"name": "skip", "value": "Skips the playing song"},
                    {"name": "force-skip", "value": "Force skips the playing song"},
                ]
            },
            "buttons" : ["queue", "clear", "shuffle", "loop single", "loop queue", "loop true", "skip", "force-skip"],
            "cat_style": ButtonStyle.secondary
        },
        "Other Commands": {
            "page" : {
                "title": "Other Commands", "description": "",
                "fields": [
                    {"name": "help", "value": "This command"},
                    {"name": "settings", "value": "Get or set the bot's settings for the server"},
                    {"name": "ping", "value": "A diagnostic command to make sure the bot is running"},
                    {"name": "join", "value": "Have MaBalls join the voice channel you are connected to"},
                    {"name": "leave", "value": "Have MaBalls disconnect from its voice channel"},
                    {"name": "inspect", "value": "Get information about a song in the queue by its index"},
                    {"name": "replay", "value": "Restarts the current song"},
                    {"name": "pause", "value": "Pauses the current song"},
                    {"name": "resume", "value": "Resumes the current song"},
                    {"name": "now", "value": "Gets the song that is currently playing"},
                    {"name": "force-reset-player", "value": "Did something go wrong while listening?  Run this command and it will (hopefully) sort it out!"},
                    {"name": "update", "value": "Updates all bot libraries to maintain functionality, this command is disabled by default. To enable this command, see \"Cogs\" in the readme on this bot's repository or check README.md"}
                ]
            },
            "buttons" : ["help", "settings", "ping", "join", "leave", "inspect",  "replay", "pause", "resume", "now"],
            "cat_style": ButtonStyle.secondary
        }
    }
    #indepth command pages
    ind_commands = {
        "Permissions": {
            "title": "Permissions", "description": """This bot utilizes a permission system that has **Song Authority** and **Discretionary Authority**, below are in-depth explanations for these terms.\n
            This system has been put in place to attempt to restrict malicious users from being able to disrupt those listening (ie, having the bot disconnect with 46 curated songs in the queue)""",
            "fields":[]
        },
        "Song authority": {
            "title": "Song authority", "description": "**Song Authority** is a limited form of **Discretionary Authority**, It gives the user control over a song that they queued, not control over the queue or songs that others have queued.\nEx. You may skip a song that you queued with no vote, you may vote to skip someone else's song, you may not effect the queue in any way",
            "fields":[]
        },
        "Discretionary authority": {
            "title": "Discretionary authority", "description": """**Discretionary Authority** grants a user full control over the bot and its playback, not including being able to change settings\n
            Ex. You will be able to skip anybody's songs without calling a vote
            Ex. You will be able to remove all of the songs queued by a user
            Ex. Depending on MaBalls' settings, **Discretionary Authority** may be the only way to be able to queue playlists
                
            **Discretionary Authority** is granted through a few different means:\n
                If the number of users in the voice channel is less than 4 (to allow smaller listening groups to have more freedom)\n
                If the user has a role named "DJ" (the permissions associated with it do not affect the authority)\n
                If the user has the "Manage Channels" or "Administrator" permissions
            """,
            "fields":[]
        },
        "help": {
            "title": "help", "description": "This command\nDumbass",
            "fields": [
                # would put fields here ex.{"name": "ping", "value": "This command is used to check if the bot is working"}, etc...
            ]
        },
        "settings": {
            "title": "settings", "description": "Allows you to customize MaBalls to your server\nRun the command to view the different settings and their explanations\nRequires **Discretionary Authority** (see help->general)",
            "fields": []
        },
        "ping": {
            "title": "ping", "description": "A diagnostic command to make sure the bot is running",
            "fields": []
        },
        "join": {
            "title": "join", "description": "Have MaBalls join the voice channel you are connected to",
            "fields": []
        },
        "leave": {
            "title": "leave", "description": "Have MaBalls disconnect from its voice channel",
            "fields": []
        },
        "play": {
            "title": "play", "description": "Plays a song or adds it to the queue\nIf given a playlist it will play only the first song in the playlist\n\n Options:",
            "fields": [
                {"name": "link", "value": "The link to the song\n Supports playback of anything YT-DLP is able to handle, so almost anything at all."},
                {"name": "top", "value": "Puts the song at the top of the queue\nRequires DJ role or the Manage Channels permission"},
            ]
        },
        "skip": {
            "title": "skip", "description": "Skips the playing song\nThis may cause a vote for the song to be skipped, but if the user has **Song Authority** (see help->general) it will be bypassed.",
            "fields": []
        },
        "force-skip": {
            "title": "force-skip", "description": "Force skips the playing song\nRequires **Discretionary Authority** (see help->general)",
            "fields": []
        },
        "queue": {
            "title": "queue", "description": "Lists all of the songs in the queue",
            "fields": []
        },
        "now": {
            "title": "now", "description": "Get the song that is currently playing",
            "fields": []
        },
        "remove index": {
            "title": "remove index", "description": "Removes a song from the queue by its index\nRequires **Song Authority** (see help->general)\n\nOptions:",
            "fields": [
                {"name": "index", "value": "The index of the song to remove.\nThis can be found from the queue command (see help->queue)"}
            ]
        },
        "remove user": {
            "title": "remove user", "description": "Removes all songs from the queue that was added by a given user\nRequires **Discretionary Authority** (see help->general)",
            "fields": [
                {"name": "user", "value": "The user who's songs should be removed from the queue"}
            ]
        },
        "remove duplicates": {
            "title": "remove duplicates", "description": "Remove all duplicate songs from the queue\nRequires **Discretionary Authority** (see help->general)",
            "fields": []
        },
        "playlist": {
            "title": "playlist", "description": "Adds all songs in a YouTube playlist to the queue\nThis command is more powerful than you may think; try giving it links to a channel or a Mix playlist...\nMay require **Discretionary Authority** or may be disabled in your server by settings (see help->general and help->other)",
            "fields": [
                {"name": "link", "value": "The link to the playlist"}
            ]
        },
        "search": {
            "title": "search", "description": "Searches for a song and allows you to add it to the queue",
            "fields": [
                {"name": "query", "value": "The query to search for"}
            ]
        },
        "clear": {
            "title": "clear", "description": "Clears the queue\nRequires **Discretionary Authority** (see help->general)",
            "fields": []
        },
        "shuffle": {
            "title": "shuffle", "description": "Shuffles the queue\nRequires **Discretionary Authority** (see help->general)",
            "fields": []
        },
        "pause": {
            "title": "pause", "description": "Pauses the current song",
            "fields": []
        },
        "resume": {
            "title": "resume", "description": "Resumes the current song",
            "fields": []
        },
        "loop single": {
            "title": "loop single", "description": "Loops the current song",
            "fields": []
        },
        "loop queue": {
            "title": "loop queue", "description": "Loops the queue, so that when a song finishes it is added to the end of the queue",
            "fields": []
        },
        "loop true": {
            "title": "loop true", "description": "Similar to `loop queue` but it attempts to mask the looping of the songs by adding them into pseudorandom positions in the queue",
            "fields": []
        },
        "inspect": {
            "title": "inspect", "description": "Get information about a song in the queue by its index",
            "fields": [
                {"name": "index", "value": "The index of the song to inspect\nRequires **Song Authority** (see help->general)"}
            ]
        },
        "replay": {
            "title": "replay", "description": "Restarts the current song",
            "fields": []
        }
    }

    @staticmethod
    @DeprecationWarning
    def get_page(command: str) -> dict:
        return Pages.ind_commands[command]
    
    #list of buttons for pages
    #when you hit general help it will return list of buttons and an embed
    @staticmethod
    def get_main_page() -> dict:
        return Pages.main_page


    @staticmethod
    def get_category(cat: str) -> dict:
        return Pages.categories[cat]


    @staticmethod
    def get_command_page(page: str) -> dict:
        return Pages.ind_commands[page]