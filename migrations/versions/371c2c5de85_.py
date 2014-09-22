"""empty message

Revision ID: 371c2c5de85
Revises: 143db59ade88
Create Date: 2014-09-22 10:27:45.240465

"""

# revision identifiers, used by Alembic.
revision = '371c2c5de85'
down_revision = '143db59ade88'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.drop_constraint('roles_users_users_id_fkey', 'roles_users', type='foreignkey')
    op.rename_table('users', 'casework_users')
    op.create_foreign_key('roles_casework_users_casework_users_id_fkey', 'roles_users', 'casework_users', ['users_id'], ['id'])

def downgrade():

    op.drop_constraint('roles_casework_users_casework_users_id_fkey', 'roles_users', type='foreignkey')

    op.rename_table('casework_users', 'users')

    op.create_foreign_key('roles_users_users_id_fkey', 'roles_users', 'users', ['users_id'], ['id'])
