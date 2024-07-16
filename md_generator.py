import logging

from repository.repo_abstract import IRepository
from pathlib import Path


class MdGenerator:
    def __init__(self, repository: IRepository, template_path: str, logger: logging.Logger, base_save_path="~/"):
        self._repo = repository
        self._base_save_path = base_save_path
        self._template_path = template_path
        self.log = logger

    def generate_one_table(self, table_name: str):
        table = self._repo.get_table(table_name)
        with open(self._template_path, "r") as f:
            template = f.read()
        md_str = table.generate_md_string(template)
        Path(f'{table.db_name}/{table.table_schema}/').mkdir(parents=True, exist_ok=True)
        with open(f'{self._base_save_path}/{table.db_name}/{table.table_schema}/{table.table_name}.md', 'w') as md_file:
            md_file.write(md_str)

    def generate_all_tables(self):
        table_list = self._repo.get_tables_location()
        counter = int()
        for table in table_list:
            counter += 1
            self.generate_one_table(table.table_name)
            self.log.info(f"Generated file {counter} of {len(table_list)}")
