from pytezos.michelson.grammar import MichelsonParser

michelson_parser = MichelsonParser()


def michelson_to_micheline(source):
    return michelson_parser.parse(source)
