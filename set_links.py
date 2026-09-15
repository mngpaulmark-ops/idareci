import sqlite3
conn = sqlite3.connect('instance/cms.db')
c = conn.cursor()
c.execute("UPDATE setting SET value='https://facebook.com/' WHERE key='facebook_url'")
c.execute("UPDATE setting SET value='https://twitter.com/' WHERE key='twitter_url'")
conn.commit()
conn.close()

import update_social_links
update_social_links.update_social_links_in_all_html()
