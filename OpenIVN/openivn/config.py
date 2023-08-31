"""OpenIVN development configuration."""
import os

# Root of application
APPLICATION_ROOT = '/'

# Database file path
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'openivn.sqlite3'
)

CLOUD_COMPUTING_API_ENDPOINT = "https://neuer.eecs.umich.edu:1620/container/add"

CLOUD_COMPUTING_RECEIVER_PORT = 1622


SCRIPT_DIRECTORY = os.path.join(os.getcwd(), 'developer_executables')

# Secret key is used to manage user sessions
# Set SECRET_KEY with: python3 -c "import os; print(os.urandom(24))"
SECRET_KEY = b'\xa3g\x9bU_%\xc4r\x8b\x0cmm\tvh\r+\xc2\xe6\xe9\xd1GC\x16'
# SESSION_COOKIE_NAME = 'login'
