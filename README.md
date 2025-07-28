# eip4844
This repository contains the code and data used in our study:

["Impact of EIP-4844 on Ethereum: Consensus Security, Ethereum Usage, Rollup Transaction Dynamics, and Blob Gas Fee Markets"](https://arxiv.org/abs/2405.03183). 

It provides analysis scripts for evaluating Ethereum node logs, rollup activity, and fee market behavior before and after the EIP-4844 upgrade. Users can reproduce all figures in the paper and explore the dataset via the provided tools.

## Prerequisites
- Python 3.12.2
- MongoDB 7.0.3
- requirements.txt

## Data
We have collected logs from the prysm node before and after the Ethereum upgrade and stored them in MongoDB. We also have gathered data from various sources such as L2Beats and explorers like Etherscan. The data is available [here](https://drive.google.com/drive/folders/1xwOJiaISzptNMoAefusgmaUtD4rl1dr_?usp=sharing).

This dataset consists of 22 CSV files exported from MongoDB, organized into two primary categories: Consensus Layer Data and Rollup Layer Data. These files support all empirical analyses in our study and enable full reproduction of figures and results.

### Consensus layer data (data/consensus)
This category contains 10 files that capture block-level events, validator behavior, and propagation delays across three geographic regions (Virginia, Singapore, and Paris).

| Filename                                                                                                     | Description                                                                                             |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `ethereum.transactions.csv`                                                                                  | Ethereum transactions including blob and non-blob types, with timestamps and gas usage.             |
| `ethereum.forked_blocks.csv`                                                                                 | List of blocks involved in forks, including slot number, block root, and fork classification.           |
| `ethereum.delay_paris_cl.csv`<br>`ethereum.delay_singapore_cl.csv`<br>`ethereum.delay_virginia_cl.csv`       | Receive and sync time measurements from Prysm validator logs located in Paris, Singapore, and Virginia. |
| `ethereum.delay_blob_paris.csv`<br>`ethereum.delay_blob_singapore.csv`<br>`ethereum.delay_blob_virginia.csv` | Blob propagation delays per region, derived from blob gossip timestamps.                                |
| `ethereum.blocks.csv`                                                                                        | Canonical Ethereum blocks with metadata: slot, proposer index, blob count, DA-related gas usage.        |
| `ethereum.blobs.csv`                                                                                         | Blob-level metadata including slot, size, count, and sender information.                                |
| `ethereum.blob_transactions.csv`                                                                             | Mapping between transactions and their associated blobs, including blob fee components.                 |


### Rollup Layer Data (data/L2/)
This category includes 12 files spanning major rollup networks (Arbitrum, Optimism, Base, Linea, zkSync Era, Starknet). The data is used to compute L1 posting delays, transaction throughput, and gas efficiency.

| Filename                                                                                                                                                                                              | Description                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `ethereum.transactions_rollup.csv`                                                                                                                                                                    | Decoded rollup batch transactions from L1, used to estimate rollup-level activity. |
| `ethereum.slots.csv`                                                                                                                                                                                  | Slot-level metadata used to align rollup submissions with block timing.            |
| `ethereum.arbitrum_l2delay.csv`<br>`ethereum.optimism_l2delay.csv`<br>`ethereum.base_l2delay.csv`<br>`ethereum.linea_l2delay.csv`<br>`ethereum.zksync_l2delay.csv`<br>`ethereum.starknet_l2delay.csv` | Delay between L2 transaction generation and corresponding L1 posting, per rollup.  |
| `ethereum.optimism_blocks.csv`<br>`ethereum.base_blocks.csv`<br>`ethereum.linea_blocks.csv`<br>`ethereum.starknet_tx.csv`                                                                             | Block-level metadata per rollup, including batch size, fee, and submission time.   |


## Directory Structure

**Analysis:** Code for data analysis

- **4_1_consensus_security**: Analyzes factors such as receive time, sync time, CSP time, and DA time to investigate the impact of EIP 4844 on consensus security.
- **4_2_ethereum_usage**: Analyzes the Ethereum usage before and after EIP 4844, including the amount of data posted, amount of fee paid, price of posting 1MiB, and gas used.
- **4_3_rollup_transactions**: Analyzes changes in rollup transaction volume and delays to understand the activity changes caused by EIP 4844.
- **4_4_blob_gas_analysis**: Analyzes blob gas fees to understand the dynamics of the blob gas fee market.

**Crawler:** Code for crawling Ethereum data, rollup data from various sources (specified in the code).

- This is not necessary if you download preprocessed data from above google drive link.
