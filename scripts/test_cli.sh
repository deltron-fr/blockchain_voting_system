#!/usr/bin/env bash
set -euo pipefail

# Adjust these key paths if your key filenames differ
PK1="keys/example_pub.pem"
SK1="keys/example.pem"
PK2="keys/example_pub1.pem"
SK2="keys/example1.pem"
PK3="keys/exam4_pub.pem"
SK3="keys/exam4.pem"

WORKDIR="$(dirname "$0")/.."
cd "$WORKDIR"

# Prepare candidate file for election 2
CAND_FILE="candidates_e2.txt"
cat > "$CAND_FILE" <<EOF
Alice
Bob
Charlie
EOF

# Prepare user_keys file by SHA256-hashing the PEM public keys (matches hash_pk)
USER_KEYS_FILE="user_keys_e2.txt"
: > "$USER_KEYS_FILE"
for PK in "$PK1" "$PK2" "$PK3"; do
    if [ ! -f "$PK" ]; then
        echo "Missing public key: $PK" >&2
        exit 1
    fi
    sha256sum "$PK" | awk '{print $1}' >> "$USER_KEYS_FILE"
done

echo "Created $CAND_FILE and $USER_KEYS_FILE"

# Create an election (election_id 2) via CLI (times must be ISO with Z allowed)
START="2025-01-01T00:00:00Z"
END="2026-01-01T00:00:00Z"
python3 cli.py create-election 2 "$CAND_FILE" "$USER_KEYS_FILE" "$PK1" "$SK1" "$START" "$END"

# Cast votes via CLI (use the matching public/private key files)
python3 cli.py vote 2 1 "$PK1" "$SK1"
python3 cli.py vote 2 2 "$PK2" "$SK2"
python3 cli.py vote 2 1 "$PK3" "$SK3"

# Optionally create a second election and cast a vote there
CAND_FILE2="candidates_e3.txt"
cat > "$CAND_FILE2" <<EOF
Xavier
Yara
Zoe
EOF

USER_KEYS_FILE2="user_keys_e3.txt"
: > "$USER_KEYS_FILE2"
for PK in "$PK1" "$PK2"; do
    sha256sum "$PK" | awk '{print $1}' >> "$USER_KEYS_FILE2"
done

python3 cli.py create-election 3 "$CAND_FILE2" "$USER_KEYS_FILE2" "$PK1" "$SK1" "$START" "$END"
python3 cli.py vote 3 2 "$PK2" "$SK2"

# Show resulting chain and run main.py to print results
echo -e "\n==== chain.json ===="
jq . chain.json || cat chain.json
