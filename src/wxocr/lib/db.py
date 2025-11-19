import os
import sqlite3
import secrets
from datetime import datetime

import click
from flask import current_app, g


"""apikey表结构
CREATE TABLE apikey (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  appname TEXT UNIQUE NOT NULL,
  apikey TEXT NOT NULL
);
"""


def get_db():
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE',os.path.join(os.path.dirname(__file__), 'wxocr.sqlite'))
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('./lib/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('add-key')
@click.option('--appname', prompt='授权给哪个应用',help='生成一个授权码')
def add_secret_command(appname):
    """Add a secret to the database."""
    api_key = secrets.token_hex(16)
    if is_appname_exists(appname):
        click.echo('App name:{} already exists.'.format(appname))
        return
    db = get_db()
    db.execute(
        'INSERT INTO apikey (appname,apikey) VALUES (?,?)',
        (appname,api_key)
    )
    db.commit()
    click.echo('Added a api key: {} for app: {}'.format(api_key,appname))


@click.command('del-key')
@click.option('--appname', prompt='删除一个应用',help='删除一个授权码')
def del_key_command(appname):
    """Delete a secret from the database."""
    db = get_db()
    db.execute(
        'DELETE FROM apikey WHERE appname = ?',
        (appname,)
    )
    db.commit()
    click.echo('Deleted a api key: {}'.format(appname))


@click.command('list-keys')
def list_keys_command():
    """List all api keys."""
    db = get_db()
    rows = db.execute('SELECT * FROM apikey').fetchall()
    
    if not rows:
        click.echo("No API keys found.")
        return
    
    # 打印表头
    click.echo(f"{'ID':<5} {'App Name':<20} {'API Key':<32}")
    click.echo("-" * 60)
    
    # 打印每一行数据
    for row in rows:
        click.echo(f"{row['id']:<5} {row['appname']:<20} {row['apikey']:<32}")

@click.command('clear-keys')
def clear_keys_command():
    db = get_db()
    db.execute('DELETE FROM apikey')
    db.commit()
    click.echo("API keys cleared.")


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_secret_command)
    app.cli.add_command(list_keys_command)
    app.cli.add_command(del_key_command)
    app.cli.add_command(clear_keys_command)



# 获取apikey表数据行数
def get_apikey_count():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM apikey")
        return cursor.fetchone()[0]

#判断apikey里字段apikey是否存在
def is_apikey_exists(apikey):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM apikey WHERE apikey = ?",(apikey,))
        return cursor.fetchone() != None

#判断apikey里字段appname是否存在
def is_appname_exists(appname):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM apikey WHERE appname = ?",(appname,))
        return cursor.fetchone() != None