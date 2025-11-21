![status](https://img.shields.io/badge/status-in%20progress-yellow)

# Blockchain Voting System

Lightweight prototype of a blockchain-backed voting system. This repository contains a minimal blockchain representation, an on-disk chain (`chain.json`), key handling utilities, vote/election validators, and a CLI for creating elections and casting votes.

## Quick summary

- Language: Python
- Purpose: Demonstrate a simple append-only blockchain for managing elections and votes with signature verification
- Status: In progress (see top badge). Planned future work: decentralization (multiple nodes), removing hard-coded values, better key and config management, tests and CI, and code organization.

## Prerequisites

- Python 3.10+ (features such as typing of built-in generics may be used)
- pip
- (Optional) `jq` for pretty-printing `chain.json` when inspecting results

Optional: create and activate a virtual environment before installing dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

## Project layout and important files

- `block.py` - Block model and serialization/deserialization. A `Block` has a `type` (`create` or `vote`), `prev_hash`, `data`, `nonce`, `timestamp` and `hash`.
- `blockchain.py` - `Blockchain` class that loads/saves `chain.json`, mines blocks (simple proof-of-work), verifies signatures, validates blocks and appends new blocks.
- `keys.py` - Utilities to generate Ed25519 key pairs, sign payloads and verify signatures.
- `users.py` - Helpers for reading keys from disk and hashing public keys with SHA256.
- `validator.py` - Election and vote validation logic (checks voter list, timeframe and double-voting), and verification wrapper that uses `keys.verify_signature`.
- `utils.py` - Helper utilities: payload serialization for signing, load candidates/keys from files, tallying/displaying results.
- `cli.py` - Command-line interface using `click` for creating elections, casting votes, and printing results.
- `main.py` - Minimal FastAPI app shell (work in progress).
- `chain.json` - The on-disk JSON chain (created automatically if missing).
- `scripts/test_cli.sh` - A convenience script that demonstrates creating elections and casting votes using the CLI. Useful for quick local testing.

## High-level design

1. A `create` block contains `election_data` (id, candidates, list of allowed voters, start/end datetimes). The creator signs the election payload and their public key is included with the block.
2. A `vote` block contains a `vote` payload (election_id, candidate_id) and the voter's public key and signature.
3. Each block is verified for signature correctness before being accepted.
4. Basic local proof-of-work (mining) is implemented by `Blockchain.mine_block()` using a leading-zero difficulty metric.
5. The chain is stored in `chain.json` and used by `validator.py` to ensure votes are in the allowed timeframe, are from permitted voters, and no double-voting occurs.

## Important usage examples (CLI)

Note: the repository includes example keys in the `keys/` directory. The example script `scripts/test_cli.sh` shows a full usage flow; you can run that directly (see below). The examples here show equivalent commands.

1) Prepare a file with candidate names (one per line), e.g. `candidates_e2.txt`:

```bash
cat > candidates_e2.txt <<EOF
Alice
Bob
Charlie
EOF
```

2) Prepare a voter file containing the SHA-256 hashes of the voter public key files (one hash per line). Example (re-creates what `scripts/test_cli.sh` does):

```bash
: > user_keys_e2.txt
sha256sum keys/example_pub.pem | awk '{print $1}' >> user_keys_e2.txt
sha256sum keys/example_pub1.pem | awk '{print $1}' >> user_keys_e2.txt
sha256sum keys/exam4_pub.pem | awk '{print $1}' >> user_keys_e2.txt
```

3) Create an election via the CLI:

```bash

python3 cli.py create-election 2 candidates_e2.txt user_keys_e2.txt keys/example_pub.pem keys/example.pem 2025-01-01T00:00:00Z 2026-01-01T00:00:00Z
```

4) Cast votes (example votes using key pairs):

```bash
python3 cli.py vote 2 1 keys/example_pub.pem keys/example.pem
python3 cli.py vote 2 2 keys/example_pub1.pem keys/example1.pem
python3 cli.py vote 2 1 keys/exam4_pub.pem keys/exam4.pem
```

5) Show results (reads `chain.json` and prints tally):

```bash
python3 cli.py results 2
# or to inspect the chain using jq
jq . chain.json
```

6) Quick test script (the repo contains a convenience script that automates the above flow):

```bash
bash scripts/test_cli.sh
```

7) Generating new keys (utility provided in `keys.py`):

```bash
python3 -c "from keys import generate_key_files; generate_key_files()"
# This writes files under 'keys/' named exam5.pem / exam5_pub.pem and writes hashed pk to keys/hashed_pk5.txt
```

## How signing works

- Payloads are serialized using `utils.serialize_payload()` which converts datetimes to strings and then uses canonical JSON (sorted keys) to produce consistent byte sequences for signing.
- Private keys are Ed25519 PEM-encoded keys. Signatures are stored as hex strings in block `data`.
- `keys.verify_signature` is used by `validator.verify_sig` to confirm signatures before blocks are accepted.


## Displaying results

- CLI output: the `cli.py results <election_id>` command reads the chain and prints a human-friendly tally for the given election. This is the simplest way to check vote counts locally.

How results are produced

- The results are derived by scanning `chain.json` for `vote` blocks that reference the target `election_id`, verifying those blocks' signatures and validity via the project's validator utilities, and then tallying votes by `candidate_id`. The implementation lives in `utils.py` (tallying / display helpers) and is used by `cli.py`.

Quick commands

```bash
# Print a readable tally for election ID 2
python3 cli.py results 2

```

## Future extensions


- Decentralization with local nodes (leader mechanism)

	- run multiple local node processes that each maintain a copy of the ledger (`chain.json`). A leader (proposer) is responsible for collecting pending create/vote payloads, assembling them into a block, and proposing the block to the other nodes.

	- Simple leader-based protocol:
		1. Leader collects transaction(block).
		2. Leader broadcasts the proposed block to all peers over a simple HTTP endpoint.
		3. Peers validate the block (signatures, vote validity, prev_hash consistency). If valid, they reply with a signed ACK.
		4. If the leader collects a quorum (majority) of ACKs within a timeout, it broadcasts a commit message and appends the block locally. Peers append on commit receipt.


- Config file for hard-coded values


## Contributing

This project is a prototype. If you'd like to contribute:

- Fork the repo, fix an issue or add a small enhancement, and open a PR.
- Please add tests for any behavior you change.