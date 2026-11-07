from datetime import datetime
from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Order, OrderItem, Customer, Product
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse, OrderItemResponse

router = APIRouter(prefix="/api/orders", tags=["Orders"])


def require_auth(request: Request):
    if not request.session.get("admin_id"):
        return False
    return True


STATUS_FA_TO_EN = {
    "pending": "pending",
    "در انتظار": "pending",
    "completed": "completed",
    "تکمیل شده": "completed",
    "cancelled": "cancelled",
    "لغو شده": "cancelled",
}

STATUS_EN_TO_FA = {
    "pending": "در انتظار",
    "completed": "تکمیل شده",
    "cancelled": "لغو شده",
}


def normalize_status(val: str) -> str:
    if not val:
        return "pending"
    stripped = val.strip()
    if stripped in STATUS_FA_TO_EN:
        return STATUS_FA_TO_EN[stripped]
    lower = stripped.lower()
    if lower in STATUS_FA_TO_EN:
        return STATUS_FA_TO_EN[lower]
    return lower


def order_to_response(o: Order) -> OrderResponse:
    canonical_status = normalize_status(o.status)
    display_status = STATUS_EN_TO_FA.get(canonical_status, canonical_status)
    return OrderResponse(
        id=o.id,
        customer_id=o.customer_id,
        customer_name=o.customer.name if o.customer else None,
        order_date=o.order_date,
        total_amount=o.total_amount,
        status=canonical_status,
        status_display=display_status,
        items=[
            OrderItemResponse(
                id=i.id,
                product_id=i.product_id,
                product_name=i.product.name if i.product else None,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in o.order_items
        ],
    )


@router.get("")
async def list_orders(
    request: Request,
    page: int = Query(1, ge=1),
    sort: str = Query("default"),
    q: str = Query(""),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    query = db.query(Order).options(joinedload(Order.customer), joinedload(Order.order_items))
    if q:
        query = query.join(Customer).filter(
            Customer.name.ilike(f"%{q}%") | Order.status.ilike(f"%{q}%")
        )

    if sort == "price":
        query = query.order_by(Order.total_amount.desc())
    elif sort == "status":
        query = query.order_by(Order.status)
    else:
        query = query.order_by(Order.id.desc())

    total = query.count()
    orders = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, (total + per_page - 1) // per_page),
        "orders": [order_to_response(o) for o in orders],
    }


@router.get("/{order_id}")
async def get_order(
    request: Request, order_id: int, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    order = (
        db.query(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.order_items).joinedload(OrderItem.product),
        )
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_to_response(order)


@router.post("", status_code=201)
async def create_order(
    request: Request, body: OrderCreate, db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    customer = db.query(Customer).filter(Customer.id == body.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    total = 0.0
    items_data = []
    for item in body.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found"
            )
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'. Available: {product.stock}",
            )
        total += product.price * item.quantity
        items_data.append((product, item.quantity))

    order = Order(
        customer_id=body.customer_id,
        total_amount=round(total, 2),
        status="pending",
        order_date=datetime.utcnow(),
    )
    db.add(order)
    db.flush()

    for product, qty in items_data:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                unit_price=product.price,
            )
        )
        product.stock -= qty

    db.commit()
    db.refresh(order)

    # Reload with relationships
    order = (
        db.query(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.order_items).joinedload(OrderItem.product),
        )
        .filter(Order.id == order.id)
        .first()
    )
    return order_to_response(order)


@router.patch("/{order_id}/status")
async def update_order_status(
    request: Request, order_id: int, body: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    if not require_auth(request):
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})

    normalized = normalize_status(body.status)
    valid_statuses = {"pending", "completed", "cancelled"}
    if normalized not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status: '{body.status}'. Must be one of: pending, completed, cancelled (یا معادل‌های فارسی: در انتظار، تکمیل شده، لغو شده)",
        )

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = normalized
    db.commit()

    order = (
        db.query(Order)
        .options(
            joinedload(Order.customer),
            joinedload(Order.order_items).joinedload(OrderItem.product),
        )
        .filter(Order.id == order.id)
        .first()
    )
    return order_to_response(order)

