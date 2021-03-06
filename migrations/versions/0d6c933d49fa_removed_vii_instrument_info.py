"""removed vii instrument info

Revision ID: 0d6c933d49fa
Revises: 3479d47f8e20
Create Date: 2021-09-07 09:16:13.513337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d6c933d49fa'
down_revision = '3479d47f8e20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('run', 'vii6_id')
    op.drop_column('run', 'vii12_cdd')
    op.drop_column('run', 'vii7_id')
    op.drop_column('run', 'vii10_id')
    op.drop_column('run', 'vii6_cdd')
    op.drop_column('run', 'vii7_cdd')
    op.drop_column('run', 'vii10_cdd')
    op.drop_column('run', 'vii1_id')
    op.drop_column('run', 'vii11_id')
    op.drop_column('run', 'vii9_id')
    op.drop_column('run', 'vii9_cdd')
    op.drop_column('run', 'vii3_id')
    op.drop_column('run', 'vii5_cdd')
    op.drop_column('run', 'vii5_id')
    op.drop_column('run', 'vii4_cdd')
    op.drop_column('run', 'vii4_id')
    op.drop_column('run', 'vii8_cdd')
    op.drop_column('run', 'vii2_id')
    op.drop_column('run', 'vii8_id')
    op.drop_column('run', 'vii11_cdd')
    op.drop_column('run', 'vii12_id')
    op.drop_column('run', 'vii3_cdd')
    op.drop_column('run', 'vii1_cdd')
    op.drop_column('run', 'vii2_cdd')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('run', sa.Column('vii2_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii1_cdd', sa.VARCHAR(length=7), nullable=False))
    op.add_column('run', sa.Column('vii3_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii12_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii11_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii8_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii2_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii8_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii4_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii4_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii5_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii5_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii3_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii9_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii9_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii11_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii1_id', sa.VARCHAR(length=8), nullable=False))
    op.add_column('run', sa.Column('vii10_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii7_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii6_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii10_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii7_id', sa.VARCHAR(length=8), nullable=True))
    op.add_column('run', sa.Column('vii12_cdd', sa.VARCHAR(length=7), nullable=True))
    op.add_column('run', sa.Column('vii6_id', sa.VARCHAR(length=8), nullable=True))
    # ### end Alembic commands ###
