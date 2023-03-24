import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
import numpy as np
import json
import pandas as pd
from datetime import datetime
import requests
from time import sleep

def extract_data(start_block, end_block):
    bck= {
        'ethereum': {'chain': 'eth', 'node_url': 'https://eth.llamarpc.com', 'explorer_url': 'https://api.etherscan.io/api', 'api_key':'XS54T9YEXVT2RPXBWDJHUT5D6DCSIGWF73'},
        'bsc': {'chaisn': 'bsc', 'node_url':'https://bsc-dataseed.binance.org/', 'explorer_url':'http://api.bscscan.com/api', 'api_key': 'JFVAD3XHTZY7DZ2WZM5IPKDYVQK1M5IMT8' },
        'polygon': {'chain': 'polygon', 'node_url':'https://polygon-rpc.com', 'explorer_url':'http://api.polygonscan.com/api', 'api_key': 'D7ZW5H9BW4M8H24E9HV65AUDXM3ZHZTNR8'}
        }

    web3 = Web3(Web3.HTTPProvider(bck['ethereum']['node_url']))
    data = np.array([])

    i = 0

    for block_number in range(start_block, end_block):
        while True:
            try:
                block_data = web3.eth.getBlock(block_identifier=block_number, full_transactions=True)
                break
            except:
                sleep(1)
                continue

        n_txn = len(block_data['transactions'])
        dt = datetime.fromtimestamp(block_data['timestamp'])

        gas_price = np.array([])
        for t in block_data['transactions']:
            gas_price = np.append(gas_price, t['gasPrice'])
        gas_price = np.mean(gas_price)

        params = {
            "query":'{bundle(id:"1", block: {number: %s}){ethPrice}}'%str(block_number),
            "operationName": None,
            "variables": None,
            }
        url = 'https://api.thegraph.com/subgraphs/name/ianlapham/uniswapv2'
        while True:
            try:
                eth_price = float(requests.post(url, data=json.dumps(params)).json()['data']['bundle']['ethPrice'])
                break
            except:
                sleep(1)
                continue

        data = np.append(data, [dt, n_txn, eth_price, gas_price])
        i = i+1
        print(i)
         
    np.savetxt("blockDataSample.csv", data.reshape(-1, 4), delimiter=",", fmt='%s')

def display_data():
    df = pd.read_csv("blockDataSample.csv")
    gas = np.asarray(df.iloc[:,[3]])
    
    plt.plot(gas)
    plt.show()
    
start_block = 16250000
end_block = 16450000
extract_data(start_block, end_block)
