import subprocess

def create_election_cli(election_id, candidates_file, user_keys_file, pk_file, sk_file, start_time, end_time):
    cmd = [
        "python3", "cli.py", "create-election",
        str(election_id),
        candidates_file,
        user_keys_file,
        pk_file,
        sk_file,
        start_time,
        end_time
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Election {election_id} output:\n{result.stdout}")
    if result.stderr:
        print(f"Error:\n{result.stderr}")

if __name__ == "__main__":
    # Example file paths, adjust as needed
    candidates_file = "sample_data/candidates.txt"
    user_keys_file = "sample_data/user_keys.txt"
    pk_file = "keys/example_pub2.pem"
    sk_file = "keys/example2.pem"
    start_time = "2025-08-30T09:00:00Z"
    end_time = "2025-08-30T17:00:00Z"

    for eid in range(2, 5):
        create_election_cli(
            eid,
            candidates_file,
            user_keys_file,
            pk_file,
            sk_file,
            start_time,
            end_time
        )