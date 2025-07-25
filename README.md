# eip4844
This repository contains the code and data used in our study: ["Impact of EIP-4844 on Ethereum: Consensus Security, Ethereum Usage, Rollup Transaction Dynamics, and Blob Gas Fee Markets"](https://arxiv.org/abs/2405.03183). It provides analysis scripts for evaluating Ethereum node logs, rollup activity, and fee market behavior before and after the EIP-4844 upgrade. Users can reproduce all figures in the paper and explore the dataset via the provided tools.

## Prerequisites
- python 3.12.2

## Data
We have collected logs from the prysm node before and after the Ethereum upgrade and stored them in MongoDB. We also have gathered data from various sources such as L2Beats and explorers like Etherscan. The data is available [here](https://drive.google.com/drive/folders/1xwOJiaISzptNMoAefusgmaUtD4rl1dr_?usp=sharing).

Contents include:
- `consensus_logs_pre.json` and `consensus_logs_post.json`: Extracted logs from Prysm validator nodes.
- `ethereum_usage.csv`: Aggregated Ethereum transaction and fee data.
- `rollup_delays.csv`: Timestamped rollup and Ethereum batch submission data.
- `blob_gas_prices.csv`: Blob gas base and priority fee time series.

## Directory Structure

**Analysis:** Code for data analysis

- **4_1_consensus_security**: Analyzes factors such as receive time, sync time, CSP time, and DA time to investigate the impact of EIP 4844 on consensus security.
- **4_2_ethereum_usage**: Analyzes the Ethereum usage before and after EIP 4844, including the amount of data posted, amount of fee paid, price of posting 1MiB, and gas used.
- **4_3_rollup_transactions**: Analyzes changes in rollup transaction volume and delays to understand the activity changes caused by EIP 4844.
- **4_4_blob_gas_analysis**: Analyzes blob gas fees to understand the dynamics of the blob gas fee market.

**Crawler:** Code for crawling Ethereum data, rollup data from various sources (specified in the code).
