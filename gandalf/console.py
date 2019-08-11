import sys
import os

import click


def import_application(app_package, appbuilder):
    sys.path.append(os.getcwd())
    try:
        _app = __import__(app_package)
    except Exception as e:
        click.echo(
            click.style(
                "Was unable to import {0} Error: {1}".format(app_package, e), fg="red"
            )
        )
        exit(3)
    if hasattr(_app, appbuilder):
        return getattr(_app, appbuilder)
    else:
        click.echo(
            click.style(
                "There is no appbuilder var on your package, "
                "you can use appbuilder parameter to config",
                fg="red",
            )
        )
        exit(3)


def echo_header(title):
    click.echo(click.style(title, fg="green"))
    click.echo(click.style("-" * len(title), fg="green"))


@click.group()
def cli_app():
    pass


def cli():
    cli_app()


if __name__ == '__main':
    cli_app()
