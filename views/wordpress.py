from jinja2 import Template

from IndicoWp.config import Config, PATH
from IndicoWp.indico.event import IndicoEvent

import pathlib


class IndicoEventWordpressPostView:

    DATETIME_FORMAT = '%A, %d %B %Y at %M:%M'

    def __init__(self, event):
        self.event = event  # type: IndicoEvent

        # The path to the template file
        self.path = pathlib.Path(PATH) / 'templates' / 'post.html'
        self.template = None
        self.load_template()

    def load_template(self):
        with self.path.open(mode='r') as file:
            self.template = file.read()

    def get_title(self):
        title_encoded = self.event.title.encode('utf-8')
        return title_encoded

    def get_date(self):
        date_tuple = self.event.created.timetuple()
        return date_tuple

    def get_content(self):
        template = Template(self.template)
        content_string = template.render(
            location=self.event.location,
            address=self.event.address,
            description=self.event.description,
            starting=self._starting_date_string(),
            link=self._indico_link()
        )
        return content_string

    def _starting_date_string(self):
        return self.event.datetime.strftime(self.DATETIME_FORMAT)

    def _indico_link(self):
        return self.event.url
