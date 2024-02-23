"""add image column to Post model

Revision ID: 58228adebd6d
Revises: 7a0985aef442
Create Date: 2024-02-23 04:42:35.492779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58228adebd6d'
down_revision = '7a0985aef442'
branch_labels = None
depends_on = None



def upgrade():
    # Add column with nullable=True
    op.add_column('post', sa.Column('image_url', sa.String(255), nullable=True))

def downgrade():
    # Remove column
    op.drop_column('post', 'image_url')

    # ### end Alembic commands ###
