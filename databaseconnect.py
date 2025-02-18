import os

import sqlalchemy
from dotenv import load_dotenv


def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
		"""Initializes a Unix socket connection pool for a Cloud SQL instance of Postgres."""
		# Note: Saving credentials in environment variables is convenient, but not
		# secure - consider a more secure solution such as
		# Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
		# keep secrets safe.
		db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
		db_pass = os.environ["DB_PASSWORD"]  # e.g. 'my-database-password'
		db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
		unix_socket_path = os.environ[
				"INSTANCE_UNIX_SOCKET"
		]  # e.g. '/cloudsql/project:region:instance'

		urr = sqlalchemy.engine.url.URL.create(
						drivername="postgresql",
						username=db_user,
						password=db_pass,
						database=db_name,
						query={"unix_sock": f"{unix_socket_path}/.s.PGSQL.5432"},
				)
		pool = sqlalchemy.create_engine(
				# Equivalent URL:
				# postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
				#                         ?unix_sock=<INSTANCE_UNIX_SOCKET>/.s.PGSQL.5432
				# Note: Some drivers require the `unix_sock` query parameter to use a different key.
				# For example, 'psycopg2' uses the path set to `host` in order to connect successfully.
				urr
				# ...
		)
		return pool
		
		
def test_connection():
    try:
        engine = connect_unix_socket()  # Use your existing function
        with engine.connect() as connection:
            result = connection.execute(sqlalchemy.text("SELECT 1"))
            print("Connection successful:", result.scalar())  # Should print 1 if successful
    except Exception as e:
        print("Connection failed:", str(e))

load_dotenv()
test_connection()


# connect_unix_socket()