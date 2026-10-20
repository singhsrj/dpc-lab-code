import json
import time
import sys
import math

N = 5

def load_seed(path):
    with open(path) as f:
        return json.load(f)

def align_clocks(clocks, theta):
    T0 = clocks[0]
    trusted = [i for i in range(N) if abs(clocks[i] - T0) <= theta]
    Ttarget = math.floor(sum(clocks[i] for i in trusted) / len(trusted))
    deltas = [Ttarget - clocks[i] if i in trusted else 0 for i in range(N)]
    synced = [clocks[i] + deltas[i] for i in range(N)]
    return trusted, Ttarget, deltas, synced

def can_deliver(v_msg, Vi, sender):
    if v_msg[sender] != Vi[sender] + 1:
        return False
    for k in range(N):
        if k != sender and v_msg[k] > Vi[k]:
            return False
    return True

def process_message(msg, Vi):
    v_msg = msg["v_msg"]
    for k in range(N):
        Vi[k] = max(Vi[k], v_msg[k])

def drain_buffer(buffer, Vi):
    changed = True
    released = []
    while changed:
        changed = False
        remaining = []
        for msg in buffer:
            if can_deliver(msg["v_msg"], Vi, msg["sender"]):
                process_message(msg, Vi)
                released.append(msg)
                changed = True
            else:
                remaining.append(msg)
        buffer[:] = remaining
    return released

def compute_payload(T_sync, Vi):
    return (T_sync * sum(Vi)) % 9973



def print_step(label, content="", delay=0.05):
    print(f"  {label}", end="")
    if content:
        print(f"  {content}", end="")
    print()
    time.sleep(delay)

def run(seed_path):
    data = load_seed(seed_path)
    theta = data["theta"]
    clocks = data["clocks"]
    queues = [list(q) for q in data["queues"]]

    print("  PROJECT CHRONOS — Distributed Clock Sync & Causal Ordering")
    time.sleep(0.3)

    print()
    print("  INITIAL STATE")
    for i in range(N):
        print_step(f"Node {i}  clock={clocks[i]:>6}  VC={[0]*N}", delay=0.08)
    print_step(f"θ (tolerance) = {theta}", delay=0.1)
    print()

    print("  STEP 1 — CLOCK ALIGNMENT  (Node 0 is coordinator)")

    time.sleep(0.2)

    trusted, Ttarget, deltas, synced = align_clocks(clocks, theta)

    print()
    print_step(f"Node 0 clock  T0 = {clocks[0]}", delay=0.1)
    time.sleep(0.1)

    for i in range(N):
        diff = abs(clocks[i] - clocks[0])
        verdict = "TRUSTED" if i in trusted else "EXCLUDED"
        print_step(f"Node {i}  |T{i} - T0| = |{clocks[i]} - {clocks[0]}| = {diff:>5}  →  {verdict}", delay=0.09)

    time.sleep(0.15)
    print()
    trusted_clocks_sum = sum(clocks[i] for i in trusted)
    print_step(f"Trusted set S = {trusted}")
    print_step(f"Sum of trusted clocks = {trusted_clocks_sum}")
    print_step(f"Ttarget = floor({trusted_clocks_sum} / {len(trusted)}) = {Ttarget}")
    time.sleep(0.1)

    print()
    for i in range(N):
        tag = "(ignored)" if i not in trusted else ""
        print_step(f"Node {i}  δ{i} = {Ttarget} - {clocks[i]} = {deltas[i]:>+6}  →  T_sync = {synced[i]}  {tag}", delay=0.09)

    print()
    print("  STEP 2 — CAUSAL MESSAGE ORDERING")
    time.sleep(0.2)

    vector_clocks = [[0] * N for _ in range(N)]
    buffers = [[] for _ in range(N)]
    processed_counts = [0] * N

    for i in range(N):
        print()
        
        print(f"  Node {i} — processing queue ({len(queues[i])} messages)")
        
        time.sleep(0.1)

        queue = list(queues[i])
        Vi = vector_clocks[i]

        for msg in queue:
            sender = msg["sender"]
            v_msg = msg["v_msg"]
            time.sleep(0.12)

            if can_deliver(v_msg, Vi, sender):
                process_message(msg, Vi)
                processed_counts[i] += 1
                print_step(f"  DELIVER  from={sender}  v_msg={v_msg}  VC={Vi}", delay=0.05)

                released = drain_buffer(buffers[i], Vi)
                for r in released:
                    processed_counts[i] += 1
                    print_step(f"  RELEASE  from={r['sender']}  v_msg={r['v_msg']}  VC={Vi}  (was buffered)", delay=0.05)
            else:
                buffers[i].append(msg)
                print_step(f"  BUFFER   from={sender}  v_msg={v_msg}  (causal gap)", delay=0.05)

        if buffers[i]:
            print_step(f"  WARNING  {len(buffers[i])} message(s) remain in buffer (unresolvable)", delay=0.05)

        print_step(f"  Final VC = {Vi}", delay=0.05)

    print()
    print("  STEP 3 — FINAL PAYLOAD COMPUTATION")
    time.sleep(0.2)
    print()

    payloads = []
    for i in range(N):
        Vi = vector_clocks[i]
        T_sync = synced[i]
        Pi = compute_payload(T_sync, Vi)
        payloads.append(Pi)
        vc_sum = sum(Vi)
        print_step(
            f"Node {i}  T_sync={T_sync}  VC_sum={vc_sum}"
            f"  P{i} = ({T_sync} × {vc_sum}) mod 9973 = {Pi}",
            delay=0.1
        )

    print()
    print("  SUMMARY")
    time.sleep(0.1)
    print()

    for i in range(N):
        status = "trusted " if i in trusted else "excluded"
        print_step(
            f"Node {i}  [{status}]"
            f"  clock {clocks[i]:>5} → {synced[i]:>5}"
            f"  VC={vector_clocks[i]}"
            f"  payload={payloads[i]}",
            delay=0.07
        )

if __name__ == "__main__":
    path = "lab8\seed.json"
    run(path)