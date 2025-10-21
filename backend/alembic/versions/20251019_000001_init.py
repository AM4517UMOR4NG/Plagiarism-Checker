"""init tables

Revision ID: 20251019_000001
Revises: 
Create Date: 2025-10-19 05:10:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251019_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'documents',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('title', sa.String(length=512), nullable=True),
        sa.Column('storage_path', sa.String(length=1024), nullable=False),
        sa.Column('language', sa.String(length=32), nullable=True),
        sa.Column('num_words', sa.Integer(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('is_reference', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    )

    op.create_table(
        'jobs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('document_id', sa.String(length=36), sa.ForeignKey('documents.id'), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='pending'),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('result_path', sa.String(length=1024), nullable=True),
    )

    op.create_table(
        'sources',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('title', sa.String(length=512), nullable=True),
        sa.Column('storage_path', sa.String(length=1024), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
    )

    op.create_table(
        'fragments',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('job_id', sa.String(length=64), sa.ForeignKey('jobs.id'), nullable=False),
        sa.Column('doc_pos', sa.Integer(), nullable=False),
        sa.Column('length_tokens', sa.Integer(), nullable=False),
        sa.Column('matched_source_id', sa.String(length=36), sa.ForeignKey('sources.id'), nullable=True),
        sa.Column('match_type', sa.String(length=32), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('source_excerpt', sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('fragments')
    op.drop_table('sources')
    op.drop_table('jobs')
    op.drop_table('documents')
    op.drop_table('users')
