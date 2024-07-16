from pydantic import BaseModel

class TableLocation:
    def __init__(self, table_catalog: str, table_schema: str, table_name:str):
        self.table_catalog = table_catalog
        self.table_schema = table_schema
        self.table_name = table_name
