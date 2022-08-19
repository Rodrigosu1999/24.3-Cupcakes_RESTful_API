"""File to add functionality to the app.py file"""


def serialize_cupcake(self):
    """Serialize a cupcake SQLAlchemy object into a dictionary"""

    return {
        "id": self.id,
        "flavor": self.flavor,
        "size": self.size,
        "rating": self.rating,
        "image": self.image
    }
