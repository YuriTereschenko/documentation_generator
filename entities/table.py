from entities.column import Column
from typing import List


class Table:
    def __init__(self,
                 db_name: str,
                 table_schema: str,
                 table_name: str,
                 table_description: str,
                 columns: List[Column]):
        self.db_name = db_name
        self.table_schema = table_schema
        self.table_name = table_name
        self.table_description = table_description
        self.columns = columns

    def generate_md_string(self, template: str) -> str:
        md_string = template.format(table_name=self.table_name,
                table_description=self.table_description,
                db_name=self.db_name,
                schema=self.table_schema)
        columns = "\n".join([column.generate_md_string_column() for column in self.columns])
        md_string += columns
        return md_string

