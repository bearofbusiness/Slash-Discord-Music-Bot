import sqlite3
"""
Small script for setting up the initial database table.
"""
db = sqlite3.connect('settings.db')
cursor = db.cursor()
try:
    cursor.execute("""
            CREATE TABLE GuildSettings (
                guild_id INTEGER PRIMARY KEY,
                np_sent_to_vc BOOLEAN DEFAULT '1',
                remove_orphaned_songs BOOLEAN DEFAULT '0',
                song_breadcrumbs BOOLEAN DEFAULT '1'
            )
    """)
except sqlite3.OperationalError:
    pass
db.close()