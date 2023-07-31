import sqlite3
import settings

connection_obj = sqlite3.connect(settings.guilds_directory)
cursor_obj = connection_obj.cursor()
table = """ CREATE TABLE guilds (
			"guild_id"	INTEGER UNIQUE,
			"archive_channel_id"	INTEGER UNIQUE
		); """
cursor_obj.execute("DROP TABLE IF EXISTS guilds")
# cursor_obj.execute(table)
# # cursor_obj.execute("""CREATE UNIQUE INDEX "sqlite_autoindex_guilds_2" ON (archive_channel_id)""")
# # cursor_obj.execute("""CREATE UNIQUE INDEX "sqlite_autoindex_guilds_1" ON (guild_id)""")
cursor_obj.close()
connection_obj.close()