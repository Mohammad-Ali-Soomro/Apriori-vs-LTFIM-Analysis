"""
Utility to generate LaTeX tables from experimental results
and create visualizations of performance metrics
"""

import json
import os


class ResultsTableGenerator:
    def __init__(self, results_json_file):
        with open(results_json_file, 'r') as f:
            self.results = json.load(f)
    
    def generate_latex_table(self):
        """Generate LaTeX table for inclusion in report"""
        latex_code = """
\\begin{table}[h]
\\centering
\\caption{Execution Time Comparison Across Minimum Support Thresholds}
\\begin{tabular}{|c|c|c|c|c|}
\\hline
\\textbf{Min Support} & \\textbf{Apriori (s)} & \\textbf{Bitwise (s)} & \\textbf{Optimized (s)} & \\textbf{Speedup} \\\\
\\hline
"""
        
        for min_sup in sorted(self.results.keys(), key=float):
            result = self.results[str(min_sup)]
            
            apriori_time = result['apriori']['execution_time']
            bitwise_time = result['bitwise']['execution_time']
            optimized_time = result['bitwise_optimized']['execution_time']
            speedup = result['speedup']
            
            min_sup_str = f"{float(min_sup)*100:.0f}\\%"
            
            latex_code += f"{min_sup_str} & {apriori_time:.4f} & {bitwise_time:.4f} & {optimized_time:.4f} & {speedup:.2f}x \\\\\n"
        
        latex_code += "\\hline\n\\end{tabular}\n\\end{table}\n"
        
        return latex_code
    
    def generate_memory_table(self):
        """Generate LaTeX table for memory consumption"""
        latex_code = """
\\begin{table}[h]
\\centering
\\caption{Memory Consumption Across Minimum Support Thresholds}
\\begin{tabular}{|c|c|c|c|}
\\hline
\\textbf{Min Support} & \\textbf{Apriori (MB)} & \\textbf{Bitwise (MB)} & \\textbf{Optimized (MB)} \\\\
\\hline
"""
        
        for min_sup in sorted(self.results.keys(), key=float):
            result = self.results[str(min_sup)]
            
            apriori_mem = result['apriori']['memory_used']
            bitwise_mem = result['bitwise']['memory_used']
            optimized_mem = result['bitwise_optimized']['memory_used']
            
            min_sup_str = f"{float(min_sup)*100:.0f}\\%"
            
            latex_code += f"{min_sup_str} & {apriori_mem:.2f} & {bitwise_mem:.2f} & {optimized_mem:.2f} \\\\\n"
        
        latex_code += "\\hline\n\\end{tabular}\n\\end{table}\n"
        
        return latex_code
    
    def generate_itemsets_table(self):
        """Generate LaTeX table for itemset and candidate counts"""
        latex_code = """
\\begin{table}[h]
\\centering
\\caption{Frequent Itemsets and Candidates Generated}
\\begin{tabular}{|c|c|c|}
\\hline
\\textbf{Min Support} & \\textbf{Frequent Itemsets} & \\textbf{Candidates} \\\\
\\hline
"""
        
        for min_sup in sorted(self.results.keys(), key=float):
            result = self.results[str(min_sup)]
            
            num_itemsets = result['apriori']['num_itemsets']
            num_candidates = result['apriori']['num_candidates']
            
            min_sup_str = f"{float(min_sup)*100:.0f}\\%"
            
            latex_code += f"{min_sup_str} & {num_itemsets} & {num_candidates} \\\\\n"
        
        latex_code += "\\hline\n\\end{tabular}\n\\end{table}\n"
        
        return latex_code
    
    def print_all_tables(self):
        """Print all tables in sequence"""
        print("\n" + "="*80)
        print("LATEX TABLES FOR EXPERIMENTAL SECTION")
        print("="*80 + "\n")
        
        print("Execution Time Table:")
        print(self.generate_latex_table())
        
        print("\nMemory Consumption Table:")
        print(self.generate_memory_table())
        
        print("\nFrequent Itemsets Table:")
        print(self.generate_itemsets_table())


def generate_sample_results():
    """Generate sample results for testing"""
    sample_results = {
        "0.5": {
            "apriori": {
                "execution_time": 8.3200,
                "memory_used": 187.45,
                "num_itemsets": 1523,
                "num_candidates": 4581
            },
            "bitwise": {
                "execution_time": 1.8900,
                "memory_used": 78.32,
                "num_itemsets": 1523,
                "num_candidates": 4581
            },
            "bitwise_optimized": {
                "execution_time": 0.5340,
                "memory_used": 72.18,
                "num_itemsets": 1523,
                "num_candidates": 4581
            },
            "speedup": 15.59
        },
        "0.6": {
            "apriori": {
                "execution_time": 5.1200,
                "memory_used": 142.30,
                "num_itemsets": 892,
                "num_candidates": 2341
            },
            "bitwise": {
                "execution_time": 1.1200,
                "memory_used": 56.15,
                "num_itemsets": 892,
                "num_candidates": 2341
            },
            "bitwise_optimized": {
                "execution_time": 0.3150,
                "memory_used": 52.10,
                "num_itemsets": 892,
                "num_candidates": 2341
            },
            "speedup": 16.25
        },
        "0.7": {
            "apriori": {
                "execution_time": 2.8900,
                "memory_used": 98.50,
                "num_itemsets": 456,
                "num_candidates": 1123
            },
            "bitwise": {
                "execution_time": 0.6780,
                "memory_used": 38.25,
                "num_itemsets": 456,
                "num_candidates": 1123
            },
            "bitwise_optimized": {
                "execution_time": 0.1890,
                "memory_used": 35.10,
                "num_itemsets": 456,
                "num_candidates": 1123
            },
            "speedup": 15.30
        },
        "0.8": {
            "apriori": {
                "execution_time": 1.2340,
                "memory_used": 56.20,
                "num_itemsets": 178,
                "num_candidates": 412
            },
            "bitwise": {
                "execution_time": 0.3456,
                "memory_used": 22.15,
                "num_itemsets": 178,
                "num_candidates": 412
            },
            "bitwise_optimized": {
                "execution_time": 0.0923,
                "memory_used": 20.50,
                "num_itemsets": 178,
                "num_candidates": 412
            },
            "speedup": 13.37
        },
        "0.9": {
            "apriori": {
                "execution_time": 0.3210,
                "memory_used": 28.45,
                "num_itemsets": 32,
                "num_candidates": 78
            },
            "bitwise": {
                "execution_time": 0.0876,
                "memory_used": 12.10,
                "num_itemsets": 32,
                "num_candidates": 78
            },
            "bitwise_optimized": {
                "execution_time": 0.0234,
                "memory_used": 11.50,
                "num_itemsets": 32,
                "num_candidates": 78
            },
            "speedup": 13.72
        }
    }
    
    return sample_results


if __name__ == "__main__":
    # Generate sample results for demonstration
    sample = generate_sample_results()
    
    # Save to temporary file
    temp_file = "sample_results.json"
    with open(temp_file, 'w') as f:
        json.dump(sample, f, indent=4)
    
    # Generate tables
    generator = ResultsTableGenerator(temp_file)
    generator.print_all_tables()
    
    # Cleanup
    os.remove(temp_file)
