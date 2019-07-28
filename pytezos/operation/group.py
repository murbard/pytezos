from pprint import pformat

from pytezos.rpc import ShellQuery
from pytezos.crypto import Key
from pytezos.operation.content import ContentMixin
from pytezos.encoding import base58_encode


class OperationGroup(ContentMixin):

    def __init__(self, shell=None, key=None, contents=None, **kwargs):
        self.shell = shell  # type: ShellQuery
        self.key = key  # type: Key
        self.contents = contents
        self._kwargs = kwargs

    def __repr__(self):
        return pformat(self.payload())

    def payload(self):
        return {
            'protocol': self._kwargs.get('protocol'),
            'branch': self._kwargs.get('branch'),
            'contents': self.contents,
            'signature': self._kwargs.get('signature')
        }

    def operation(self, content):
        return OperationGroup(
            shell=self.shell,
            key=self.key,
            contents=self.contents + [content],
            **self._kwargs
        )

    def autofill(self):
        branch = self._kwargs.get('branch', self.shell.head.predecessor.hash())
        block = self.shell.blocks[branch]
        protocol = self._kwargs.get('protocol', block.header()['protocol'])
        source = self.key.public_key_hash()
        counter = block.context.contracts[source].next_counter()
        contents = self.contents.copy()

        for content in contents:
            if content.get('source') == '':
                content['source'] = source
            if content.get('pkh') == '':
                content['pkh'] = source
            if content.get('counter') == '0':
                content['counter'] = str(counter)
                counter += 1
            if content.get('fee') == '0':
                content['fee'] = '1000'
            if content.get('gas_limit') == '0':
                content['gas_limit'] = '400000'
            if content.get('storage_limit') == '0':
                content['storage_limit'] = '60000'
            if content.get('period') == '0':
                content['period'] = str(block.voting_period())
            if content.get('delegate') == '':
                content['delegate'] = source
            if content.get('manager_pubkey') == '':
                content['manager_pubkey'] = self.key.public_key()

        return OperationGroup(
            shell=self.shell,
            key=self.key,
            contents=contents,
            protocol=protocol,
            branch=branch
        )

    def run(self):
        return self.shell.head.helpers.scripts.run_operation.post({
            'branch': self._kwargs.get('branch'),
            'contents': self.contents,
            'signature': base58_encode(b'0' * 64, b'sig').decode()
        })

    def forge(self):
        pass

    def sign(self):
        pass

    def preapply(self):
        pass

    def inject(self):
        pass
