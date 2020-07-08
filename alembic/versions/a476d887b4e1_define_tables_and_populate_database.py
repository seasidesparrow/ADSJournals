"""Define tables and populate database

Revision ID: a476d887b4e1
Revises: 6dd846da95c3
Create Date: 2019-10-03 13:18:28.648100

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a476d887b4e1'
down_revision = '6dd846da95c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('master',
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('bibstem', sa.String(), nullable=False),
    sa.Column('journal_name', sa.String(), nullable=False),
    sa.Column('primary_language', sa.String(), nullable=True),
    sa.Column('multilingual', sa.Boolean(), nullable=True),
    sa.Column('defunct', sa.Boolean(), nullable=False),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.Column('pubtype', postgresql.ENUM('Journal', 'Conf. Proc.', 'Monograph', 'Book', 'Software', 'Other', name='pub_type'), nullable=False),
    sa.Column('refereed', postgresql.ENUM('yes', 'no', 'partial', 'na', name='ref_status'), nullable=False),
    sa.PrimaryKeyConstraint('masterid'),
    sa.UniqueConstraint('bibstem'),
    sa.UniqueConstraint('masterid')
    )
    op.create_table('abbrevs',
    sa.Column('abbrevid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('abbreviation', sa.String(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['masterid'], ['master.masterid'], ),
    sa.PrimaryKeyConstraint('abbrevid', 'masterid'),
    sa.UniqueConstraint('abbrevid')
    )
    op.create_table('history',
    sa.Column('historyid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('year_start', sa.Integer(), nullable=True),
    sa.Column('year_end', sa.Integer(), nullable=True),
    sa.Column('predecessor_id', sa.Integer(), nullable=True),
    sa.Column('successor_id', sa.Integer(), nullable=True),
    sa.Column('orgid', sa.String(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['masterid'], ['master.masterid'], ),
    sa.PrimaryKeyConstraint('historyid', 'masterid'),
    sa.UniqueConstraint('historyid')
    )
    op.create_table('holdings',
    sa.Column('holdingsid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('volumes_list', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['masterid'], ['master.masterid'], ),
    sa.PrimaryKeyConstraint('holdingsid', 'masterid'),
    sa.UniqueConstraint('holdingsid')
    )
    op.create_table('idents',
    sa.Column('identid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('id_type', sa.String(), nullable=True),
    sa.Column('id_value', sa.String(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['masterid'], ['master.masterid'], ),
    sa.PrimaryKeyConstraint('identid', 'masterid'),
    sa.UniqueConstraint('identid')
    )
    op.create_table('names',
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('name_english_translated', sa.String(), nullable=True),
    sa.Column('title_language', sa.String(), nullable=True),
    sa.Column('name_native_language', sa.String(), nullable=True),
    sa.Column('name_normalized', sa.String(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['masterid'], ['master.masterid'], ),
    sa.PrimaryKeyConstraint('masterid')
    )
    op.create_table('publisher',
    sa.Column('publisherid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('pubname', sa.String(), nullable=True),
    sa.Column('pubaddress', sa.String(), nullable=True),
    sa.Column('pubcontact', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=True),
    sa.Column('puburl', sa.String(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['masterid'], ['master.masterid'], ),
    sa.PrimaryKeyConstraint('publisherid', 'masterid'),
    sa.UniqueConstraint('publisherid')
    )
    op.create_table('rastercontrol',
    sa.Column('historyid', sa.Integer(), nullable=False),
    sa.Column('rasterid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('copyrt_file', sa.String(), nullable=True),
    sa.Column('pubtype', sa.String(), nullable=True),
    sa.Column('bibstem', sa.String(), nullable=True),
    sa.Column('abbrev', sa.String(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('embargo', sa.Integer(), nullable=True),
    sa.Column('options', sa.String(), nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['historyid'], ['history.historyid'], ),
    sa.PrimaryKeyConstraint('historyid', 'rasterid'),
    sa.UniqueConstraint('rasterid')
    )
    op.create_table('rastervolume',
    sa.Column('rasterid', sa.Integer(), nullable=False),
    sa.Column('rvolid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('volume_number', sa.String(), nullable=False),
    sa.Column('volume_properties', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=True),
    sa.ForeignKeyConstraint(['rasterid'], ['rastercontrol.rasterid'], ),
    sa.PrimaryKeyConstraint('rasterid','rvolid'),
    sa.UniqueConstraint('rasterid')
    )
    op.create_table('statistics',
    sa.Column('historyid', sa.Integer(), nullable=False),
    sa.Column('statsid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('statistics', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['historyid'], ['history.historyid'], ),
    sa.PrimaryKeyConstraint('historyid', 'statsid'),
    sa.UniqueConstraint('statsid')
    )
    op.create_table('refsource',
    sa.Column('refsourceid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('masterid', sa.Integer(), nullable=False),
    sa.Column('refsource_list', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=True),
    sa.Column('updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['masterid'], ['master.masterid'], ),
    sa.PrimaryKeyConstraint('refsourceid', 'masterid'),
    sa.UniqueConstraint('refsourceid')
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('refsource')
    op.drop_table('statistics')
    op.drop_table('rastervolume')
    op.drop_table('rastercontrol')
    op.drop_table('publisher')
    op.drop_table('names')
    op.drop_table('idents')
    op.drop_table('holdings')
    op.drop_table('history')
    op.drop_table('abbrevs')
    op.drop_column('master','pubtype')
    pub_type = postgresql.ENUM('Journal', 'Conf. Proc.', 'Monograph', 'Book', 'Software', 'Other', name='pub_type') 
    pub_type.drop(op.get_bind())
    op.drop_column('master','refereed')
    ref_status = postgresql.ENUM('yes', 'no', 'partial', 'na', name='ref_status')
    ref_status.drop(op.get_bind())
    op.drop_table('master')
    # ### end Alembic commands ###
