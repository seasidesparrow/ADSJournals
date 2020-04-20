# COLLECTIONS is a list of which collections/databases are stored
COLLECTIONS = ['ast', 'phy', 'gen']

# DATA_DIRECTORY:
JDB_DATA_DIR = '/proj/ads/abstracts/config/journalsdb/PIPELINE/data/'

# BIBSTEMS has bibstem, R/J/C/etc, and canonical name
BIBSTEMS_FILE = 'bibstems.dat'

# JOURNAL_ABBREV has bibstem and multiple title abbreviations (e.g. A&A, AA, Astron. & Astrophys.)
JOURNAL_ABBREV_FILE = 'journals_abbrev.dat'

JOURNAL_ISSN_FILE = 'journal_issn'
ISSN_JOURNAL_FILE = 'issn2journal'
CANONICAL_BIB_FILE = 'bib2accno.dat'

# ESOURCES: for holdings table
# Any new esources must be **prepended** to this list
ESOURCE_LIST = ['PUB_HTML', 'PUB_PDF', 'EPRINT_HTML', 'EPRINT_PDF', 'ADS_SCAN', 'ADS_PDF']
