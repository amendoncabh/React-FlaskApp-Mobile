from flask import Blueprint, request

from services.product_service import (
    get_category,
    post_category,
    put_category,
    delete_category,
    get_product,
    get_product_by_category,
    post_product,
    put_product,
    delete_product
)


categories_bp = Blueprint(name = 'categories', import_name = __name__, url_prefix = "/api/v2/categories")
products_bp = Blueprint(name = 'products', import_name = __name__, url_prefix = "/api/v2/products")


# Product Categories Routes
@categories_bp.route("/all", methods=['GET'])
def get_categories_all():
    return get_category()

@categories_bp.route("/<category_id>", methods=['GET'])
def get_category_id(category_id):
    return get_category(category_id)

@categories_bp.route("/add", methods=['POST'])
def post_category():
    data = request.get_json()
    return post_category(data)

@categories_bp.route("/update/<category_id>", methods=['PUT'])
def put_category(category_id):
    category_data = request.get_json()
    return put_category(category_id, category_data)

@categories_bp.route("/delete/<category_id>", methods=['DELETE'])
def delete_category(category_id):
    return delete_category(category_id)


# Products Routes
@products_bp.route("/all", methods=['GET'])
def get_products():
    return get_product()

@products_bp.route("/<product_id>", methods=['GET'])
def get_product_by_id(product_id):
    return get_product(product_id)

@products_bp.route("/category/<category_id>", methods=['GET'])
def get_product_by_category(category_id):
    return get_product_by_category(category_id)

@products_bp.route("/add", methods=['POST'])
def post_product():
    data = request.get_json()
    return post_product(data)

@products_bp.route("/update/<product_id>", methods=['PUT'])
def put_product(product_id):
    product_data = request.get_json()
    return put_product(product_id, product_data)

@products_bp.route("/delete/<product_id>", methods=['DELETE'])
def delete_product(product_id):
    return delete_product(product_id)
