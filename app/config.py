from fastapi.templating import Jinja2Templates

# from dotenv import load_dotenv
# load_dotenv()

LOCAL = False

templates = Jinja2Templates(directory="app/api/templates")

# with open("app/config.json") as f:
#     config = json.loads(f.read())


def get_vector_db_uri() -> str:
    # uri = os.getenv("POSTGRES_URI")
    # return uri if not LOCAL else uri.replace("desarrollo-postgres-1", "localhost")  # type: ignore
    return 'postgresql://postgres:postgres@localhost:5432/vector_db'
