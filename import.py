"""Import table file."""

import os
import csv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("sqlite:///book.db")
db = scoped_session(sessionmaker(bind=engine))


def main():
    """Main function."""
    with open("book_file.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            db.execute("INSERT INTO books ( title, author, year,isbn) VALUES ( :title, :author, :year,:isbn)",
                       { "title": row[0], "author": row[1], "year": row[2],"isbn": row[3],})
            db.commit()
    print("Imported!")


if __name__ == "__main__":
    main()
