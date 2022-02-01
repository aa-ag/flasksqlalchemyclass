# Flask Sqlalchemy Class

Taking this class via [PrettyPrinted](https://courses.prettyprinted.com/).

### environment

- `python3 -m venv env`
- `source env/bin/activate`
- `pip3 install Faker` (github: [Faker](https://github.com/joke2k/faker))

### database creation

- `flask shell`
- `from app import db`
- `db.create_all()`
- `exit()`

### database access without UI

- `sqlite3 db.sqlite3`
- `.exit` 