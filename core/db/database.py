from sqlmodel import create_engine, Session


engine = create_engine('postgresql://postgres:postgres@localhost:5433/postgres')
session = Session(engine)


# используется с pandas to_sql
legacy_engine = create_engine('postgresql://postgres:postgres@localhost:5433/postgres', future=False)