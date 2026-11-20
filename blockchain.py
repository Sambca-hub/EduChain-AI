
import hashlib
import json
import os
from datetime import datetime, timezone

LEDGER_PATH = "data/blockchain_ledger.json"


class EducationBlockchain:
    def __init__(self, ledger_path=LEDGER_PATH):
        self.ledger_path = ledger_path
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)

        if not os.path.exists(self.ledger_path):
            self._save([])

    def _load(self):
        try:
            with open(self.ledger_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, chain):
        with open(self.ledger_path, "w", encoding="utf-8") as file:
            json.dump(chain, file, indent=4)

    @staticmethod
    def calculate_hash(block):
        block_data = {
            key: value
            for key, value in block.items()
            if key != "hash"
        }

        encoded = json.dumps(
            block_data,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def add_record(self, student_id, recommendations):
        chain = self._load()

        previous_hash = (
            chain[-1]["hash"] if chain else "0" * 64
        )

        block = {
            "index": len(chain) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "student_id": str(student_id),
            "recommendations": recommendations,
            "previous_hash": previous_hash
        }

        block["hash"] = self.calculate_hash(block)

        chain.append(block)
        self._save(chain)

        return block

    def get_chain(self):
        return self._load()

    def verify_chain(self):
        chain = self._load()

        if not chain:
            return True, "Blockchain is empty. No integrity issues found."

        for index, block in enumerate(chain):
            if block.get("index") != index + 1:
                return False, f"Invalid block index at block {index + 1}."

            if block.get("hash") != self.calculate_hash(block):
                return False, f"Block {index + 1} has been modified."

            expected_previous = (
                chain[index - 1]["hash"]
                if index > 0
                else "0" * 64
            )

            if block.get("previous_hash") != expected_previous:
                return False, f"Broken blockchain link at block {index + 1}."

        return True, "All blockchain records are valid."

    def get_total_blocks(self):
        return len(self._load())
