"""Initial migration

Revision ID: 1dc58d2c15b6
Revises: 9ef6ea2127d8
Create Date: 2025-02-01 13:38:36.519184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dc58d2c15b6'
down_revision = '9ef6ea2127d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Itineraries', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Itineraries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'Users', ['user_id'], ['id'])
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               nullable=False)

    # ### end Alembic commands ###
