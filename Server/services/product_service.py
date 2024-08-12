import json

from flask import make_response

from Server.utils import validate_token
from Server.utils.mongoJsonEncoder import Encoder

from model.product import ProductCategory, Product


# Categories Services Control
def get_category(category_id: str = None):
    try:
        categories = ProductCategory.objects.get(id=category_id) if category_id else ProductCategory.objects()
        return make_response({"category" if category_id else "categories": json.loads(categories.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


# @validate_token
def post_category(category_data: dict | list):
    def do_create(category_document: dict):
        category_check = ProductCategory.objects(name=category_document["name"])

        if category_check:
            return (False, "")

        category = ProductCategory(
            name=category_document["name"]
        ).save()
        
        return (True, str(category.id))
    try:
        categories_out = []
        
        if isinstance(category_data, list):
            for category_document in category_data:
                success, category_id = do_create(category_document)
                if success:
                    categories_out.append(category_id)
                else:
                    return make_response({"message": "category already exists"}, 404)
        elif isinstance(category_data, dict):
            success, category_id = do_create(category_document)
            if success:
                categories_out.append(category_id)
            else:
                return make_response({"message": "category already exists"}, 404)

        return make_response({"message": "successfully inserted", "result": categories_out}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


def put_category(category_id: str, category_data: dict):
    try:
        category = ProductCategory.objects.get(id=category_id)
        if category:
            category.name = category_data["name"]
            category.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "category does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_category(category_id: str):
    try:
        category = ProductCategory.objects.get(id=category_id)
        if category:
            category.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "category does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# Products Services Control
def get_product(product_id:str = None):
    try:
        products = Product.objects.get(id=product_id) if product_id else Product.objects()
        return {"product" if product_id else "products": json.loads(products.to_json(cls=Encoder))}
    except Exception as e:
        return make_response({"message": str(e)}, 404)


def get_product_by_category(category_id: str):
    products = []
    try:
        products = Product.objects(category=category_id)
        return {"products": json.loads(products.to_json(cls=Encoder))}
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# @validate_token
def post_product(product_data: dict):
    try:
        product =Product(
            title=product_data["title"],
            description=product_data["description"],
            category=product_data["category"],
            price=product_data["price"]
        ).save()

        return make_response({"message": "successfully inserted", "result": str(product.id)}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def put_product(product_id: str, product_data: dict):
    try:
        product = Product.objects.get(id=product_id) # return a queryset

        if product:
            product.title = product_data["title"]
            product.description = product_data["description"]
            product.category = product_data["category"]
            product.enabled = product_data["enabled"]
            product.price = product_data["price"]
            product.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "product does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_product(product_id: str):
    try:
        product = Product.objects.get(id=product_id)

        if product:
            product.delete()
            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "product does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)
