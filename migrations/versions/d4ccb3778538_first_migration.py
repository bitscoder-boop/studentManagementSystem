"""first migration

Revision ID: d4ccb3778538
Revises: 
Create Date: 2021-07-14 13:20:55.367501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4ccb3778538'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=24), nullable=True),
    sa.Column('last_name', sa.String(length=24), nullable=True),
    sa.Column('username', sa.String(length=24), nullable=True),
    sa.Column('address', sa.Text(length=100), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_admin')),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('username', name=op.f('uq_admin_username'))
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_first_name'), ['first_name'], unique=False)

    op.create_table('grade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grade_number', sa.String(length=12), nullable=False),
    sa.Column('total_subject', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_grade')),
    sa.UniqueConstraint('grade_number'),
    sa.UniqueConstraint('grade_number', name=op.f('uq_grade_grade_number'))
    )
    op.create_table('staff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=24), nullable=True),
    sa.Column('middle_name', sa.String(length=24), nullable=True),
    sa.Column('last_name', sa.String(length=24), nullable=True),
    sa.Column('username', sa.String(length=24), nullable=True),
    sa.Column('gender', sa.String(length=12), nullable=True),
    sa.Column('address', sa.Text(length=100), nullable=True),
    sa.Column('email', sa.String(length=24), nullable=True),
    sa.Column('contact', sa.Integer(), nullable=True),
    sa.Column('seson_start_year', sa.DateTime(), nullable=True),
    sa.Column('grade_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], name=op.f('fk_staff_grade_id_grade')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_staff')),
    sa.UniqueConstraint('contact'),
    sa.UniqueConstraint('contact', name=op.f('uq_staff_contact')),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email', name=op.f('uq_staff_email')),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('username', name=op.f('uq_staff_username'))
    )
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_staff_first_name'), ['first_name'], unique=False)

    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=24), nullable=True),
    sa.Column('middle_name', sa.String(length=24), nullable=True),
    sa.Column('last_name', sa.String(length=24), nullable=True),
    sa.Column('username', sa.String(length=24), nullable=True),
    sa.Column('gender', sa.String(length=12), nullable=True),
    sa.Column('address', sa.Text(length=100), nullable=True),
    sa.Column('email', sa.String(length=24), nullable=True),
    sa.Column('contact', sa.Integer(), nullable=True),
    sa.Column('seson_start_year', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], name=op.f('fk_student_grade_id_grade')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_student')),
    sa.UniqueConstraint('contact'),
    sa.UniqueConstraint('contact', name=op.f('uq_student_contact')),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('username', name=op.f('uq_student_username'))
    )
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_student_first_name'), ['first_name'], unique=False)

    op.create_table('subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=36), nullable=True),
    sa.Column('market_value', sa.Integer(), nullable=True),
    sa.Column('publisher_name', sa.String(length=36), nullable=True),
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], name=op.f('fk_subject_grade_id_grade')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_subject'))
    )
    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_subject_name'), ['name'], unique=False)

    op.create_table('subject_teacher',
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], name=op.f('fk_subject_teacher_staff_id_staff')),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], name=op.f('fk_subject_teacher_subject_id_subject'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subject_teacher')
    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_subject_name'))

    op.drop_table('subject')
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_student_first_name'))

    op.drop_table('student')
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_staff_first_name'))

    op.drop_table('staff')
    op.drop_table('grade')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_first_name'))

    op.drop_table('admin')
    # ### end Alembic commands ###