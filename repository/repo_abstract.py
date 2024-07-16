from abc import ABC, abstractmethod
from typing import List

from entities.table import Table
from entities.column import Column
from entities.table_location import TableLocation


class IRepository(ABC):
    @abstractmethod
    def get_columns(self, table_name: str) -> List[Column]:
        raise NotImplemented

    @abstractmethod
    def get_table(self, table_name: str) -> Table:
        raise NotImplemented

    @abstractmethod
    def get_tables_location(self) -> List[TableLocation]:
        raise NotImplemented