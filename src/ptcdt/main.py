import click
import ptcdt.server

@click.command()
@click.option('--config', default="ptcdt.properties", help='Config file')
def start_server(config):
    ptcdt.server.serve_config(config)

if __name__ == '__main__':
    start_server()
