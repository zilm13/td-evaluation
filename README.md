# TOTALDIFFICULTY Evaluation

This set of scripts evaluates precision of TOTALDIFFICULTY computation and votes anomalies using historical Ethereum data.

## Preparing the setup environment

These scripts have dependencies that we need to install. To do this, follow these steps.

Preparing the setup environment on your host:
```shell
apt-get install python3-dev python3-pip python3-venv

# Create, start and install python venv
python -m venv venv 
. venv/bin/activate
pip install -r requirements.txt
```

## Running the script

`python evaluate.py`

`python evaluate_target.py`

 In 2 steps prepares [Ethereum 1.0 data](./blocks_4_mainnet.csv) to simulate any block as anchor for transition start

`python difficulty_growth.py`

Estimates difficulty growth after hash power changes

---

`python votes_1fill_blocks.py`

`python votes_2fill_time.py`

`python votes_3calc_deltas.py`

`python votes_4calc_period.py`

`python votes_5calc_leader.py`

In 5 steps prepares [Ethereum 2.0 data](eth1votes.csv) to be used in votes analysis

---

`python plot.py` 

Plots everything after some code changes
