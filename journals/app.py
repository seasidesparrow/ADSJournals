"""
The main application object (it has to be loaded by any worker/script)
in order to initialize the database and get a working configuration.
"""

from __future__ import absolute_import, unicode_literals
from sqlalchemy.orm import load_only as _load_only
from adsputils import ADSCelery, get_date, setup_logging, load_config, u2asc

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

class ADSJournalsCelery(ADSCelery):

    pass

#   def __init__(self):
#       Session = sessionmaker()
#       self.session = Session()
