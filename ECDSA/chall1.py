#!/usr/bin/env python3
"""ECDSA Nonce Reuse Challenge"""

import json
import hashlib
import secrets
from ecdsa import SECP256k1
from ecdsa.numbertheory import inverse_mod

CURVE = SECP256k1
ORDER = CURVE.order
G = CURVE.generator

def hash_msg(msg: str) -> int:
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)

def sign(sk: int, msg: str, nonce: int = None) -> tuple:
    if nonce is None:
        nonce = secrets.randbelow(ORDER - 1) + 1
    e = hash_msg(msg) % ORDER
    R = nonce * G
    r = R.x() % ORDER
    s = (inverse_mod(nonce, ORDER) * (e + sk * r)) % ORDER
    return (r, s)

def verify(pk, msg: str, r: int, s: int) -> bool:
    e = hash_msg(msg) % ORDER
    w = inverse_mod(s, ORDER)
    R = (e * w % ORDER) * G + (r * w % ORDER) * pk
    return R.x() % ORDER == r

def make_msg(f, t, v):
    return json.dumps({"from": f, "to": t, "value": v}, sort_keys=True)

# === Setup Users ===
users = {
    "Alice":   {"sk": secrets.randbelow(ORDER-1)+1, "balance": 10000},
    "Bob":     {"sk": secrets.randbelow(ORDER-1)+1, "balance": 500},
    "Charlie": {"sk": secrets.randbelow(ORDER-1)+1, "balance": 200},
}
for u in users.values():
    u["pk"] = u["sk"] * G

# === Transaction Pool ===
alice_nonce = secrets.randbelow(ORDER-1)+1  # Reused!

pool = [
    ("Alice", "Bob", 100, sign(users["Alice"]["sk"], make_msg("Alice", "Bob", 100), alice_nonce)),
    ("Bob", "Charlie", 50, sign(users["Bob"]["sk"], make_msg("Bob", "Charlie", 50))),
    ("Alice", "Charlie", 200, sign(users["Alice"]["sk"], make_msg("Alice", "Charlie", 200), alice_nonce)),
    ("Charlie", "Bob", 30, sign(users["Charlie"]["sk"], make_msg("Charlie", "Bob", 30))),
]

# Process
for (f, t, v, _) in pool:
    users[f]["balance"] -= v
    users[t]["balance"] += v

# === Display ===
print("=" * 80)
print("ECDSA Nonce Reuse Challenge")
print("=" * 80)
print()
print("[You are Bob]")
print(f"  Your secret key: {hex(users['Bob']['sk'])}")
print()
print("[Balances]")
for name, u in users.items():
    print(f"  {name}: ${u['balance']}")
print()
print("[Transaction Pool]")
for i, (f, t, v, (r, s)) in enumerate(pool):
    print(f"TX[{i}]: {f} -> {t}, value={v}")
    print(f"  r = {hex(r)}")
    print(f"  s = {hex(s)}")
    print()

print("[Commands]")
print("  send   - Send money as Bob (practice signing)")
print("  attack - Submit forged transaction as Alice")
print("  balance - Show balances")
print("  quit   - Exit")
print()
print("[Goal] Steal Alice's ${} !".format(users["Alice"]["balance"]))
print()

# === Interactive ===
while True:
    cmd = input("> ").strip().lower()
    
    if cmd == "quit":
        break
    
    elif cmd == "balance":
        for name, u in users.items():
            print(f"  {name}: ${u['balance']}")
    
    elif cmd == "send":
        try:
            to = input("  to: ").strip()
            value = int(input("  value: "))
            
            if to not in users:
                users[to] = {"balance": 0, "pk": None}
            
            if users["Bob"]["balance"] < value:
                print("  [FAIL] Insufficient balance")
                continue
            
            msg = make_msg("Bob", to, value)
            r, s = sign(users["Bob"]["sk"], msg)
            
            print(f"  [Signed] r = {hex(r)}")
            print(f"           s = {hex(s)}")
            
            if verify(users["Bob"]["pk"], msg, r, s):
                users["Bob"]["balance"] -= value
                users[to]["balance"] += value
                print(f"  [OK] Bob -> {to}: ${value}")
                print(f"  Bob: ${users['Bob']['balance']}, {to}: ${users[to]['balance']}")
            else:
                print("  [FAIL] Invalid signature")
        except Exception as e:
            print(f"  [ERROR] {e}")
    
    elif cmd == "attack":
        try:
            to = input("  to: ").strip()
            value = int(input("  value: "))
            r = int(input("  r: "), 16)
            s = int(input("  s: "), 16)
            
            if to not in users:
                users[to] = {"balance": 0, "pk": None}
            
            msg = make_msg("Alice", to, value)
            
            if verify(users["Alice"]["pk"], msg, r, s) and users["Alice"]["balance"] >= value:
                users["Alice"]["balance"] -= value
                users[to]["balance"] += value
                print(f"  [OK] Alice -> {to}: ${value}")
                print(f"  Alice: ${users['Alice']['balance']}, {to}: ${users[to]['balance']}")
                if users["Alice"]["balance"] == 0:
                    print()
                    print("  " + "=" * 40)
                    print("  🎉 YOU WIN! Alice's funds stolen!")
                    print("  " + "=" * 40)
            else:
                print("  [FAIL] Invalid signature or insufficient balance")
        except Exception as e:
            print(f"  [ERROR] {e}")
    
    else:
        print("  Unknown command. Try: send, attack, balance, quit")
