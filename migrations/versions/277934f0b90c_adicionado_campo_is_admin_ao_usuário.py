"""Adicionado campo is_admin ao usuário

Revision ID: 277934f0b90c
Revises: 
Create Date: 2025-02-06 10:16:32.627517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '277934f0b90c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
