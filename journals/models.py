from adsputils import get_date, UTCDateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table, Column, Integer, Numeric, String, TIMESTAMP,
                        ForeignKey, Boolean, Float, UniqueConstraint)
from sqlalchemy.dialects.postgresql import JSONB, ENUM

Base = declarative_base()


class JournalsMaster(Base):
    __tablename__ = 'master'

    pub_type = ENUM('Journal', 'Conf. Proc.', 'Monograph', 'Book',
                    'Software', 'Other', name='pub_type')
    ref_status = ENUM('yes', 'no', 'partial', 'na', name='ref_status')

    masterid = Column(Integer, primary_key=True, unique=True)
    bibstem = Column(String, unique=True, nullable=False)
    journal_name = Column(String, nullable=False)
    primary_language = Column(String)
    multilingual = Column(Boolean)
    defunct = Column(Boolean, nullable=False, default=False)
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    pubtype = Column(pub_type, nullable=False)
    refereed = Column(ref_status, nullable=False)

    def __repr__(self):
        return "master.masterid='{self.masterid}')".format(self=self)


class JournalsNames(Base):
    __tablename__ = 'names'

    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    name_english_translated = Column(String)
    title_language = Column(String)
    name_native_language = Column(String)
    name_normalized = Column(String)
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "JournalsNames(masterid='{self.masterid}')".format(self=self)


class Identifiers(Base):
    __tablename__ = 'idents'

    identid = Column(Integer, primary_key=True, autoincrement=True,
                     unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    id_type = Column(String)
    id_value = Column(String)
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)
    id_combo = UniqueConstraint('id_type', 'id_value', name='identkey')

    def __repr__(self):
        return "Identifiers(identid='{self.identid}')".format(self=self)


class Abbreviations(Base):
    __tablename__ = 'abbrevs'

    abbrevid = Column(Integer, primary_key=True, autoincrement=True,
                      unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    abbreviation = Column(String)
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "Abbreviations(abbrevid='{self.abbrevid}')".format(self=self)


class History(Base):
    __tablename__ = 'history'

    historyid = Column(Integer, primary_key=True, autoincrement=True,
                       unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    year_start = Column(Integer)
    year_end = Column(Integer)
    predecessor_id = Column(Integer)
    successor_id = Column(Integer)
    orgid = Column(String)
    notes = Column(String)
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "History(historyid='{self.historyid}')".format(self=self)


class Holdings(Base):
    __tablename__ = 'holdings'

    holdingsid = Column(Integer, primary_key=True, autoincrement=True,
                        unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    volumes_list = Column(JSONB, server_default="'{}'")
    complete = Column(Boolean, default=False)
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "Holdings(holdingsid='{self.holdingsid}')".format(self=self)


class Publisher(Base):
    __tablename__ = 'publisher'

    publisherid = Column(Integer, primary_key=True, autoincrement=True,
                         unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    pubname = Column(String)
    pubaddress = Column(String)
    pubcontact = Column(JSONB, server_default="'{}'")
    puburl = Column(String)
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "Publisher(publisherid='{self.publisherid}')".format(self=self)


class Statistics(Base):
    __tablename__ = 'statistics'

# placeholder for the concept of a stats table for journal-level tracking
# information separate from our Holdings table (e.g. journal reads, ADS pdf
# reads, etc)

    historyid = Column(Integer, ForeignKey('history.historyid'),
                       primary_key=True, nullable=False)
    statsid = Column(Integer, primary_key=True, autoincrement=True,
                     unique=True, nullable=False)
    statistics = Column(JSONB, server_default="'{}'")
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr(self):
        return "Statistics(statsid='{self.statsid}')".format(self=self)


class RasterControl(Base):
    __tablename__ = 'rastercontrol'

# placeholder for the concept of a table with information controlling
# rasterizing information (e.g. the information in .../articles/config/ABC.xml)

    historyid = Column(Integer, ForeignKey('history.historyid'),
                       primary_key=True, nullable=False)
    rasterid = Column(Integer, primary_key=True, autoincrement=True,
                      unique=True, nullable=False)
    embargo_months = Column(Integer)
    volume_properties = Column(JSONB, server_default="'{}'")
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr(self):
        return "RasterControl(rasterid='{self.rasterid}')".format(self=self)


class RefSource(Base):
    __tablename__ = 'refsource'

    refsourceid = Column(Integer, primary_key=True, autoincrement=True,
                        unique=True, nullable=False)
    masterid = Column(Integer, ForeignKey('master.masterid'),
                      primary_key=True, nullable=False)
    refsource_list = Column(JSONB, server_default="'{}'")
    updated = Column(UTCDateTime, onupdate=get_date)
    created = Column(UTCDateTime, default=get_date)

    def __repr__(self):
        return "RefSource(refsourceid='{self.refsourceid}')".format(self=self)
