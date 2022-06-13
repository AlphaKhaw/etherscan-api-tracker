<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/AlphaKhaw/etherscan-api-tracker">
    <img src="https://user-images.githubusercontent.com/87654386/173388852-3ed95b8b-3b9b-4d25-9f8f-8cc5264f9402.png" alt="Logo" width="350" height="80">
  </a>

<h3 align="center">Etherscan API Tracker</h3>

  <p align="center">
    A github repository utilising Etherscan API to build a Ethereum address tracker
    <br />
    <a href="https://github.com/AlphaKhaw/etherscan-api-tracker"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/AlphaKhaw/etherscan-api-tracker">View Demo</a>
    ·
    <a href="https://github.com/AlphaKhaw/etherscan-api-tracker/issues">Report Bug</a>
    ·
    <a href="https://github.com/AlphaKhaw/etherscan-api-tracker/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#main-packages-utilised">Main Packages Utilised</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

<!--[![Product Name Screen Shot][product-screenshot]](https://example.com) --> 

This project aims to utilise Etherscan API and webscraping techniques to build a tracker for Ethereum address(es). Currently, this repository contains two Python 
scripts - `eth_etherscan.py` and `etherscan_api_methods.py`. User can utilise this repository to keep track of their personal Ethereum cryptocurrency portfolio. 

### Built with

* [Etherscan API](https://docs.etherscan.io/)

<p align="right">(<a href="#top">back to top</a>)</p>

### Main Packages Utilised

* [Selenium with Python](https://selenium-python.readthedocs.io/)
* [Pandas](https://pandas.pydata.org/docs/reference/index.html)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

![etherscan-api-plans](https://user-images.githubusercontent.com/87654386/173401884-1f6ca9d4-6a0b-4cfb-8472-ebf84af82228.png)

- Free API Key at - [https://etherscan.io/apis](https://etherscan.io/apis)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

| `etherscan_api_methods.py` - Referencing the Etherscan API documentation, this script contains methods with respect to the relevant API endpoints 
(eg. Accounts - Get Ether Balance for a Single Address | Gas Tracker - Get Gas Oracle). This script can be used to get the general information about Ethereum token and 
Ethereum address(es). 

- Code with required input arguments to initialise ETH class: 
 ```py
if __name__ == '__main__':
    eth = ETH(eth_address=ETH_ADDRESS, api_key=API_KEY)
   ```

| `eth_etherscan.py` - This script combines class methods from `etherscan_api_methods.py` and webscraping to obtain additional information about Ethereum address on 
the Etherscan webpage. From the Etherscan webpage, additional information such as receipent's and sender's Public Name Tag. After processing information, user can 
choose to export it as an Excel file for further any processing or data visualisation purposes. All the aforementioned informations are limited to 'Normal'
transactions as defined by Etherscan. 

- Code with required input arguments to initialise ETH class: 
 ```py
if __name__ == '__main__':    
    eth = ETH(path=CHROMEDRIVER_PATH, 
              eth_address=ETH_ADDRESS, 
              api_key=API_KEY)
   ```

_For more examples, please refer to the [Documentation](https://github.com/AlphaKhaw/etherscan-api-tracker)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] Adapting free API Endpoints into `etherscan_api_methods.py` as individual respective methods
- [ ] Expanding beyond 'Normal' transactions
  - [ ] Expand list of transactions to 'ERC20 - Token Transfer Events' - Fungible Tokens
  - [ ] Expand list of transactions to 'ERC721 - Token Transfer Events' - Non-Fungible Tokens
  - [ ] Expand list of transactions to 'Internal' Transactions

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Khaw Jiahao - [Linkedin](https://www.linkedin.com/in/khaw-jia-hao-65832217b/) - alphakhaw@gmail.com

Project Link: [https://github.com/AlphaKhaw/etherscan-api-tracker](https://github.com/AlphaKhaw/etherscan-api-tracker")

<p align="right">(<a href="#top">back to top</a>)</p>
