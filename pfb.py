#MY NODE ID: 12D3KooWGMx7VZ9tgYAk3GgAcK5p8NE5Y5VgUDTNvB6PY76BHgC4

import flask
from pywebio.input import *
from pywebio.output import *
import requests
import json
from pywebio.platform.flask import webio_view
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)


def main():
    img = open('./logo.png', 'rb').read()
    put_image(img)
    put_markdown('# UI for Submitting PayForBlob Transactions')

    user_data = input_group("PayForBlob Parameters", [
        # radio("Schema", name='schema', options=['http', 'https'], value='http', required=True),
        select('Schema type', name='schema', options=['http', 'https'], value='http', required=True),
        input('Node IP', name='node_ip', value='194.163.160.60', required=True),
        input('Port', name='port', value='26659', required=True),
        input('Message', name='data', required=True),
        input('Namespace Id', name='namespace_id', value='0c204d39600fddd3', required=True),
        input('Gas', name='gas_limit', type=NUMBER, value='80000', required=True),
        input('Fee', name='fee', type=NUMBER, value='2000', required=True),
    ])
    with put_loading():
        put_text('Waiting for response...')
        resp = submit_pfb(user_data)

        if 'txhash' in str(resp):
            put_text('Successfully submitted!')
            tx_hash = resp['txhash']
            put_table([
                ['Type', 'Content'],
                ['Block Height', resp['height']],
                ['Tx hash (click to check it on explorer)',
                 put_link(tx_hash, f'https://testnet.mintscan.io/celestia-incentivized-testnet/txs/{tx_hash}')],
                ['Submit again', put_text('Please refresh the page.')],
            ])
        else:
            put_text('Submit error. Please check the parameters!')


def submit_pfb(data):
    try:
        url = data['schema'] + '://' + data['node_ip'] + ':' + str(data['port']) + '/submit_pfb'
        payload_names = {'namespace_id', 'data', 'gas_limit', 'fee'}
        payload = {key: value for key, value in data.items() if key in payload_names}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
    except Exception as err:
        return err


if __name__ == '__main__':
    app.add_url_rule('/', 'webio_view', webio_view(main), methods=['GET', 'POST', 'OPTIONS'])
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0')
