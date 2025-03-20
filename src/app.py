import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# cargo desde el archivo .env
load_dotenv()

# 1) Connect to the database with SQLAlchemy
def connect():
    try:
        connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
        print("Iniciando...")
        engine = create_engine(connection_string, isolation_level="AUTOCOMMIT")
        engine.connect()
        print("¡Exito!")
        return engine
    except Exception as e:
        print(f"Error: {e}")
        return None

# Conectar a la base de datos
engine = connect()

if engine is None:
    exit()

# 2) Create the tables
with engine.connect() as connection:
    # He hecho que solo se creen si no existen para que no me de fallo la segunda vez en ejecutarlo
    sql = """
    CREATE TABLE IF NOT EXISTS publishers(
        publisher_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        PRIMARY KEY(publisher_id)
    );

    CREATE TABLE IF NOT EXISTS authors(
        author_id INT NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        middle_name VARCHAR(50) NULL,
        last_name VARCHAR(100) NULL,
        PRIMARY KEY(author_id)
    );

    CREATE TABLE IF NOT EXISTS books(
        book_id INT NOT NULL,
        title VARCHAR(255) NOT NULL,
        total_pages INT NULL,
        rating DECIMAL(4, 2) NULL,
        isbn VARCHAR(13) NULL,
        published_date DATE,
        publisher_id INT NULL,
        PRIMARY KEY(book_id),
        CONSTRAINT fk_publisher FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
    );

    CREATE TABLE IF NOT EXISTS book_authors (
        book_id INT NOT NULL,
        author_id INT NOT NULL,
        PRIMARY KEY(book_id, author_id),
        CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
    );
    """

# 3) Insert data
with engine.connect() as connection:
    # He hecho que si hay conflicto es decir ya está creado que no haga nada, al igual que en las tablas para que no de error
    print("Metiendo valores...")
    connection.execute(text("""
    -- authors 
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (1, 'Merritt', null, 'Eric')
    ON CONFLICT (author_id) DO NOTHING;
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (2, 'Linda', null, 'Mui')
    ON CONFLICT (author_id) DO NOTHING;
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (3, 'Alecos', null, 'Papadatos')
    ON CONFLICT (author_id) DO NOTHING;
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (4, 'Anthony', null, 'Molinaro')
    ON CONFLICT (author_id) DO NOTHING;
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (5, 'David', null, 'Cronin')
    ON CONFLICT (author_id) DO NOTHING;
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (6, 'Richard', null, 'Blum')
    ON CONFLICT (author_id) DO NOTHING;
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (7, 'Yuval', 'Noah', 'Harari')
    ON CONFLICT (author_id) DO NOTHING;
    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (8, 'Paul', null, 'Albitz')
    ON CONFLICT (author_id) DO NOTHING;

    -- books
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (1, 'Lean Software Development: An Agile Toolkit', 240, 4.17, '9780320000000', '2003-05-18', 5)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (2, 'Facing the Intelligence Explosion', 91, 3.87, null, '2013-02-01', 7)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (3, 'Scala in Action', 419, 3.74, '9781940000000', '2013-04-10', 1)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (4, 'Patterns of Software: Tales from the Software Community', 256, 3.84, '9780200000000', '1996-08-15', 1)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (5, 'Anatomy Of LISP', 446, 4.43, '9780070000000', '1978-01-01', 3)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (6, 'Computing machinery and intelligence', 24, 4.17, null, '2009-03-22', 4)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (7, 'XML: Visual QuickStart Guide', 269, 3.66, '9780320000000', '2009-01-01', 5)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (8, 'SQL Cookbook', 595, 3.95, '9780600000000', '2005-12-01', 7)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (9, 'The Apollo Guidance Computer: Architecture And Operation (Springer Praxis Books / Space Exploration)', 439, 4.29, '9781440000000', '2010-07-01', 6)
    ON CONFLICT (book_id) DO NOTHING;
    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (10, 'Minds and Computers: An Introduction to the Philosophy of Artificial Intelligence', 222, 3.54, '9780750000000', '2007-02-13', 7)
    ON CONFLICT (book_id) DO NOTHING;

    -- book authors
    INSERT INTO book_authors (book_id, author_id) VALUES (1, 1)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (2, 8)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (3, 7)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (4, 6)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (5, 5)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (6, 4)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (7, 3)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (8, 2)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (9, 4)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    INSERT INTO book_authors (book_id, author_id) VALUES (10, 1)
    ON CONFLICT (book_id, author_id) DO NOTHING;
    """))
    print("Valores metidos...")

# 4) Use Pandas to read and display a table
df_publishers = pd.read_sql("SELECT * FROM publishers;", engine)
print("\nTabla de publishers:")
print(f"{df_publishers}")

df_books = pd.read_sql("SELECT * FROM books;", engine)
print("\nTabla de books:")
print(df_books)

df_books_authors = pd.read_sql("SELECT * FROM book_authors;", engine)
print("\nTabla de books authors:")
print(df_books_authors)

