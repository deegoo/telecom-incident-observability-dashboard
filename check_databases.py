from sqlalchemy import create_engine, text

USER = "postgres"
PASSWORD = "1406"
HOST = "localhost"
PORT = "5432"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres"
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT datname FROM pg_database"))
    print("Bancos encontrados:")
    for row in result:
        print("-", row[0])
