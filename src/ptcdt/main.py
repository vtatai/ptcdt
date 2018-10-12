import click
import ptcdt.server

@click.command()
@click.argument('config', type=click.Path(exists=True), required=True)
def main(config):
    ptcdt.server.serve_config(config)
