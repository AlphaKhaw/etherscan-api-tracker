import requests
import pandas as pd
from etherscan import Etherscan

class ETH:
    def __init__(self, eth_address, api_key):
        self.eth = Etherscan(api_key)
        self.address = eth_address
        self.url = "https://api.exchangerate-api.com/v4/latest/SGD"
        self.currency_api = requests.get(self.url).json()
        self.currency_data = self.currency_api['rates']
        self.block_no = []
        self.unix_timestamp = []
        self.hash_ = []
        self.nonce = []
        self.block_hash = []
        self.txn_index = []
        self.gas = []
        self.gas_price = []
        self.error_status = []
        self.txreceipt_status = []
        self.input_ = []
        self.contract_address = []
        self.cum_gas_used = []
        self.gas_used = []
        self.confirmations = []
        
    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'SGD':
            amount = float(amount) / self.currency_data[from_currency]
        amount = round(amount * self.currency_data[to_currency], 2) 
        return amount
    
    def convert_wei_to_eth(self, amount):
        amount = float(amount)/pow(10, 18)
        return amount
    
    def convert_gwei_to_eth(self, amount):
        amount = float(amount)/pow(10, 9)
        return amount
    
    def get_balance(self):
        eth_balance = self.eth.get_eth_balance(self.address)
        eth_balance = self.convert_wei_to_eth(eth_balance)
        print(f'{eth_balance:.2f} Ether')
    
    # sort = 'asc'/ 'desc'
    def get_normal_txs(self, first_block, last_block, sort='asc'):
        eth_normal_txs = self.eth.get_normal_txs_by_address(self.address, first_block, last_block, sort=sort)

        for n, transaction in enumerate(eth_normal_txs):
            self.block_no.append(transaction.get('blockNumber'))
            self.unix_timestamp.append(transaction.get('timeStamp'))
            self.hash_.append(transaction.get('hash'))
            self.nonce.append(transaction.get('nonce'))
            self.block_hash.append(transaction.get('blockHash'))
            self.txn_index.append(transaction.get('transactionIndex'))
            self.gas.append(transaction.get('gas'))
            self.gas_price.append(transaction.get('gasPrice'))
            self.error_status.append(transaction.get('isError'))
            self.txreceipt_status.append(transaction.get('txreceipt_status'))
            self.input_.append(transaction.get('input'))
            self.contract_address.append(transaction.get('contractAddress'))
            self.cum_gas_used.append(transaction.get('cumulativeGasUsed'))
            self.gas_used.append(transaction.get('gasUsed'))
            self.confirmations.append(transaction.get('confirmations'))
        
        self.datetime = [pd.to_datetime(value, unit='s') for value in self.unix_timestamp]
        
        self.normal_txs_df = pd.DataFrame({'Block Number': self.block_no,
                                          'UnixTimeStamp': self.unix_timestamp,
                                          'DateTime': self.datetime,
                                          'Transaction Hash': self.hash_,
                                          'Nonce': self.nonce,
                                          'Block Hash': self.block_hash,
                                          'Transaction Index': self.txn_index,
                                          'Gas': self.gas,
                                          'Gas Price': self.gas_price,
                                          'Error Status': self.error_status,
                                          'Transaction Receipt Status': self.txreceipt_status,
                                          'Input': self.input_,
                                          'Contract Address': self.contract_address,
                                          'Gas Used': self.gas_used,
                                          'Cumulative Gas Used': self.cum_gas_used,
                                          'Confirmations': self.confirmations
                                     })
              
        return self.normal_txs_df
    
    def get_internal_txs_by_address(self, first_block, last_block, sort='asc'):
        try:
            self.eth_internal_txs = self.eth.get_internal_txs_by_address(self.address, first_block, last_block, sort=sort)
        except AssertionError:
            print('No internal transactions found')
    
    def get_gas_price(self):
        gas_oracle = self.eth.get_gas_oracle()
        safe_gas = gas_oracle["SafeGasPrice"]  
        propose_gas = gas_oracle["ProposeGasPrice"]  
        fast_gas = gas_oracle["FastGasPrice"]
        
        safe_gas_eth = self.convert_gwei_to_eth(safe_gas)
        propose_gas_eth = self.convert_gwei_to_eth(propose_gas)
        fast_gas_eth = self.convert_gwei_to_eth(fast_gas)
        
        safe_message = f'Safe: {safe_gas} Gwei / {safe_gas_eth} Ether'
        propose_message = f'Propose: {propose_gas} Gwei / {propose_gas_eth} Ether'
        fast_message = f'Fast: {fast_gas} Gwei / {fast_gas_eth} Ether'

        print(f'{safe_message}\n{propose_message}\n{fast_message}')        
    
    def get_last_price(self):
        self.last_price = self.eth.get_eth_last_price()
        self.last_price_timestamp = pd.to_datetime(self.last_price['ethusd_timestamp'], unit='s')
        self.eth_usd_price = self.last_price['ethusd']
        self.eth_sgd_price = self.convert('USD', 'SGD', self.eth_usd_price)
        
        print(f'At {self.last_price_timestamp}, the price of Ethereum is USD {self.eth_usd_price}/SGD {self.eth_sgd_price:.2f}.')
