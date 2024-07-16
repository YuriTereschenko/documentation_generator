from typing import List
from repository.repo_abstract import IRepository
import psycopg2
import psycopg2.extras
from entities.table import Table
from entities.column import Column
from entities.table_location import TableLocation
from entities.postgres_connect import PgConnect


class DatabasePostgres(IRepository):
    def __init__(self, conn: PgConnect):
        self._conn = conn

    def get_columns(self, table_name: str) -> List[Column]:
        with self._conn.client() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                with open('resources/column_info_postgres.sql', 'r') as f:
                    query = f.read()

                query = query.format(table_name=table_name)
                cur.execute(query)
                columns_info = cur.fetchall()
                return [Column(column_name=x['column_name'],
                               data_type=x['data_type'],
                               required_field=x['is_nullable'],
                               column_default=x['column_default'],
                               description=x['description'],
                               constraint=x['column_constr']) for x in columns_info]

    def get_table(self, table_name: str) -> Table:
        with self._conn.client() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute('''
                SELECT t.table_catalog,
                       t.table_schema,
                       table_name,
                       COALESCE(OBJ_DESCRIPTION(pc.oid), '')            AS description
                FROM
                    information_schema.tables t
                        LEFT JOIN pg_catalog.pg_statio_all_tables st
                                  ON t.table_name = st.relname AND t.table_schema = st.schemaname
                        LEFT JOIN pg_catalog.pg_description pgd ON pgd.objoid = st.relid
                        LEFT JOIN pg_catalog.pg_class pc ON st.relid = pc.oid
                WHERE
                      table_type = 'BASE TABLE'
                  AND table_schema NOT IN ('pg_catalog', 'information_schema')
                  AND t.table_name = %(table_name)s;
                                    ''', {
                    'table_name': table_name
                })
                data = cur.fetchone()
                return Table(db_name=data['table_catalog'],
                             table_schema=data['table_schema'],
                             table_name=data['table_name'],
                             table_description=data['description'],
                             columns=self.get_columns(table_name))

    def get_tables_location(self) -> List[TableLocation]:
        with self._conn.client() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        COALESCE(table_catalog, 'None') AS table_catalog
                      , COALESCE(table_schema, 'None') AS table_schema
                      , COALESCE(table_name, 'None') AS table_name
                    FROM
                        information_schema.tables
                    WHERE
                          table_type = 'BASE TABLE'
                      AND table_schema NOT IN ('pg_catalog', 'information_schema');
                      """
                )
                return [TableLocation(*row) for row in cur.fetchall()]

