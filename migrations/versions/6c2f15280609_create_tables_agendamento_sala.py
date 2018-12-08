"""Create-Tables-Agendamento-Sala

Revision ID: 6c2f15280609
Revises: 
Create Date: 2018-12-08 00:16:32.374418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c2f15280609'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Sala',
    sa.Column('id_sala', sa.Integer(), nullable=False),
    sa.Column('sala_nome', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id_sala'),
    sa.UniqueConstraint('sala_nome')
    )
    op.create_table('Agendamento',
    sa.Column('id_agendamento', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=45), nullable=True),
    sa.Column('horario_inicio', sa.DateTime(), nullable=True),
    sa.Column('horario_fim', sa.DateTime(), nullable=True),
    sa.Column('id_sala', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_sala'], ['Sala.id_sala'], ),
    sa.PrimaryKeyConstraint('id_agendamento'),
    sa.UniqueConstraint('titulo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Agendamento')
    op.drop_table('Sala')
    # ### end Alembic commands ###
