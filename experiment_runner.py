import time
import psutil
import os
from apriori import Apriori, BitwiseVerticalFIM, BitwiseVerticalFIMOptimized
from dataset_loader import DatasetLoader
import json


class ExperimentRunner:
    def __init__(self, dataset_path: str, dataset_name: str, min_sup_values: list):
        self.dataset_path = dataset_path
        self.dataset_name = dataset_name
        self.min_sup_values = min_sup_values
        self.dataset = None
        self.results = {}
    
    def load_dataset(self):
        """Load the dataset"""
        print(f"Loading dataset from {self.dataset_path}...")
        self.dataset = DatasetLoader.load_dataset(self.dataset_path)
        
        if not self.dataset:
            print(f"Failed to load dataset: {self.dataset_path}")
            return False
        
        info = DatasetLoader.get_dataset_info(self.dataset)
        print(f"Dataset loaded successfully")
        print(f"Transactions: {info.get('transaction_count', 0)}")
        print(f"Unique Items: {info.get('unique_items', 0)}")
        print(f"Avg Transaction Size: {info.get('avg_transaction_size', 0)}")
        print()
        
        return True
    
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)
    
    def run_apriori(self, min_sup):
        """Run Apriori algorithm and collect metrics"""
        mem_before = self.get_memory_usage()
        start_time = time.time()
        
        apriori = Apriori(self.dataset, min_sup)
        frequent_itemsets = apriori.mine()
        
        end_time = time.time()
        mem_after = self.get_memory_usage()
        
        execution_time = end_time - start_time
        memory_used = max(0, mem_after - mem_before)
        num_itemsets = len(frequent_itemsets)
        num_candidates = apriori.candidates_generated
        
        return {
            'execution_time': execution_time,
            'memory_used': memory_used,
            'num_itemsets': num_itemsets,
            'num_candidates': num_candidates
        }
    
    def run_bitwise(self, min_sup):
        """Run Bitwise Vertical FIM algorithm and collect metrics"""
        mem_before = self.get_memory_usage()
        start_time = time.time()
        
        bitwise = BitwiseVerticalFIM(self.dataset, min_sup)
        frequent_itemsets = bitwise.mine()
        
        end_time = time.time()
        mem_after = self.get_memory_usage()
        
        execution_time = end_time - start_time
        memory_used = max(0, mem_after - mem_before)
        num_itemsets = len(frequent_itemsets)
        num_candidates = bitwise.candidates_generated
        
        return {
            'execution_time': execution_time,
            'memory_used': memory_used,
            'num_itemsets': num_itemsets,
            'num_candidates': num_candidates
        }
    
    def run_bitwise_optimized(self, min_sup):
        """Run optimized Bitwise algorithm with multi-threading"""
        mem_before = self.get_memory_usage()
        start_time = time.time()
        
        bitwise_opt = BitwiseVerticalFIMOptimized(self.dataset, min_sup)
        frequent_itemsets = bitwise_opt.mine()
        
        end_time = time.time()
        mem_after = self.get_memory_usage()
        
        execution_time = end_time - start_time
        memory_used = max(0, mem_after - mem_before)
        num_itemsets = len(frequent_itemsets)
        num_candidates = bitwise_opt.candidates_generated
        
        return {
            'execution_time': execution_time,
            'memory_used': memory_used,
            'num_itemsets': num_itemsets,
            'num_candidates': num_candidates
        }
    
    def run_experiments(self, num_runs=3):
        """Run all experiments with specified number of runs"""
        print(f"Running experiments on {self.dataset_name} dataset")
        print(f"Number of runs per configuration: {num_runs}")
        print("=" * 80)
        
        results_by_minsup = {}
        
        for min_sup in self.min_sup_values:
            print(f"\nMinimum Support: {min_sup} ({int(min_sup * 100)}%)")
            print("-" * 80)
            
            apriori_results = []
            bitwise_results = []
            bitwise_opt_results = []
            
            for run in range(num_runs):
                print(f"  Run {run + 1}/{num_runs}...")
                
                apriori_res = self.run_apriori(min_sup)
                print(f"    - Apriori finished in {apriori_res['execution_time']:.2f}s")
                apriori_results.append(apriori_res)
                
                bitwise_res = self.run_bitwise(min_sup)
                print(f"    - Bitwise finished in {bitwise_res['execution_time']:.2f}s")
                bitwise_results.append(bitwise_res)
                
                bitwise_opt_res = self.run_bitwise_optimized(min_sup)
                print(f"    - Bitwise Opt finished in {bitwise_opt_res['execution_time']:.2f}s")
                bitwise_opt_results.append(bitwise_opt_res)
            
            avg_apriori = self._average_results(apriori_results)
            avg_bitwise = self._average_results(bitwise_results)
            avg_bitwise_opt = self._average_results(bitwise_opt_results)
            
            speedup = avg_apriori['execution_time'] / max(avg_bitwise_opt['execution_time'], 0.0001)
            
            results_by_minsup[min_sup] = {
                'apriori': avg_apriori,
                'bitwise': avg_bitwise,
                'bitwise_optimized': avg_bitwise_opt,
                'speedup': speedup
            }
            
            print(f"\nApriori Results:")
            print(f"  Execution Time: {avg_apriori['execution_time']:.4f} seconds")
            print(f"  Memory Used: {avg_apriori['memory_used']:.2f} MB")
            print(f"  Frequent Itemsets: {avg_apriori['num_itemsets']}")
            print(f"  Candidates Generated: {avg_apriori['num_candidates']}")
            
            print(f"\nBitwise Vertical FIM Results:")
            print(f"  Execution Time: {avg_bitwise['execution_time']:.4f} seconds")
            print(f"  Memory Used: {avg_bitwise['memory_used']:.2f} MB")
            print(f"  Frequent Itemsets: {avg_bitwise['num_itemsets']}")
            print(f"  Candidates Generated: {avg_bitwise['num_candidates']}")
            
            print(f"\nOptimized Bitwise Vertical FIM Results:")
            print(f"  Execution Time: {avg_bitwise_opt['execution_time']:.4f} seconds")
            print(f"  Memory Used: {avg_bitwise_opt['memory_used']:.2f} MB")
            print(f"  Frequent Itemsets: {avg_bitwise_opt['num_itemsets']}")
            print(f"  Candidates Generated: {avg_bitwise_opt['num_candidates']}")
            
            print(f"\nSpeedup (Apriori / Optimized Bitwise): {speedup:.2f}x")
        
        self.results = results_by_minsup
        return results_by_minsup
    
    @staticmethod
    def _average_results(results_list):
        """Average results from multiple runs"""
        if not results_list:
            return {}
        
        avg_time = sum(r['execution_time'] for r in results_list) / len(results_list)
        avg_memory = sum(r['memory_used'] for r in results_list) / len(results_list)
        num_itemsets = results_list[0]['num_itemsets']
        num_candidates = results_list[0]['num_candidates']
        
        return {
            'execution_time': avg_time,
            'memory_used': avg_memory,
            'num_itemsets': num_itemsets,
            'num_candidates': num_candidates
        }
    
    def save_results(self, output_file):
        """Save results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\nResults saved to {output_file}")


def main():
    """Main experiment runner"""
    
    base_path = "d:/GIKI/SEMESTER 06/Design and Analysis of Algorithm/DA Prj"
    
    datasets = [
        {
            'path': os.path.join(base_path, 'chess.dat'),
            'name': 'Chess'
        },
        {
            'path': os.path.join(base_path, 'connect.dat'),
            'name': 'Connect'
        },
        {
            'path': os.path.join(base_path, 'accidents.dat'),
            'name': 'Accidents'
        }
    ]
    
    min_sup_thresholds = [0.7, 0.75, 0.8, 0.85, 0.9]  # Adjusted thresholds to avoid exponentially long runtimes on dense python sets
    
    all_results = {}
    
    for dataset_info in datasets:
        dataset_path = dataset_info['path']
        dataset_name = dataset_info['name']
        
        if not os.path.exists(dataset_path):
            print(f"Dataset file not found: {dataset_path}")
            print(f"Skipping {dataset_name} dataset")
            print()
            continue
        
        runner = ExperimentRunner(dataset_path, dataset_name, min_sup_thresholds)
        
        if runner.load_dataset():
            results = runner.run_experiments(num_runs=1)
            all_results[dataset_name] = results
            
            output_file = os.path.join(base_path, f"results_{dataset_name.lower()}.json")
            runner.save_results(output_file)
        
        print("\n" + "=" * 80 + "\n")
    
    print("All experiments completed successfully!")


if __name__ == "__main__":
    main()
