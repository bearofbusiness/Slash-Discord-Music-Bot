from discord import Embed, ButtonStyle


class Pages:
    main_page = {
        "title": "Ma Help", "description": "",
        "fields": [
            {"name": "General Help", "value": "General tips and tricks for using MaBalls"},
            {"name": "Adding Songs", "value" : "Commands for adding one or many songs to the queue"},
            {"name": "Removing Songs", "value" : "Commands for removing one or many songs from the queue"},
            {"name": "Queue Management", "value" : "Commands for modifying the queue"},
            {"name": "Other Commands", "value" : "miscellaneous commands that don't fit into to any category"},
        ]
    }
    categories = {
        "General Help": { 
            "page" : {
                "title": "General Help", "description": "",
                "fields": [
                ]
            },
            "buttons" : [],
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
                    {"name": "remove", "value": "This command is used to remove a song from the queue"},
                    {"name": "removeuser", "value": "This command is used to remove all songs from the queue that was added by a user"},
                    {"name": "removeduplicates", "value": "Remove all duplicate songs from the queue"},
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
                    {"name": "loop", "value": "This command is used to loop the playing song"},
                    {"name": "loopqueue", "value": "This command is used to loop the queue"},
                    {"name": "trueloop", "value": "Loops queue but when done doesn't add to the end it adds it in randomly into the queue"},
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
                {"name": "now", "value": "This command is used to get the song that is currently playing"}

                ]
            },
            "buttons" : ["help", "settings", "ping", "join", "leave", "inspect",  "replay", "pause", "resume", "now"],
            "cat_style": ButtonStyle.secondary
        }
    }
    temp = {
        "title": "Ma Help", "description": "",
        "fields": [
            {"name": "help", "value": "This command is used to get help"},
            {"name": "settings", "value": "Get or set the bot's settings for your server"},
            {"name": "ping", "value": "This command is used to check if the bot is working"},
            {"name": "join", "value": "This command is used to join a voice channel"},
            {"name": "leave", "value": "This command is used to leave a voice channel"},
            {"name": "play", "value": "This command is used to play a song from youtube. if given a playlist it will pick the first song in the playlist"},
            {"name": "skip", "value": "This command is used to skip the playing song"},
            {"name": "forceskip", "value": "This command is used to force skip the playing song. requires the manage channels permission"},
            {"name": "queue", "value": "This command is used to get the queue of songs"},
            {"name": "now", "value": "This command is used to get the song that is currently playing"},
            {"name": "remove",
                "value": "This command is used to remove a song from the queue"},
            {"name": "removeuser",
             "value": "This command is used to remove all songs from the queue that was added by a user"},
            {"name": "removeduplicates", "value": "Remove all duplicate songs from the queue"},
            {"name": "playlist", "value": "This command is used to get a playlist from youtube and add it to the queue"},
            {"name": "search", "value": "This command is used to search for a song on youtube and add it to the queue"},
            {"name": "clear", "value": "This command is used to clear the queue"},
            {"name": "shuffle", "value": "This command is used to shuffle the queue"},
            {"name": "pause", "value": "This command is used to pause the playing song"},
            {"name": "resume", "value": "This command is used to resume the playing song"},
            {"name": "loop", "value": "This command is used to loop the playing song"},
            {"name": "loopqueue", "value": "This command is used to loop the queue"},
            {"name": "trueloop", "value": "Loops queue but when done doesn't add to the end it adds it in randomly into the queue"},
            {"name": "inspect", "value": "Get information about a song in the queue"},
            {"name": "replay", "value": "Restarts the current song"}
        ]
    }
    #indepth command pages
    ind_commands = {
        "help": {
            "title": "help", "description": "This command is used to get help",
            "fields": [
                # would put fields here ex.{"name": "ping", "value": "This command is used to check if the bot is working"}, etc...
            ]
        },
        "settings": {
            "title": "settings", "description": "Get or set the bot's settings for your server",
            "fields": []
        },
        "ping": {
            "title": "ping", "description": "This command is used to check if the bot is working",
            "fields": [
            ]
        },
        "join": {
            "title": "join", "description": "This command is used to join a voice channel",
            "fields": []
        },
        "leave": {
            "title": "leave", "description": "This command is used to leave a voice channel",
            "fields": []
        },
        "play": {
            "title": "play", "description": "This command is used to play a song from youtube. if given a playlist it will pick the first song in the playlist",
            "fields": []
        },
        "skip": {
            "title": "skip", "description": "This command is used to skip the playing song",
            "fields": []
        },
        "forceskip": {
            "title": "forceskip", "description": "This command is used to force skip the playing song. requires the manage channels permission",
            "fields": []
        },
        "queue": {
            "title": "queue", "description": "This command is used to get the queue of songs",
            "fields": []
        },
        "now": {
            "title": "now", "description": "This command is used to get the song that is currently playing",
            "fields": []
        },
        "remove": {
            "title": "remove", "description": "This command is used to remove a song from the queue",
            "fields": []
        },
        "removeuser": {
            "title": "removeuser", "description": "This command is used to remove all songs from the queue that was added by a user",
            "fields": []
        },
        "removeduplicates": {
            "title": "removeDuplicates", "description": "Remove all duplicate songs from the queue",
            "fields": []
        },
        "playlist": {
            "title": "playlist", "description": "This command is used to get a playlist from youtube and add it to the queue",
            "fields": [{"name": "Can play youtube Mixes", "value": "yes"}]
        },
        "search": {
            "title": "search", "description": "This command is used to search for a song on youtube and add it to the queue",
            "fields": []
        },
        "clear": {
            "title": "clear", "description": "This command is used to clear the queue",
            "fields": []
        },
        "shuffle": {
            "title": "shuffle", "description": "This command is used to shuffle the queue",
            "fields": []
        },
        "pause": {
            "title": "pause", "description": "This command is used to pause the playing song",
            "fields": []
        },
        "resume": {
            "title": "resume", "description": "This command is used to resume the playing song",
            "fields": []
        },
        "loop": {
            "title": "loop", "description": "This command is used to loop the playing song",
            "fields": []
        },
        "loopqueue": {
            "title": "loopqueue", "description": "This command is used to loop the queue",
            "fields": []
        },
        "trueloop": {
            "title": "trueLoop", "description": "Loops queue but when done doesn't add to the end it adds it in randomly into the queue",
            "fields": []
        },
        "inspect": {
            "title": "inspect", "description": "Get information about a song in the queue",
            "fields": []
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