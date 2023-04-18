from discord import Embed


class Pages:

    main_page = {
        "title": "Ma Help", "description": "",
        "fields": [
            {"name": "ping", "value": "This command is used to check if the bot is working"},
            {"name": "help", "value": "This command is used to get help"},
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
            {"name": "playlist", "value": "This command is used to get a playlist from youtube and add it to the queue"},
            {"name": "search", "value": "This command is used to search for a song on youtube and add it to the queue"},
            {"name": "clear", "value": "This command is used to clear the queue"},
            {"name": "shuffle", "value": "This command is used to shuffle the queue"},
            {"name": "pause", "value": "This command is used to pause the playing song"},
            {"name": "resume", "value": "This command is used to resume the playing song"},
            {"name": "loop", "value": "This command is used to loop the playing song"},
            {"name": "loop_queue", "value": "This command is used to loop the queue"}
        ]
    }
    ind_commands = {
        "ping": {
            "title": "ping", "description": "This command is used to check if the bot is working",
            "fields": [
                # would put fields here ex.{"name": "ping", "value": "This command is used to check if the bot is working"}, etc...
            ]
        },
        "help": {
            "title": "help", "description": "This command is used to get help",
            "fields": []
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
        "playlist": {
            "title": "playlist", "description": "This command is used to get a playlist from youtube and add it to the queue",
            "fields": []
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
        "loop_queue": {
            "title": "loopqueue", "description": "This command is used to loop the queue",
            "fields": []
        }
    }

    @staticmethod
    def get_page(command: str) -> dict:
        return Pages.ind_commands[command]
