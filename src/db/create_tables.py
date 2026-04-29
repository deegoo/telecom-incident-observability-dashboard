from src.db.models import Base
from src.core.database import engine


def create_tables():
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    create_tables()


# CONFIG
USER = "postgres"
PASSWORD = "1406"
HOST = "localhost"
PORT = "5432"
DATABASE = "telecom_incidents"

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

Base.metadata.create_all(engine)

print("Tabelas criadas com sucesso.")
