"""Evidence passport: SHA-256 seal over code + params + results.

Canonical JSON (sorted keys, no floats beyond repr) is hashed, so
any later change to code, parameters, seeds, or results changes
the seal. A headline is allowed only if the data are MEASURED
and the lower confidence bound is positive; here all data are
synthetic and observer-reported, so the headline is always
WITHHELD in this package, by rule, not by judgement.
"""
import hashlib
import json
import pathlib


def sha_file(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def seal(payload, code_files):
    canon = json.dumps(payload, sort_keys=True, default=str)
    h = hashlib.sha256(canon.encode())
    for f in sorted(code_files):
        h.update(sha_file(f).encode())
    return h.hexdigest()


def headline_allowed(data_kind, lower_bound):
    return data_kind == "measured" and lower_bound is not None and lower_bound > 0
