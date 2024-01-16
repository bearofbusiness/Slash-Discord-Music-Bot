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
                    {"name": "Permissions", "value": "This bot has a permissions system based off of Rythm\nSee below for a more in-depth explanation"},
                    {"name": "Song authority", "value": "What categorizes 'song authority' and what you can do with it."},
                    {"name": "Discretionary authority", "value": "What categorizes 'discretionary authority' and what you can do with it."}
                ]
            },
            "buttons" : ["Permissions", "Song authority", "Discretionary authority"],
            "cat_style": ButtonStyle.primary
        },
        "Adding Songs": {
            "page" : {
                "title": "Adding Songs", "description": "",
                "fields": [
                    {"name": "play", "value": "This command is used to play a song from youtube. if given a playlist it will pick the first song in the playlist"},
                    {"name": "playlist", "value": "This command is used to get a playlist from youtube and add it to the queue"},
                    {"name": "search", "value": "This command is used to search for a song on youtube and add it to the queue"},
                ]
            },
            "buttons" : ["play", "playlist", "search"],
            "cat_style": ButtonStyle.success
        },
        "Removing Songs": {
            "page" : {
                "title": "Removing Songs", "description": "",
                "fields": [
                    {"name": "remove single", "value": "This command is used to remove a song from the queue"},
                    {"name": "remove user", "value": "This command is used to remove all songs from the queue that was added by a user"},
                    {"name": "remove duplicates", "value": "Remove all duplicate songs from the queue"},
                ]
            },
            "buttons" : ["remove", "removeuser", "removeduplicates"],
            "cat_style": ButtonStyle.danger
        },
        "Queue Management": {
            "page" : {
                "title": "Queue Management", "description": "",
                "fields": [
                    {"name": "queue", "value": "This command is used to get the queue of songs"},
                    {"name": "clear", "value": "This command is used to clear the queue"},
                    {"name": "shuffle", "value": "This command is used to shuffle the queue"},
                    {"name": "loop single", "value": "This command is used to loop the playing song"},
                    {"name": "loop queue", "value": "This command is used to loop the queue"},
                    {"name": "loop true", "value": "Loops queue but when done doesn't add to the end it adds it in randomly into the queue"},
                    {"name": "skip", "value": "This command is used to skip the playing song"},
                    {"name": "forceskip", "value": "This command is used to force skip the playing song. requires the manage channels permission"},
                ]
            },
            "buttons" : ["queue", "clear", "shuffle", "loop", "loopqueue", "trueloop", "skip", "forceskip"],
            "cat_style": ButtonStyle.secondary
        },
        "Other Commands": {
            "page" : {
                "title": "Other Commands", "description": "",
                "fields": [
                {"name": "help", "value": "This command is used to get help"},
                {"name": "settings", "value": "Get or set the bot's settings for your server"},
                {"name": "ping", "value": "This command is used to check if the bot is working"},
                {"name": "join", "value": "This command is used to join a voice channel"},
                {"name": "leave", "value": "This command is used to leave a voice channel"},
                {"name": "inspect", "value": "Get information about a song in the queue"},
                {"name": "replay", "value": "Restarts the current song"},
                {"name": "pause", "value": "This command is used to pause the playing song"},
                {"name": "resume", "value": "This command is used to resume the playing song"},
                {"name": "now", "value": "This command is used to get the song that is currently playing"},
                {"name": "force-reset-player", "value": "Did something go wrong while listening?  Run this command and it will (hopefully) sort it out!"}

                ]
            },
            "buttons" : ["help", "settings", "ping", "join", "leave", "inspect",  "replay", "pause", "resume", "now"],
            "cat_style": ButtonStyle.secondary
        }
    }
    #indepth command pages
    ind_commands = {
        "Permissions": {
            "title": "Permissions", "description": """This bot has a permissions system similar to the Rythm bot - god rest its soul\n
            This system has been put in place to attempt to restrict malicious users from being able to disrupt those listening (ie, having the bot disconnect with 46 curated songs in the queue)""",
            "fields":[]
        },
        "Song authority": {
            "title": "Song authority", "description": "Song authority gives a user control over a song they have queued\nThis is like a more limited form of discretionary authority\nEx. You will be able to skip a song you have queued without a vote but not somebody else's\nEx. You will not be able to shuffle the queue",
            "fields":[]
        },
        "Discretionary authority": {
            "title": """Discretionary authority", "description": "Discretionary authority grants a user full control over the bot and its playback, not including being able to change settings\n
            Ex. You will be able to skip anybody's songs without calling a vote
            Ex. You will be able to remove all of the songs queued by a user
            Ex. Depending on MaBalls' settings, discretionary authority may be the only way to be able to queue playlists
                
            Discretionary authority is granted through a few different means:\n
                If the number of users in the voice channel is less than 4 (to allow smaller listening groups to have more freedom)\n
                If the user has a role named "DJ" (the permissions associated with it do not affect the authority)\n
                If the user has the "Manage Channels" or "Administrator" permissions
            """,
            "fields":[]
        },
        "help": {
            "title": "help", "description": "This command is used to get help",
            "fields": [
                # would put fields here ex.{"name": "ping", "value": "This command is used to check if the bot is working"}, etc...
            ]
        },
        "settings": {
            "title": "settings", "description": "Allows you to customize MaBalls to your server\nRun the command to view the different settings and their explanations\nRequires discretionary authority (see help->general)",
            "fields": []
        },
        "ping": {
            "title": "ping", "description": "This command is used to check if the bot is working",
            "fields": []
        },
        "join": {
            "title": "join", "description": "This command is used to have MaBalls join the voice channel you are connected to",
            "fields": []
        },
        "leave": {
            "title": "leave", "description": "This command is used to have MaBalls disconnect from a voice channel",
            "fields": []
        },
        "play": {
            "title": "play", "description": "This command is used to play a song or add it to the queue\nIf given a playlist it will play only the first song in the playlist\n\n Options:",
            "fields": [
                {"name": "link", "value": "The link to the song\n Supports playback of anything YT-DLP is able to handle, so almost anything at all."},
                {"name": "top", "value": "Puts the song at the top of the queue\nRequires DJ role or the Manage Channels permission"},
            ]
        },
        "skip": {
            "title": "skip", "description": "Skips the playing song\nThis may cause a vote for the song to be skipped, but if the user has song authority (see help->general) it will be bypassed.",
            "fields": []
        },
        "force-skip": {
            "title": "forceskip", "description": "Force skip the playing song\nRequires discretionary authority (see help->general)",
            "fields": []
        },
        "queue": {
            "title": "queue", "description": "Lists all of the songs in the queue",
            "fields": []
        },
        "now": {
            "title": "now", "description": "This command is used to get the song that is currently playing",
            "fields": []
        },
        "remove index": {
            "title": "remove index", "description": "Removes a song from the queue by its index\nRequires song authority (see help->general)\n\nOptions:",
            "fields": [
                {"name": "index", "value": "The index of the song to remove.\nThis can be found from the queue command (see help->queue)"}
            ]
        },
        "remove user": {
            "title": "remove user", "description": "This command is used to remove all songs from the queue that was added by a user\nRequires discretionary authority (see help->general)",
            "fields": [
                {"name": "user", "value": "The user who's songs should be removed from the queue"}
            ]
        },
        "remove duplicates": {
            "title": "remove duplicates", "description": "Remove all duplicate songs from the queue\nRequires discretionary authority (see help->general)",
            "fields": []
        },
        "playlist": {
            "title": "playlist", "description": "This command is used to get a playlist from youtube and add it to the queue\nThis command is more powerful than you may think; try giving it links to a channel or a Mix playlist...\nMay require discretionary authority or may be disabled in your server by settings (see help->general and help->other)",
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
            "title": "clear", "description": "Clears the queue\nRequires discretionary authority (see help->general)",
            "fields": []
        },
        "shuffle": {
            "title": "shuffle", "description": "Shuffles the queue\nRequires discretionary authority (see help->general)",
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
                {"name": "index", "value": "The index of the song to inspect\nRequires song authority (see help->general)"}
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