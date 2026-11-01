import click


class EvenInt(click.ParamType):
    name = "even integer"

    def convert(self, value, param, ctx):
        try:
            number = int(value)
        except ValueError:
            self.fail(f"{value!r} is not an integer", param, ctx)
        if number % 2:
            self.fail(f"{number} is not even", param, ctx)
        return number

EVEN = EvenInt()

@click.command()
@click.option("--n", type=EVEN, required=True)
def half(n):
    click.echo(f"{n} / 2 = {n // 2}")

if __name__ == "__main__":
    half()