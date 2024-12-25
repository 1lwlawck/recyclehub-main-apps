"""Add order, detail sampah, and jenis sampah models

Revision ID: f2d57b5bbd42
Revises: c57adf4a2b4f
Create Date: 2024-12-24 23:58:44.472813

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f2d57b5bbd42'
down_revision = 'c57adf4a2b4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jenis_sampah',
    sa.Column('id_jenis_sampah', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nama_jenis_sampah', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id_jenis_sampah')
    )
    op.create_table('orders',
    sa.Column('id_order', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('tanggal_pengantaran', sa.Date(), nullable=False),
    sa.Column('waktu_pengantaran', sa.Time(), nullable=False),
    sa.Column('informasi_tambahan', sa.Text(), nullable=True),
    sa.Column('status_order', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_order')
    )
    op.create_table('detail_sampah',
    sa.Column('id_detail', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_order', sa.Integer(), nullable=False),
    sa.Column('id_jenis_sampah', sa.Integer(), nullable=False),
    sa.Column('perkiraan_berat', sa.Float(), nullable=False),
    sa.Column('foto_sampah', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['id_jenis_sampah'], ['jenis_sampah.id_jenis_sampah'], ),
    sa.ForeignKeyConstraint(['id_order'], ['orders.id_order'], ),
    sa.PrimaryKeyConstraint('id_detail')
    )
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=mysql.LONGTEXT(),
               type_=sa.Text(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.Text(),
               type_=mysql.LONGTEXT(),
               nullable=True)

    op.drop_table('detail_sampah')
    op.drop_table('orders')
    op.drop_table('jenis_sampah')
    # ### end Alembic commands ###
