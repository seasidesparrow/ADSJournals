from __future__ import absolute_import, unicode_literals
from kombu import Queue
from journals import app as app_module
from journals.models import *
import journals.utils as utils
import journals.holdings as holdings


class DBCommit_Exception(Exception):
    """Non-recoverable Error with making database commits."""
    pass


class DBRead_Exception(Exception):
    """Non-recoverable Error with making database selection."""
    pass


app = app_module.ADSJournalsCelery('journals')
logger = app.logger

app.conf.CELERY_QUEUES = (
    Queue('load-datafiles', app.exchange, routing_key='load-datafiles'),
    Queue('load-holdings', app.exchange, routing_key='load-holdings')
)


@app.task(queue='load-datafiles')
def task_db_bibstems_to_master(recs):
    pubtypes = {'C': 'Conf. Proc.', 'J': 'Journal', 'R': 'Journal'}
    reftypes = {'C': 'na', 'J': 'no', 'R': 'yes'}
    with app.session_scope() as session:
        if len(recs) > 0:
            for r in recs:
                if r[1] in pubtypes:
                    ptype = pubtypes[r[1]]
                else:
                    ptype = 'Other'
                if r[1] in reftypes:
                    rtype = reftypes[r[1]]
                else:
                    rtype = 'na'
                session.add(JournalsMaster(bibstem=r[0], journal_name=r[2], pubtype=ptype, refereed=rtype, defunct=False))
            try:
                session.commit()
            except Exception, err:
                logger.error("Problem with database commit: %s" % err)
                raise DBCommit_Exception("Could not commit to db, stopping now.")


@app.task(queue='load-datafiles')
def task_db_load_abbrevs(recs):
    with app.session_scope() as session:
        if len(recs) > 0:
            for r in recs:
                try:
                    session.add(Abbreviations(masterid=r[0], abbreviation=r[1]))
                    session.commit()
                except Exception, err:
                    logger.warn("Problem with abbreviation: %s,%s" % (r[0], r[1]))
        else:
            logger.info("There were no abbreviations to load!")


@app.task(queue='load-datafiles')
def task_db_load_issn(recs):
    with app.session_scope() as session:
        if len(recs) > 0:
            for r in recs:
                try:
                    session.add(Identifiers(masterid=r[0], id_type='ISSN', id_value=r[1]))
                    session.commit()
                except Exception as e:
                    logger.warn("Duplicate ISSN ident skipped: %s,%s" % (r[0], r[1]))
                    session.rollback()
                    session.flush()
        else:
            logger.info("There were no ISSNs to load!")


@app.task(queue='load-datafiles')
def task_db_load_xref(recs):
    with app.session_scope() as session:
        if len(recs) > 0:
            for r in recs:
                try:
                    session.add(Identifiers(masterid=r[0], id_type='CROSSREF', id_value=r[1]))
                    session.commit()
                except Exception as e:
                    logger.warn("Duplicate XREF ident skipped: %s,%s" % (r[0], r[1]))
                    session.rollback()
                    session.flush()
        else:
            logger.info("There were no XREF IDs to load!")


@app.task(queue='load-datafiles')
def task_db_get_bibstem_masterid():
    dictionary = {}
    with app.session_scope() as session:
        try:
            for record in session.query(JournalsMaster.masterid, JournalsMaster.bibstem):
                dictionary[record.bibstem] = record.masterid
        except Exception, err:
            logger.error("Error: failed to read bibstem-masterid dict from table master")
            raise DBRead_Exception("Could not read from database!")
    return dictionary


@app.task(queue='load-holdings')
def task_db_load_holdings(recs, infile):
    with app.session_scope() as session:
        if len(recs) > 0:
            hold = holdings.Holdings()
            output = hold.load_json(infile)
            h_out = hold.process_output(output)
            for bibstem, masterid in recs.items():
                bibstem = str(bibstem)
                try:
                    h_data = h_out[bibstem]
                    for d in h_data:
                        try:
                            session.add(Holdings(masterid=masterid, volumes_list=d))
                            session.commit()
                        except Exception, err:
                            logger.warn("Error adding holdings for {0}".format(bibstem))
                            session.rollback()
                            session.commit()
                except Exception, err:
                    logger.warn("Bibstem does not exist: {0}".format(bibstem))
        else:
            logger.error("No holdings data to load!")
    return
