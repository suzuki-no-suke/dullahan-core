import typer
from pathlib import Path
from alembic.config import Config
from alembic import command

app = typer.Typer()

@app.command()
def migrate():
    """Migrete dullahan database tables"""
    basepath = Path(__file__).parent
    config = Config(basepath.joinpath("alembic.ini"))
    config.set_main_option("script_location", str(Path(__file__).parent.joinpath("db/migrations")))
    command.upgrade(config, 'head')

if __name__ == "__main__":
    app()
