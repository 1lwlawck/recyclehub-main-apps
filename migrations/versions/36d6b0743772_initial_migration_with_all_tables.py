"""Initial migration with all tables

Revision ID: 36d6b0743772
Revises: 
Create Date: 2024-12-11 00:12:39.936748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36d6b0743772'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nama_user', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('otp', sa.Integer(), nullable=True),
    sa.Column('otp_expiry', sa.DateTime(), nullable=True),
    sa.Column('reset_token', sa.String(length=255), nullable=True),
    sa.Column('reset_token_expiry', sa.DateTime(), nullable=True),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
