import sqlite3

db = sqlite3.connect('settings.db')
cursor = db.cursor()

cursor.execute("""
        CREATE TABLE GuildSettings (
            guild_id INTEGER PRIMARY KEY,
            np_sent_to_vc BOOLEAN DEFAULT '1',
            remove_orphaned_songs BOOLEAN DEFAULT '0'
        )
""")

db.commit()

cursor.execute("""
        INSERT INTO GuildSettings (guild_id) VALUES (1008950152737849415)
    """)

db.commit()

testvar = 'np_sent_to_vc'
cursor.execute(f"""
        SELECT {testvar} FROM GuildSettings WHERE guild_id=1008950152737849415
    """)
print(cursor.fetchone())