import logging
import pandas as pd
from tqdm import tqdm
from etherscan import Etherscan

from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


class Webscraping:
    def __init__(self, path, eth_address):
        self.path = path
        self.driver = webdriver.Chrome(executable_path=path)
        self.address = eth_address
        self.first_block = None
        self.last_block = None
        self.method = []
        self.from_address = []
        self.to_address = []
        self.value = []
        self.txn_fee = []
        
        self.load_etherscan()
        self.get_last_block_no()
        self.switch()        
        
    def load_etherscan(self):
        self.driver.get(f"https://etherscan.io/txs?a={self.address}")
    
    def get_last_block_no(self):
        try:
            block_no_element = self.driver.find_element(by=By.XPATH, 
                                                        value="//*[@id='paywall_mask']/table/tbody/tr[1]/td[4]/a").text
        except NoSuchElementException:
            pass
        self.last_block = block_no_element
        
    def switch(self):
        try:
            self.next_element = self.driver.find_element(
                                    by=By.XPATH, 
                                    value='//*[@id="ContentPlaceHolder1_topPageDiv"]/nav/ul/li[4]/span[2]'
                                    )
        except NoSuchElementException:
            pass
        try:
            self.next_element = self.driver.find_element(
                                    by=By.XPATH, 
                                    value='//*[@id="ContentPlaceHolder1_topPageDiv"]/nav/ul/li[4]/a/span[2]'
                                    )
        except NoSuchElementException:
            pass
        
        if self.next_element.text == 'Previous':
            self.get_address_information()
        else:
            self.get_address_information_multiple_page()
    
    def get_address_information(self):
        all_txs = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_all_elements_located((
                                By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr")))
        for tx in tqdm((x+1 for x in range(len(all_txs)))):
            # Get method
            try:
                method_element = self.driver.find_element(
                                     by=By.XPATH, 
                                     value=(f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{tx}]/td[3]/span")
                                     ).get_attribute("data-original-title")
                method_element = method_element.replace('This transaction includes data in the Input Data field which may indicate a message in UTF-8',
                                                        'Transfer (Data)')
                self.method.append(method_element)
            except NoSuchElementException:
                pass

            # Get from address
            try:
                from_element = self.driver.find_element(
                                    by=By.XPATH, 
                                    value=('/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[7]')
                                    ).text
                self.from_address.append(from_element)
            except NoSuchElementException:
                pass
            
            # Get to address
            try:
                to_element = self.driver.find_element(
                                    by=By.XPATH, 
                                    value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[9]/a")
                                    ).text
                self.to_address.append(to_element)
            except NoSuchElementException:
                pass
            # try:
            #     to_element = self.driver.find_element(
            #                     by=By.XPATH, 
            #                     value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[9]/span")
            #                     ).text
            #     self.to_address.append(to_element)
            # except NoSuchElementException:  
            #     pass
            # try:
            #     to_element = self.driver.find_element(
            #                         by=By.XPATH, 
            #                         value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[9]/span/span/a")
            #                         ).text
            #     self.to_address.append(to_element)
            # except NoSuchElementException:
            #     pass
        
            # Get value
            try:
                value_element = self.driver.find_element(
                                    by=By.XPATH, 
                                    value=(f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{tx}]/td[10]")
                                    ).text
                value_element = value_element.replace(",", "").replace(" Ether", "")
                
                self.value.append(value_element)
            except NoSuchElementException:
                pass
            
            # Get txn fee
            try:
                txn_fee_element = self.driver.find_element(
                                    by=By.XPATH, 
                                    value=(f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{tx}]/td[11]/span")
                                    ).text
                self.txn_fee.append(txn_fee_element)
            except NoSuchElementException:
                pass

        self.get_first_block_no()
        
    def get_address_information_multiple_page(self):
        all_txs = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((
                        By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr")))
        
        while self.next_element:
            for tx in tqdm((x+1 for x in range(len(all_txs)))):
                # Get method of transfer
                try:
                    method_element = self.driver.find_element(
                                         by=By.XPATH, 
                                         value=(f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{tx}]/td[3]/span")
                                         ).get_attribute("data-original-title")
                    method_element = method_element.replace('This transaction includes data in the Input Data field which may indicate a message in UTF-8',
                                                            'Transfer (Data)')
                    self.method.append(method_element)
                except NoSuchElementException:
                    pass
            
                # Get from address
                try:
                    from_element = self.driver.find_element(
                                        by=By.XPATH, 
                                        value=('/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[7]')
                                        ).text
                    self.from_address.append(from_element)
                except NoSuchElementException:
                    pass

                # Get to address
                try:
                    to_element = self.driver.find_element(
                                        by=By.XPATH, 
                                        value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[9]/a")
                                        ).text
                    self.to_address.append(to_element)
                except NoSuchElementException:
                    pass
                # try:
                #     to_element = self.driver.find_element(
                #                     by=By.XPATH, 
                #                     value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[9]/span")
                #                     ).text
                #     self.to_address.append(to_element)
                # except NoSuchElementException:  
                #     pass
                # try:
                #     to_element = self.driver.find_element(
                #                         by=By.XPATH, 
                #                         value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr/td[9]/span/span/a")
                #                         ).text
                #     self.to_address.append(to_element)
                # except NoSuchElementException:
                #     pass
                
                # try:
                #     to_element = self.driver.find_element(
                #                     by=By.XPATH, 
                #                     value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[" + 
                #                            str(tx) + "]/td[9]/a")).text
                # except NoSuchElementException:
                #     pass
                
                # try:
                #     to_element = self.driver.find_element(
                #                     by=By.XPATH, 
                #                     value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[" + 
                #                            str(tx) + "]/td[9]/span")).text
                # except NoSuchElementException:
                #     pass
                    
                # try:
                #     to_element = self.driver.find_element(
                #                     by=By.XPATH, 
                #                     value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[" + 
                #                            str(tx) + "]/td[9]/span/a")).text
                # except NoSuchElementException:  
                #     pass
                
                # try:
                #     to_element = self.driver.find_element(
                #                     by=By.XPATH, 
                #                     value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[" + 
                #                            str(tx) + "]/td[9]/span/span/a")).text
                # except NoSuchElementException:
                #     pass
               
                # self.to_address.append(to_element)
            
                # Get value
                try:
                    value_element = self.driver.find_element(
                                        by=By.XPATH, 
                                        value=(f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{tx}]/td[10]")
                                        ).text
                    value_element = value_element.replace(",", "").replace(" Ether", "")
                    self.value.append(value_element)
                except NoSuchElementException:
                    pass                
                
                # Get txn fee
                try:
                    txn_fee_element = self.driver.find_element(
                                        by=By.XPATH, 
                                        value=(f"/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[{tx}]/td[11]/span")
                                        ).text
                    self.txn_fee.append(txn_fee_element)
                except NoSuchElementException:
                    pass                
        
            try:
                next_button = self.driver.find_element(
                                by=By.XPATH, 
                                value=("/html/body/div[1]/main/div[3]/div/div/div[2]/nav/ul/li[4]/a"))
                if next_button:
                    next_button.click()
                    all_txs = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_all_elements_located((
                                By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr")))
            except NoSuchElementException:
                break
        
        self.get_first_block_no()
               
    def get_first_block_no(self):
        all_txs = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((
                        By.XPATH, "/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr")))
        page_len = len(all_txs)
        
        try:
            block_no_element = self.driver.find_element(
                                by=By.XPATH, 
                                value=("/html/body/div[1]/main/div[3]/div/div/div[3]/table/tbody/tr[" + 
                                       str(page_len) + "]/td[4]")).text
        except StaleElementReferenceException:
            pass
        except NoSuchElementException:
            pass
        
        self.first_block = block_no_element
        self.driver.close()
        self.get_web_df()
        
    def get_web_df(self):
        self.web_df = pd.DataFrame({'Method' : self.method[::-1],
                                    'From': self.from_address[::-1],
                                    'To': self.to_address[::-1],
                                    'Value (ETH)': self.value[::-1],
                                    'Txn Fee (ETH)': self.txn_fee[::-1]})
        return self.web_df

class ETH(Webscraping):
    def __init__(self, path, eth_address, api_key):
        super().__init__(path, eth_address)
        self.eth = Etherscan(api_key)
        self.block_no = []
        self.unix_timestamp = []
        self.hash_ = []
        self.nonce = []
        self.block_hash = []
        self.txn_index = []
        self.gas = []
        self.gas_eth = []
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
        
    # sort = 'asc'/ 'desc'
    def get_normal_txs(self, sort='asc'):
        eth_normal_txs = self.eth.get_normal_txs_by_address(self.address, 
                                                            self.first_block, 
                                                            self.last_block, 
                                                            sort)
        # Extract essential columns
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

        # Convert UNIX Time Stamp to Datetime
        self.datetime = [pd.to_datetime(value, unit='s') for value in self.unix_timestamp]
        
        # Convert respective denomination to Ether
        self.gas_eth = [self.convert_gwei_to_eth(value) for value in self.gas]
        self.gas_price_eth = [self.convert_gwei_to_eth(value) for value in self.gas_price]
        self.cum_gas_used_eth = [self.convert_gwei_to_eth(value) for value in self.cum_gas_used]
        self.gas_used_eth = [self.convert_gwei_to_eth(value) for value in self.gas_used]
        
        # Construct DataFrame
        self.normal_txs_df = pd.DataFrame({'Block Number': self.block_no,
                                            'UnixTimeStamp': self.unix_timestamp,
                                            'DateTime': self.datetime,
                                            'Transaction Hash': self.hash_,
                                            'Nonce': self.nonce,
                                            'Block Hash': self.block_hash,
                                            'Transaction Index': self.txn_index,
                                            'Gas': self.gas,
                                            'Gas (ETH)': self.gas_eth,
                                            'Gas Price': self.gas_price,
                                            'Gas Price (ETH)': self.gas_price_eth,
                                            'Error Status': self.error_status,
                                            'Transaction Receipt Status': self.txreceipt_status,
                                            'Input': self.input_,
                                            'Contract Address': self.contract_address,
                                            'Gas Used': self.gas_used,
                                            'Gas Used (ETH)': self.gas_used_eth,
                                            'Cumulative Gas Used': self.cum_gas_used,
                                            'Cumulative Gas Used (ETH)': self.cum_gas_used_eth,
                                            'Confirmations': self.confirmations
                                          })
        
        # Concatenate with DataFrame from webscraping
        self.combined_df = pd.concat([self.normal_txs_df, self.web_df], axis=1)
        
        return self.combined_df

    def output_excel(self, df, file_name):
        file_name += '.xlsx'
        df.to_excel(file_name, index=False)
