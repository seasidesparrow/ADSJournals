import config
from namedentities import named_entities, unicode_entities


def normalize(instring):
    # input from whatever, output to unicode
    try:
        work_string = instring.decode('utf-8')
    except:
        try:
            work_string = instring.decode('iso-8859-1')
        except:
            try:
                work_string = instring.decode('cp1252-1')
            except:
                return unicode_entities(instring)
    return unicode_entities(work_string)


def read_bibstems_list():
    data = {}
    infile = config.JDB_DATA_DIR + config.BIBSTEMS_FILE
    try:
        with open(infile,'rU') as f:
            nbibstem = f.readline()
            for l in f.readlines():
                 (bibstem,bstype,bspubname) = l.rstrip().split('\t')
                 bibstem = bibstem.rstrip('.').lstrip('.')
                 if bibstem in data:
                     print ("Duplicate in bibstems list!",bibstem)
                 data[bibstem] = {'type':bstype,'pubname':bspubname}
    except Exception, err:
        print (err)
    return data


def read_abbreviations_list():
    datadict = {}
    infile = config.JDB_DATA_DIR + config.JOURNAL_ABBREV_FILE
    with open(infile,'rU') as f:
        for l in f.readlines():
            (bibstem_abbrev,abbrev) = l.rstrip().split('\t')
            bibstem_abbrev = bibstem_abbrev.rstrip('.').lstrip('.')
            abbrev = normalize(abbrev)
            abbrev = abbrev.lstrip().rstrip()
            if bibstem_abbrev in datadict:
                if abbrev not in datadict[bibstem_abbrev]:
                    datadict[bibstem_abbrev].append(abbrev)
                else:
                    print("Duplicate abbreviation: %s"%abbrev)
            else:
                datadict[bibstem_abbrev] = [abbrev]
    return datadict


def read_canonical_list():
    bibc = []
    infile = config.JDB_DATA_DIR + config.CANONICAL_BIB_FILE
    try:
        with open(infile, 'rU') as f:
            for l in f.readlines():
                (bibcode,a,b,c) = l.rstrip().split('\t')
                bibc.append(bibcode)
    except Exception, err:
        print(err)
    return bibc


def read_complete_csvs():
    data = {}
    collections = ['ast']
    for coll in collections:
        infile = config.JDB_DATA_DIR + 'completion.'+coll+'.csv'
        with open(infile,'rU') as f:
            f.readline()
            f.readline()
            for l in f.readlines():
                try:
                    (journal,bibstem,issn,xref,startyear,startvol,endvol,complete,complete_origin,publisher,scanned,online,url,notes) = l.strip().split('|')
                except Exception, err:
                    print err,l.strip()
                else:
                    if bibstem in data:
                        print "skipping duplicate bibstem: %s"%bibstem
                    else:
                        for a in [complete,scanned,online]:
                            if (a != '' and (a[0] == 'Y' or a[0] == 'y')):
                                a = True
                            else:
                                a = False
                        data[bibstem] = {u'issn': issn, u'xref': xref, u'startyear': startyear, u'startvol': startvol, u'endvol': endvol, u'complete': complete, u'comporig': complete_origin, u'publisher': publisher, u'scanned': scanned, u'online': online, u'url': url, u'notes': notes}
    return data
            


def parse_bibcodes(bibcode):
    parsed_bib = {}
    if not isinstance(bibcode,str):
        print ("parse_bibcodes: this is not a string")
    else:
        try:
            year = bibcode[0:4]
            stem = bibcode[4:9]
            volm = bibcode[9:13]
            qual = bibcode[13]
            page = bibcode[14:18]
            auth = bibcode[18]
            parsed_bib = {"bibcode": bibcode, "year": year, "bibstem": stem, "volume": volm,
                          "qualifier": qual, "page": page, "initial": auth}
        except Exception, err:
            print ("parse_bibcodes: this is not a standard bibcode")
    return parsed_bib
