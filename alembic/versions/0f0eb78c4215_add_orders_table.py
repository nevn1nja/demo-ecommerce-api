from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

from src.db.models.database_models import OrderStatus

# revision identifiers, used by Alembic.
revision: str = '0f0eb78c4215'
down_revision: Union[str, None] = '525bfe78fb8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

order_status_enum = sa.Enum(OrderStatus, name='orderstatus')

def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('total_price', sa.Float, nullable=False),
        sa.Column('status', order_status_enum, nullable=False, default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )

    op.create_table(
        'order_items',
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now())
    )

    op.create_index('ix_orders_status', 'orders', ['status'])
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'])
    op.create_index('ix_order_items_product_id', 'order_items', ['product_id'])
    op.create_index('ix_order_items_order_product', 'order_items', ['order_id', 'product_id'])

def downgrade() -> None:
    op.drop_index('ix_order_items_order_product', table_name='order_items')
    op.drop_index('ix_order_items_product_id', table_name='order_items')
    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_index('ix_orders_status', table_name='orders')

    op.drop_table('order_items')
    op.drop_table('orders')

    order_status_enum.drop(op.get_bind(), checkfirst=False)
