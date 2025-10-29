import sqlite3
from datetime import datetime

from discord.utils import SequenceProxy
from discord import Guild
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

    def create_tables() -> None:
        """
        Creates the tables in the database if they don't exist.
        """
        try:
            DB._cursor.execute("""
                    CREATE TABLE GuildSettings (
                        guild_id INTEGER PRIMARY KEY,
                        np_sent_to_vc BOOLEAN DEFAULT '1',
                        verbose_np BOOLEAN DEFAULT '1',
                        remove_orphaned_songs BOOLEAN DEFAULT '0',
                        song_breadcrumbs BOOLEAN DEFAULT '1'
                    )
            """)

            DB._settings_db.commit()
        except sqlite3.OperationalError:
            pass

    def fix_column_values() -> None:
        columns = [['np_sent_to_vc',"1"], ['verbose_np', "1"], ['remove_orphaned_songs',"0"], ['allow_playlist',"1"], ['song_breadcrumbs', "1"]]
        for i in columns:
            try:
                DB._cursor.execute(f"ALTER TABLE GuildSettings ADD COLUMN {i[0]} BOOLEAN DEFAULT '{i[1]}'")
                DB._settings_db.commit()
            except:
                pass
        pass

    def initalize_servers_in_DB(guilds: SequenceProxy) -> None:
        for guild in list(guilds):
            #print(guild.id)
            DB.GuildSettings.create_new_guild(guild.id)
    
    def initalize_server_in_DB(guild: Guild) -> None:
            DB.GuildSettings.create_new_guild(guild.id)

    class GuildSettings:
        """
        A static subclass of DB providing higher level querying of the GuildSettings SQL table containing guild-specific options.

        ...

        Methods
        -------
        get(guild_id: `int`, setting: `str`):
            Gets a requested column from a guild by ID.

        set(guild_id: `int`, setting: `str` value: `str` | `bool` | `int`):
            Sets a requested column from a guild by ID
        """
        def create_new_guild(guild_id: int) -> None:
            DB._cursor.execute(f"INSERT OR IGNORE INTO GuildSettings (guild_id) VALUES ({guild_id})")
            DB._settings_db.commit()

        def remove_guild(guild_id: int) -> None:
            DB._cursor.execute(f"DELETE FROM GuildSettings WHERE guild_id = {guild_id}")
            DB._settings_db.commit()

        def __setting_check(setting: str) -> str:
            """
            Provides column sanitization for the GuildSettings table.

            Parameters
            ----------
            setting : `str`
                The string to sanitize

            Raises
            ------
            ValueError
                Raised if the setting is not a valid column

            Returns
            -------
            setting : str
                The setting argument.
            """
            match setting:
                case 'guild_id':
                    return setting
                case 'verbose_np':
                    return setting
                case 'np_sent_to_vc':
                    return setting
                case 'remove_orphaned_songs':
                    return setting
                case 'allow_playlist':
                    return setting
                case 'song_breadcrumbs':
                    return setting
                case default:
                    raise ValueError(f'Invalid setting value supplied ({default})')

        def get(guild_id: int, setting: str) -> str | bool | int:
            """
            Gets a requested column from a guild by ID.

            Parameters
            ----------
            guild_id : `int`
                The guild to get the setting from.
            setting : `str`
                The setting to get.

                
                The valid values are:

                    > guild_id

                    > np_sent_to_vc

                    > verbose_np

                    > remove_orphaned_songs

                    > allow_playlist

                    > song_breadcrumbs
            """
            DB._cursor.execute(f"SELECT {DB.GuildSettings.__setting_check(setting)} FROM GuildSettings WHERE guild_id = ?", (guild_id,))
            return DB._cursor.fetchone()[0]
        
        def set(guild_id: int, setting: str, value: str | bool | int) -> None:
            """
            Sets a requested column from a guild by ID.

            Parameters
            ----------
            guild_id : `int`
                The guild to change the setting in.
            setting : `str`
                The setting to set.

                The Valid values are:

                    > guild_id

                    > np_sent_to_vc
                    
                    > verbose_np

                    > remove_orphaned_songs

                    > song_breadcrumbs
            value : `str` | `bool` | `int`
                The value to update the field with.
            """
            DB._cursor.execute(f"UPDATE GuildSettings SET {DB.GuildSettings.__setting_check(setting)} = ? WHERE guild_id = ?", (value, guild_id))
            DB._settings_db.commit()
            return