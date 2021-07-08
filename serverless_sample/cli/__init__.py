import typer

from ..models.entries import Entry
from ..models.sessions import Session

app = typer.Typer()
cli_db = typer.Typer()


@app.command()
def run():
    """アプリケーションを起動します"""
    from .. import app as flask_app

    flask_app.run()


@cli_db.command()
def init():
    """データベースを初期化します"""
    from .. import app as flask_app

    env = flask_app.config["SERVERLESS_BLOG_CONFIG"]
    print(f"env: {env}")

    if not Entry.exists():
        Entry.create_table(read_capacity_units=5, write_capacity_units=2)

    if not Session.exists():
        Session.create_table(read_capacity_units=5, write_capacity_units=2)


@cli_db.command()
def remove():
    """データベースを削除します"""
    from .. import app as flask_app

    env = flask_app.config["SERVERLESS_BLOG_CONFIG"]
    print(f"env: {env}")

    if Entry.exists():
        Entry.delete_table()

    if Session.exists():
        Session.delete_table()


app.add_typer(cli_db, name="db", help="[サブコマンド]データベースに関するコマンド集です")
