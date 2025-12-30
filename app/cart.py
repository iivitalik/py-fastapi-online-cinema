from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, database, auth

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=schemas.CartOut)
def get_cart(db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.post("/add/{movie_id}")
def add_to_cart(movie_id: int, db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    is_purchased = db.query(models.PurchasedMovie).filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if is_purchased:
        raise HTTPException(status_code=400, detail="Repeat purchases are not allowed")

    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        cart = models.Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    existing_item = db.query(models.CartItem).filter_by(cart_id=cart.id, movie_id=movie_id).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Movie already in cart")

    new_item = models.CartItem(cart_id=cart.id, movie_id=movie_id)
    db.add(new_item)
    db.commit()
    return {"message": "Movie added to cart"}


@router.delete("/remove/{movie_id}")
def remove_from_cart(movie_id: int, db: Session = Depends(database.get_db),
                     current_user=Depends(auth.get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = db.query(models.CartItem).filter_by(cart_id=cart.id, movie_id=movie_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(item)
    db.commit()
    return {"message": "Movie removed from cart"}


@router.post("/checkout")
def checkout(db: Session = Depends(database.get_db), current_user=Depends(auth.get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart.items:
        purchase = models.PurchasedMovie(user_id=current_user.id, movie_id=item.movie_id)
        db.add(purchase)

    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()
    return {"message": "Payment successful, movies added to purchased list"}
