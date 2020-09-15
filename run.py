import argparse
import config
from journals import tasks
from journals import utils
from adsputils import setup_logging

logger = setup_logging('run.py')


def get_arguments():

    parser = argparse.ArgumentParser(description='Command line options.')

    parser.add_argument('-lm',
                        '--load-master',
                        dest='load_master',
                        action='store_true',
                        help='Load master list of bibstems')

    parser.add_argument('-la',
                        '--load-abbrevs',
                        dest='load_abbrevs',
                        action='store_true',
                        help='Load list of journal name abbreviations')

    parser.add_argument('-ch',
                        '--calculate-holdings',
                        dest='calc_holdings',
                        action='store',
                        help='Populate holdings from Solr data')

    parser.add_argument('-ca',
                        '--load-complete-ast',
                        dest='load_ca',
                        action='store_true',
                        help='Load spreadsheet complete_ast')

    parser.add_argument('-lr',
                        '--load-rasterconf',
                        dest='load_raster',
                        action='store_true',
                        help='Load rasterization control parameters')

    args = parser.parse_args()
    return args


def load_master_table():
    bibstems = utils.read_bibstems_list()
    recs = []
    for k, v in bibstems.items():
        bibstem = k
        pubtype = v['type']
        journal_name = v['pubname']
        recs.append((bibstem, pubtype, journal_name))
    if len(recs) > 0:
        logger.debug("Inserting {0} bibstems into Master".format(len(recs)))
        tasks.task_db_bibstems_to_master(recs)
    else:
        logger.warn("No bibstems to insert")
    return


def load_rasterconfig(masterdict):
    recsr = []
    recsrv = []
    for k, v in masterdict.items():
        raster_rec = utils.read_raster_xml(k)
        if raster_rec:
            print("LOL! %s",raster_rec)
    return
           

def load_abbreviations(masterdict):
    abbrevs = utils.read_abbreviations_list()
    recs = []
    for k, v in abbrevs.items():
        try:
            if k in masterdict:
                logger.debug("Got mid for bibstem {0}".format(k))
                mid = masterdict[k]
                for a in v:
                    recs.append((mid, a))
            else:
                logger.debug("No mid for bibstem {0}".format(k))
        except Exception, err:
            logger.warn("Error with bibstem {0}".format(k))
            logger.warn("Error: {0}".format(err))
    if len(recs) > 0:
        logger.debug("Inserting {0} abbreviations into Abbreviations".format(len(recs)))
        try:
            tasks.task_db_load_abbrevs(recs)
        except Exception, err:
            logger.error("Could not load abbreviations: {0}".format(err))
    else:
        logger.warn("There are no abbreviations to load.")
    return


def load_completeness(masterdict):
    pub_dict = utils.read_complete_csvs()
    recsi = []
    recsx = []
    recsp = []
    for k, v in pub_dict.items():
        try:
            if k in masterdict:
                logger.debug("Got mid for bibstem {0}".format(k))
                mid = masterdict[k]
                a = v['issn']
                b = v['xref']
                c = v['startyear']
                d = v['startvol']
                e = v['endvol']
                f = v['complete']
                g = v['complete_origin']
                h = v['publisher']
                i = v['scanned']
                j = v['online']
                k = v['url']
                if a != '':
                    recsi.append((mid, a))
                if b != '':
                    recsx.append((mid, b))
                if h != '':
                    recsp.append((mid, h, k))
             
            else:
                logger.debug("No mid for bibstem {0}".format(k))
        except Exception, err:
            logger.warn("Error with bibstem {0}".format(k))
            logger.warn("Error: {0}".format(err))
    if recsi:
        tasks.task_db_load_issn(recsi)
    if recsx:
        tasks.task_db_load_xref(recsx)
    if recsp:
        tasks.task_db_load_publisher(recsp)
    return


def calc_holdings(masterdict, json_file):
    try:
        tasks.task_db_load_holdings(masterdict, json_file)
    except Exception, err:
        logger.error("Failed to load holdings: {0}".format(err))
    return


def main():

    args = get_arguments()

    # if args.load_master == True:
    # create the set of bibcode-journal name pairs and assign them UIDs;
    # these UIDs will be used as foreign keys in all other tables, so
    # if this fails, you're dead in the water.
    if args.load_master:
        load_master_table()

    # none of the other loaders will work unless you have data in
    # journals.master, so try to load it
    try:
        masterdict = tasks.task_db_get_bibstem_masterid()
        logger.info("masterdict has {0} records".format(len(masterdict)))
    except Exception, err:
        logger.error("Error reading master table bibstem-masterid mapping: {0}".format(err))
    else:
        # load bibstem-journal name abbreviation pairs
        if args.load_abbrevs:
            load_abbreviations(masterdict)

        if args.load_ca:
            # astro journal data
            load_completeness(masterdict)

        if args.calc_holdings:
            # holdings: be aware this is a big Solr query
            calc_holdings(masterdict, args.calc_holdings)


if __name__ == '__main__':
    main()
