import time
import random
from multiprocessing import Process, Pipe

def calculate_node(node_name, principal, years, conn):
    random.seed(principal)
    amount = float(principal)
    total_days = years * 365
    
    for _ in range(total_days):
        r = 0.07
        b = random.uniform(0.001, 0.009)
        rate_daily = (r + b) / 365.0
        amount *= (1 + rate_daily)
        time.sleep(0.001)
        
    conn.send(amount)
    partner_amount = conn.recv()
    
    final_total = amount + partner_amount
    print(f"Node {node_name} calculated its maturity as: {amount:.2f}")
    print(f"Node {node_name} consensus total: {final_total:.2f}")

if __name__ == '__main__':
    p1 = 4321
    p2 = 8765
    n_years = 1

    conn_a, conn_b = Pipe()

    node_a = Process(target=calculate_node, args=('A', p1, n_years, conn_a))
    node_b = Process(target=calculate_node, args=('B', p2, n_years, conn_b))

    node_a.start()
    node_b.start()

    node_a.join()
    node_b.join()