from __future__ import absolute_import, unicode_literals
from kombu import Queue

from journals import app as app_module
from journals.models import *
import journals.utils as utils
import json

import journals.holdings as holdings

class DBCommit_Exception(Exception):
    """Non-recoverable Error with making database commits."""
    pass

app = app_module.ADSJournalsCelery('journals')
logger = app.logger

app.conf.CELERY_QUEUES = (
    Queue('load-master',app.exchange,routing_key='load-master'),
    Queue('load-abbrev',app.exchange,routing_key='load-abbrev'),
    Queue('load-issn',app.exchange,routing_key='load-issn'),
    Queue('load-xref',app.exchange,routing_key='load-xref'),
    Queue('load-holdings',app.exchange,routing_key='load-holdings'),
    Queue('get-masterid',app.exchange,routing_key='get-masterid')
)
logger = app.logger

session = app.session_scope()

@app.task(queue='load-master')
def task_db_bibstems_to_master(recs):
    pubtypes = {'C':'Conf. Proc.', 'J':'Journal', 'R':'Journal'}
    reftypes = {'C':'na','J':'no','R':'yes'}
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
            
            session.add(JournalsMaster(bibstem=r[0],journal_name=r[2],pubtype=ptype,refereed=rtype,defunct=False))
        try:
            session.commit()
        except Exception, err:
            logger.error("Problem with database commit: %s" % err)
            raise DBCommit_Exception("Could not commit to db, stopping now.")


@app.task(queue='load-abbrev')
def task_db_load_abbrevs(recs):
    if len(recs) > 0:
        for r in recs:
            try:
                session.add(Abbreviations(masterid=r[0],abbreviation=r[1]))
                session.commit()
            except:
                print ("Problem with abbreviation: %s,%s"%(r[0],r[1]))
                logger.warn("Problem with abbreviation: %s,%s"%(r[0],r[1]))


@app.task(queue='load-issn')
def task_db_load_issn(recs):
    if len(recs) > 0:
        for r in recs:
            try:
                session.add(Identifiers(masterid=r[0],id_type='ISSN',id_value=r[1]))
                session.commit()
            except Exception as e:
                print ("Skipping Master ID/ISSN %s,%s"%(r[0],r[1]))
                logger.warn("Duplicate ISSN ident skipped: %s,%s"%(r[0],r[1]))
                session.rollback()
                session.flush()


@app.task(queue='load-xref')
def task_db_load_xref(recs):
    if len(recs) > 0:
        for r in recs:
            try:
                session.add(Identifiers(masterid=r[0],id_type='CROSSREF',id_value=r[1]))
                session.commit()
            except Exception as e:
                print ("Skipping Master ID/XREF %s,%s"%(r[0],r[1]))
                logger.warn("Duplicate XREF ident skipped: %s,%s"%(r[0],r[1]))
                session.rollback()
                session.flush()

#@app.task(queue='load-csv')
#def task_db_load_ids(recs):


@app.task(queue='get-masterid')
def task_db_get_bibstem_masterid():
    dictionary = {}
    try:
        for record in session.query(JournalsMaster.masterid,JournalsMaster.bibstem):
            dictionary[record.bibstem] = record.masterid
    except:
        logger.error("Error: failed to read bibstem-masterid dict from table master")
    return dictionary


@app.task(queue='load-holdings')
def task_db_load_holdings(recs, infile):
    print "IN TASK task_db_load_holdings"
    if len(recs) > 0:
        hold = holdings.Holdings()
#       for r in recs:
#           [[bibstem, masterid]] = r.items()
        output = hold.load_json(infile)
        h_out = hold.process_output(output)
        for bibstem, masterid in recs.items():
            bibstem = str(bibstem)
            print("Working on bibstem:", bibstem, masterid)
            try:
                h_data = h_out[bibstem]
                for d in h_data:
                    try:
                        session.add(Holdings(masterid=masterid, volumes_list=d))
                        session.commit()
                    except Exception, err:
                        print("Skipping Master ID %s" % masterid)
                        print(err)
                        session.rollback()
                        session.commit()
            except Exception, err:
                print "Bibstem not found:",bibstem
                print "Error:",err
    else:
        print("You got bupkus.")
    return
