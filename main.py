import logging
from repository.postgres_db import DatabasePostgres
from entities.postgres_connect import PgConnect
from md_generator import MdGenerator


if __name__ == '__main__':
    # Создаем экземпляр коннекта
    conn = PgConnect()
    # Создаем объект БД
    db = DatabasePostgres(conn)

    # указываем путь сохранения готовых md файлов
    path = ''
    logger = logging.getLogger('__name__')
    generator = MdGenerator(db, 'resources/template.md', logger, path)

    # для генерации документации всех таблиц БД
    generator.generate_all_tables()

    # для генерации документации одной таблицы БД
    generator.generate_one_table('table_name')
