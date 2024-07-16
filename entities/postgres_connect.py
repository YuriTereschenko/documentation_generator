import psycopg2


class PgConnect:
    def __init__(self, host: str, port: str, db_name: str, user: str, pw: str) -> None:
        self.host = host
        self.port = int(port)
        self.db_name = db_name
        self.user = user
        self.pw = pw

    def url(self) -> str:
        return """
            host={host}
            port={port}
            dbname={db_name}
            user={user}
            password={pw}
            target_session_attrs=read-write
        """.format(
            host=self.host, port=self.port, db_name=self.db_name, user=self.user, pw=self.pw
        )

    def client(self):
        return psycopg2.connect(self.url())
