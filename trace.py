import functools
import sys
from importlib.metadata import version

import click.core as core
import click.parser as parser
import click.types as types

from custom_type import EvenInt, half
from test import fail

depth = 0


def short(x, n=70):
    s = repr(x)
    return s if len(s) <= n else s[: n - 3] + "..."


def wrap(cls, name, show):
    original = getattr(cls, name)

    @functools.wraps(original)
    def traced(self, *args, **kwargs):
        global depth
        if getattr(self, "name", None) == "help":
            return original(self, *args, **kwargs)
        who = f"{type(self).__name__}({self.name})" if isinstance(self, core.Parameter) else type(self).__name__
        print("   " * depth + f"-> {who}.{name}({show(*args, **kwargs)})")
        depth += 1
        try:
            result = original(self, *args, **kwargs)
        except BaseException as e:
            depth -= 1
            print("   " * depth + f"!! {type(e).__name__}: {e}")
            raise
        depth -= 1
        print("   " * depth + f"<- {short(result)}")
        return result

    setattr(cls, name, traced)


def install():
    wrap(core.Command, "main", lambda args=None, **k: f"args={short(args)}")
    wrap(core.Command, "make_context", lambda n, args, **k: f"{n!r}, args={short(args)}")
    wrap(core.Command, "make_parser", lambda ctx: "ctx")
    wrap(parser._OptionParser, "parse_args", lambda args=None: f"args={short(args)}")
    wrap(core.Parameter, "handle_parse_result", lambda ctx, opts, args: f"opts={short(dict(opts))}")
    wrap(core.Parameter, "consume_value", lambda ctx, opts: "ctx, opts")
    wrap(core.Parameter, "type_cast_value", lambda ctx, value: f"value={short(value)}")
    wrap(types._NumberParamTypeBase, "convert", lambda value, param, ctx: f"value={short(value)}")
    wrap(EvenInt, "convert", lambda value, param, ctx: f"value={short(value)}")
    wrap(types.ParamType, "fail", lambda msg, param=None, ctx=None: f"message={short(msg)}")
    wrap(core.Context, "invoke", lambda cb, *a, **k: f"{cb.__name__}, kwargs={short(k)}")


SCENARIOS = {
    "ok": (fail, ["--count", "3", "Alice"]),
    "error": (fail, ["--count", "abc", "Alice"]),
    "custom": (half, ["--n", "3"]),
}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "ok"
    if name not in SCENARIOS:
        sys.exit("Сценарии: " + ", ".join(SCENARIOS))
    command, args = SCENARIOS[name]
    print(f"click {version('click')}: {command.name} {' '.join(args)}\n")
    install()
    try:
        command.main(args=args, prog_name=command.name)
    except SystemExit as e:
        print(f"\nкод выхода: {e.code}")
