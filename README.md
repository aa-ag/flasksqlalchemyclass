### Flask Sqlalchemy Class

Taking this class via [PrettyPrinted](https://courses.prettyprinted.com/).

# environment

- `python3 -m venv env`
- `source env/bin/activate`

### database creation

- `flask shell`
- `from app import db`
- `db.create_all()`

### database access without UI

- `sqlite3 db.sqlite3`