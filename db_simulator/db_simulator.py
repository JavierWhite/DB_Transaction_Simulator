#!/usr/bin/env python3
import argparse
from sim_engine import SimulationEngine

def parse_args():
    parser = argparse.ArgumentParser(description='Database Simulator')
    parser.add_argument('max_cycles', type=int)
    parser.add_argument('tx_size', type=int)
    parser.add_argument('start_prob', type=float)
    parser.add_argument('write_prob', type=float)
    parser.add_argument('rollback_prob', type=float)
    parser.add_argument('timeout', type=int)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    sim = SimulationEngine(args)
    sim.run()
    