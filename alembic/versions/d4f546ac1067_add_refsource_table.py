"""Add refsource table

Revision ID: d4f546ac1067
Revises: a476d887b4e1
Create Date: 2020-04-21 13:21:13.639047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4f546ac1067'
down_revision = 'a476d887b4e1'
branch_labels = None
depends_on = None


def upgrade():
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


def downgrade():
    op.drop_table('refsource')
