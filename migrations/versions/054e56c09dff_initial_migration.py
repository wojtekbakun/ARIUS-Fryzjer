"""Initial migration

Revision ID: 054e56c09dff
Revises: edcbc4c6e760
Create Date: 2025-01-11 14:42:37.285820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '054e56c09dff'
down_revision = 'edcbc4c6e760'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('street', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('street_number', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('postal_code', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('nip', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('company_name', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('company_name')
        batch_op.drop_column('nip')
        batch_op.drop_column('city')
        batch_op.drop_column('postal_code')
        batch_op.drop_column('street_number')
        batch_op.drop_column('street')

    op.drop_table('employee')
    # ### end Alembic commands ###