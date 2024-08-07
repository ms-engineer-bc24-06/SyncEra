"""added contact_form, summarize_history, advices_history tables

Revision ID: 290d33765dc4
Revises: be32a12d8404
Create Date: 2024-08-05 06:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '290d33765dc4'
down_revision = 'be32a12d8404'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_form',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('summarize_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('employee_id', UUID(as_uuid=True), sa.ForeignKey('employee.id'), nullable=False),
    sa.Column('summary', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('advices_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('employee_id', UUID(as_uuid=True), sa.ForeignKey('employee.id'), nullable=False),
    sa.Column('advices', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('advices_history')
    op.drop_table('summarize_history')
    op.drop_table('contact_form')
    # ### end Alembic commands ###
