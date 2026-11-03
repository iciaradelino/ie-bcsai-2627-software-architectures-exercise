# PRESENTATION LAYER: receives requests and returns (status code, body).
# It only calls business.py and turns its errors into status codes.

import business
from business import InvalidData, NotEnoughStock, NotFound


def to_response(error):
    if isinstance(error, InvalidData):
        return 400, {"error": str(error)}
    if isinstance(error, NotFound):
        return 404, {"error": str(error)}
    if isinstance(error, NotEnoughStock):
        return 409, {"error": str(error)}
    raise error


class ShopAPI:
    def add_book(self, request):
        try:
            book = business.add_book(request.get("title"), request.get("price_cents"), request.get("stock"))
        except business.ShopError as error:
            return to_response(error)
        print("Added book " + book["title"])
        return 201, book

    def list_books(self):
        return 200, business.list_books()

    def place_order(self, request):
        try:
            order = business.place_order(request.get("book_id"), request.get("quantity"))
        except business.ShopError as error:
            return to_response(error)
        print("Order placed for book " + str(order["book_id"]))
        return 201, order

    def get_order(self, order_id):
        try:
            return 200, business.get_order(order_id)
        except business.ShopError as error:
            return to_response(error)
