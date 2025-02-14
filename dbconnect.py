import os

import sqlalchemy
from dotenv import load_dotenv

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
		"""Initializes a TCP connection pool for a Cloud SQL instance of SQL Server."""
		# Note: Saving credentials in environment variables is convenient, but not
		# secure - consider a more secure solution such as
		# Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
		# keep secrets safe.
		load_dotenv()

		db_host = os.environ[
				"INSTANCE_HOST"
		]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
		db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
		db_pass = os.environ["DB_PASSWORD"]  # e.g. 'my-db-password'
		db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
		db_port = os.environ["DB_PORT"]  # e.g. 1433

		pool = sqlalchemy.create_engine(
				# Equivalent URL:
				# mssql+pytds://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
				sqlalchemy.engine.url.URL.create(
						drivername="mssql+pytds",
						username=db_user,
						password=db_pass,
						database=db_name,
						host=db_host,
						port=db_port,
				),
				# ...
		)

		return pool

connect_tcp_socket()