from utils.BaseRepository import BaseRepository
from app.models import Product


class ProductRepository(BaseRepository):

    def init_model(self):
        return Product


if __name__ == '__main__':
    product = ProductRepository().show(796)
    print(product)
