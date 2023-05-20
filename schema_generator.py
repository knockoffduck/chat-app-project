from website import create_app, db
from website.models import User, Chat
from config import Config

app = create_app(Config)

# Create Flask application context
with app.app_context():
    # Generate the schema and table definitions
    schema = db.metadata
    schema.reflect(bind=db.engine)

    for table in schema.sorted_tables:
        print(f"Table Name: {table.name}")
        print("Columns:")
        for column in table.c:
            print(f"\t{column.name} - {column.type}")

        # Primary Key
        print(f"Primary Key: {table.primary_key.columns.keys()}")

        # Foreign Keys
        for fk in table.foreign_keys:
            source_column = fk.column
            source_table = source_column.table.name
            source_column_name = source_column.name
            print(f"Foreign Key: {source_column_name} -> {source_table}.{source_column_name}")

        print("-----------------------------")
