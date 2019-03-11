import os
import simplejson as json

from pytezos.rpc.protocol import Protocol


def generate_html(patch: Protocol, output_path=None):
    with open(os.path.join(os.path.dirname(__file__), 'diff.html'), 'r') as f:
        template = f.read()

    text = '\n'.join([text for filename, text in patch if text])
    html = template.replace('{{text}}', json.dumps(text))

    if output_path:
        with open(output_path, 'w') as f:
            f.write(html)
    else:
        return html
