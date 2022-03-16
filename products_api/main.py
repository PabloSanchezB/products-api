from fastapi import FastAPI, APIRouter, HTTPException
from model.schemas import Product, ProductCreate

app = FastAPI(title = "Products API")

api_router = APIRouter()

products = [
            {
                "id": 1,
                "name": "I Phone 13",
                "quantity": 12,
                "description": "Nuevo celular de Apple",
                "precio": 4500000,
                "category": 1
            },
            {
                "id": 2,
                "name": "MSI GF13 thin",
                "quantity": 10,
                "description": "Laptop para gamer",
                "precio": 5000000,
                "category": 2
            }
            ]


@api_router.get("/products/")
def product_list() -> dict:
    return products


@api_router.get("/products/{id}/", status_code = 200, response_model = Product)
def fetch_product(*,id:int) -> any:
    result = [item for item in products if item["id"] == id]
    if not result:
        raise HTTPException(status_code = 404, detail = f"Product with id {id} not found")
    return result[0]


@api_router.get("/products/category/{category_id}")
def search_by_category(*,category_id:int) -> dict:
    result = [item for item in products if item["category"] == category_id]
    return {"results":result}


@api_router.post("/products/", status_code = 201, response_model = Product)
def add_product(*,product_in:ProductCreate) -> dict:
    id_count = len(products) + 1
    new_product = Product(
        id = id_count,
        name = product_in.name,
        quantity = product_in.quantity,
        description = product_in.description,
        precio = product_in.precio,
        category = product_in.category
    )
    products.append(new_product.dict())
    return new_product


app.include_router(api_router)