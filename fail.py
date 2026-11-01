import click

@click.command()
@click.option("--count", default=2, type=int)
@click.argument("name")
def greet(count, name):
    for _ in range(count):
        click.echo(f"Hello {name}!")

if __name__ == "__main__":
    greet()