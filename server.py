from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Union, Optional

from starlette.responses import JSONResponse

from database import MongoDBClient
from utils import identify_data_type, get_field_types

description = """
Web service helps to find form from database which can be filled with information from request.
"""
app = FastAPI(title="forms database",
              description=description,
              summary="This app can find forms and specify information from requests",
              contact={
                  "name": "Anton Khr",
                  "email": "antokhrist@gmail.com",
              }, )
connection_string = "mongodb://mongodb:27017"
database_name = "forms"

# Создаем экземпляр класса MongoDBClient
mongodb_client = MongoDBClient(connection_string, database_name)


class QueryParams(BaseModel):
    field_name_1: Union[str, None]
    field_name_2: Union[str, None]
    field_name_3: Union[str, None]
    field_name_4: Union[str, None]


@app.post("/get_form")
async def get_form_data(
        field_name_1: Optional[str] = None,
        field_name_2: Optional[str] = None,
        field_name_3: Optional[str] = None,
        field_name_4: Optional[str] = None,
):
    # Создаем словарь с параметрами запроса, удаляем None значения
    query_params = {key: value for key, value in locals().items() if value is not None}

    # Заменяем непустые значения параметров запроса результатами функции identify_data_type()
    for key, value in query_params.items():
        query_params[key] = identify_data_type(value)
    # обработка пустого запроса
    if not query_params:
        return JSONResponse(content={"message": "empty form, fill in params"}, status_code=400)
    # Ищем документ в базе данных с использованием параметров запроса
    found_documents = mongodb_client.search_matches("forms", query_params)
    # Если документ найден, возвращаем поле name, иначе возвращаем сообщение
    if found_documents:
        res = {"name": doc.get("name") for doc in found_documents}
        return res

    # Если не найден подходящий шаблон, возвращаем типы полей
    field_types = get_field_types(query_params)
    return field_types


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
