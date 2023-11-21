from pymongo import MongoClient

from utils import max_dict_from_list


class MongoDBClient:
    def __init__(self, connection_string, database_name):
        self.client = MongoClient(connection_string)
        self.database = self.client[database_name]

    def insert_one(self, collection_name, document):
        collection = self.database[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def search_matches(self, collection_name, fields_to_match):
        query_formed = []
        # формируем запрос для mongodb
        for field, value in fields_to_match.items():
            query_formed.append({'$or': [{field: value}, {field: {'$exists': False}}]})
        collection = self.database[collection_name]
        result = collection.find({"$and": query_formed})
        # среди найденным документом ищет документы,
        # в которых нет лишних полей (лишние - те, которых не было в запросе)
        match_list = []
        for res_ in result:
            if (set(res_.keys()) - {'_id'} - {'name'}).issubset(set(fields_to_match.keys())):
                match_list.append(res_)
        # если документы найдены, то выбираем документы с наибольшим числом полей(эти документы и есть наиболее
        # подходящие)
        if match_list:
            perfect_match = max_dict_from_list(match_list)
            return perfect_match
        else:
            return None

    def delete_one(self, collection_name, query):
        collection = self.database[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count


if __name__ == "__main__":
    connection_string = "mongodb://mongodb:27017"
    database_name = "forms"

    # Создаем экземпляр класса MongoDBClient
    mongodb_client = MongoDBClient(connection_string, database_name)

    # тестовые формы
    templates = [
        {"name": "Form template 1", "field_name_1": "email", "field_name_2": "phone"},
        {"name": "Form template 1.1", "field_name_1": "email", "field_name_2": "phone", "field_name_3": "text"},
        {"name": "Form template 2", "field_name_1": "text", "field_name_2": "date"},
        {"name": "Form template 3", "field_name_1": "email", "field_name_2": "text", "field_name_3": "phone",
         "field_name_4": "date"},
        {"name": "Form template 4", "field_name_1": "phone", "field_name_2": "date", "field_name_3": "text"},
        {"name": "Form template 5", 'field_name_1': 'text', 'field_name_2': 'email', 'field_name_3': 'date'}
    ]

    # Вставляем каждый документ в коллекцию
    for template in templates:
        inserted_id = mongodb_client.insert_one("forms", template)
        print(f"Inserted document for test with ID: {inserted_id}")