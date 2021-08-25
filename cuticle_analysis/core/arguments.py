
import argparse

from .display import LINE_SIZE


class Args:
    def __init__(self, * args, mutex: list = [], group: list = [], **kargs):
        self.args = args
        self.kargs = kargs
        self.group = group
        self.mutex = mutex
        self.arguments = None

    def build(self, parser=None):
        if parser is None:
            parser = argparse.ArgumentParser(
                prog='cuticle_analysis',
                epilog='~'*LINE_SIZE,
                usage='cuticle_analysis [options...]'
            )

        if len(self.args) or len(self.kargs):
            parser.add_argument(*self.args, **self.kargs)

        if len(self.group):
            arg_group = parser.add_argument_group()
            for arg in self.group:
                arg.build(arg_group)

        if len(self.mutex):
            mutex_group = parser.add_mutually_exclusive_group()
            for arg in self.mutex:
                arg.build(mutex_group)

        return parser

    def get_args(self):
        if self.arguments is None:
            self.arguments, _ = self.build().parse_known_args()
        return self.arguments


_builder = Args(
    group=[
        Args('--download-dataset', action='store_true',
             help='download and unzip dataset')
    ],
)


def get_args():
    return _builder.get_args()
