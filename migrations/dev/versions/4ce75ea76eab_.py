"""empty message

Revision ID: 4ce75ea76eab
Revises: 
Create Date: 2020-09-12 06:26:02.904768

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '4ce75ea76eab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contest', sa.Column('name', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'contest', ['uuid'])
    op.create_unique_constraint(None, 'contest_status', ['name'])
    op.create_unique_constraint(None, 'participant', ['uuid'])
    op.create_unique_constraint(None, 'participant_status', ['name'])
    op.create_unique_constraint(None, 'sport', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sport', type_='unique')
    op.drop_constraint(None, 'participant_status', type_='unique')
    op.drop_constraint(None, 'participant', type_='unique')
    op.drop_constraint(None, 'contest_status', type_='unique')
    op.drop_constraint(None, 'contest', type_='unique')
    op.drop_column('contest', 'name')
    # ### end Alembic commands ###
