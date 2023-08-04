import sqlite3

class DB:
    """
    A static class containing subclasses for accessing and mutating columns in various SQL tables.

    ...
    
    Subclasses
    ----------
    GuildSettings:
        A static subclass that provides access to guild-specific options.
    """
    _settings_db = sqlite3.connect('settings.db')
    _cursor = _settings_db.cursor()
    # def on_start() -> None:
    #     """
    #     runs to connect the database and ready important variables
    #     """
    #     __settings_db = sqlite3.connect('settings.db')
    #     __cursor = __settings_db.cursor()
    #     print("Connected to database")
    
    class GuildSettings:
        """
        A static subclass of DB providing higher level querying of the GuildSettings SQL table containing guild-specific options.

        ...

        Methods
        -------
        get(guild_id: int, setting: str):
            Gets a requested column from a guild by ID.

        set(guild_id: int, setting: str value: str | bool | int):
            Sets a requested column from a guild by ID
        """
        def __setting_check(setting: str) -> str:
            """
            Provides column sanitization for the GuildSettings table.

            Parameters
            ----------
            setting : str
                The string to sanitize

            Raises
            ------
            ValueError
                Raised if the setting is not a valid column

            Returns
            -------
            str:
                The setting argument.
            """
            match setting:
                case 'guild_id':
                    return setting
                case 'np_sent_to_vc':
                    return setting
                case 'remove_orphaned_songs':
                    return setting
                case default:
                    raise ValueError(f'Invalid setting value supplied ({default})')

        def get(guild_id: int, setting: str) -> str | bool | int:
            """
            Gets a requested column from a guild by ID.

            Parameters
            ----------
            guild_id : int
                The guild to get the setting from.
            setting : str
                The setting to get.

                
                The valid values are:

                    > guild_id

                    > np_sent_to_vc

                    > remove_orphaned_songs
            """
            DB._cursor.execute(f"SELECT {DB.GuildSettings.__setting_check(setting)} FROM GuildSettings WHERE guild_id = ?", (guild_id,))
            return DB._cursor.fetchone()[0]
        
        def set(guild_id: int, setting: str, value: str | bool | int) -> None:
            """
            Sets a requested column from a guild by ID.

            Parameters
            ----------
            guild_id : int
                The guild to change the setting in.
            setting : str
                The setting to set.


                The Valid values are:

                    > guild_id

                    > np_sent_to_vc

                    > remove_orphaned_songs
            value : str | bool | int
                The value to update the field with.
            """
            DB._cursor.execute(f"UPDATE GuildSettings SET {DB.GuildSettings.__setting_check(setting)} = ? WHERE guild_id = ?", (value, guild_id))
            DB._settings_db.commit()
            return