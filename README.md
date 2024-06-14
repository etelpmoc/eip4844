# eip4844
This repository is dedicated to the empirical analysis of the impacts of the EIP 4844 upgrade. The code was used in the study titled ["Impact of EIP-4844 on Ethereum: Consensus Security, Ethereum Usage, Rollup Transaction Dynamics, and Blob Gas Fee Markets"](https://arxiv.org/abs/2405.03183).

## Prerequisites
- python 3.12.2

> We have collected log from prysm node before and after the Ethereum upgrade and stored it in MongoDB for use. The data upload is still in progress.


## Directory Structure

**Analysis:** Code for data analysis

- **4_1_consensus_security**: Analyzes factors such as receive time, sync time, CSP time, and DA time to investigate the impact of EIP 4844 on consensus security.
- **4_2_ethereum_usage**: Analyzes the Ethereum usage before and after EIP 4844, including the amount of data posted, amount of fee paid, price of posting 1MiB, and gas used.
- **4_3_rollup_transactions**: Analyzes changes in rollup transaction volume and delays to understand the activity changes caused by EIP 4844.
- **4_4_blob_gas_analysis**: Analyzes blob gas fees to understand the dynamics of the blob gas fee market.

**Crawler:** Code for data crawling from various sources(specified in the code).
