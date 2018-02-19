from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost, DeletePost, GetPost

from IndicoWp.config import Config

from IndicoWp.views.wordpress import IndicoEventWordpressPostView

import logging


class WordpressController:

    def __init__(self):
        self.logger = logging.getLogger('Wordpress')
        self.config = Config.get_instance()

        # Getting the url path to the xmlrpc.php file from the config file
        self.url = self.config['WORDPRESS']['url']
        # Getting the username and the password for the access to the wordpress api from the config file
        self.username = self.config['WORDPRESS']['username']
        self.password = self.config['WORDPRESS']['password']

        # Creating the client object from the login data
        self.client = Client(self.url, self.username, self.password)

    def post_event(self, indico_event):
        post_view = IndicoEventWordpressPostView(indico_event)

        post = WordPressPost()

        post.title = post_view.get_title()
        post.date = post_view.get_date()
        post.content = post_view.get_content()

        post.post_status = 'publish'
        post.comment_status = 'closed'

        post_id = self.client.call(NewPost(post))

        return post_id
