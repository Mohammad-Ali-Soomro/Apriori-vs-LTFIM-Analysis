import json
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_results(json_files, output_prefix=""):
    for json_file in json_files:
        if not os.path.exists(json_file):
            continue
            
        with open(json_file, 'r') as f:
            data = json.load(f)
            
        supports = sorted([float(k) for k in data.keys()])
        
        apriori_times = [data[str(s)]['apriori']['execution_time'] for s in supports]
        bitwise_times = [data[str(s)]['bitwise']['execution_time'] for s in supports]
        bitwise_opt_times = [data[str(s)]['bitwise_optimized']['execution_time'] for s in supports]
        
        dataset_name = os.path.basename(json_file).replace('results_', '').replace('.json', '').capitalize()
        
        # Plot Execution Time
        plt.figure(figsize=(10, 6))
        plt.plot(supports, apriori_times, marker='o', linewidth=2, label='Apriori')
        plt.plot(supports, bitwise_times, marker='s', linewidth=2, label='Bitwise')
        plt.plot(supports, bitwise_opt_times, marker='^', linewidth=2, label='Bitwise Optimized')
        
        plt.title(f'Execution Time vs Minimum Support ({dataset_name})')
        plt.xlabel('Minimum Support Threshold')
        plt.ylabel('Execution Time (seconds)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{output_prefix}time_{dataset_name.lower()}.png', dpi=300)
        plt.close()
        
        # Plot Speedup
        speedups = [data[str(s)]['speedup'] for s in supports]
        plt.figure(figsize=(10, 6))
        plt.plot(supports, speedups, marker='D', linewidth=2, color='purple', label='Speedup (Apriori/Bitwise Opt)')
        plt.axhline(y=1, color='r', linestyle='-', alpha=0.3)
        plt.title(f'Speedup vs Minimum Support ({dataset_name})')
        plt.xlabel('Minimum Support Threshold')
        plt.ylabel('Speedup Factor')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{output_prefix}speedup_{dataset_name.lower()}.png', dpi=300)
        plt.close()

if __name__ == "__main__":
    base_path = "d:/GIKI/SEMESTER 06/Design and Analysis of Algorithm/DA Prj"
    json_files = [
        os.path.join(base_path, "results_chess.json"),
        os.path.join(base_path, "results_connect.json"),
        os.path.join(base_path, "results_accidents.json")
    ]
    plot_results(json_files, os.path.join(base_path, ""))
    print("Plots generated successfully.")
