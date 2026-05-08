import gzip
from typing import List, Set


class DatasetLoader:
    @staticmethod
    def load_gzip_dataset(filepath: str) -> List[Set]:
        """Load and parse a gzip compressed dataset file"""
        transactions = []
        
        try:
            with gzip.open(filepath, 'rt', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        items = set(map(int, line.split()))
                        transactions.append(items)
        except Exception as e:
            print(f"Error loading dataset from {filepath}: {e}")
            return []
        
        return transactions
    
    @staticmethod
    def is_gzip_file(filepath: str) -> bool:
        """Check if file is gzip compressed by reading magic bytes"""
        try:
            with open(filepath, 'rb') as f:
                magic = f.read(2)
                return magic == b'\x1f\x8b'
        except:
            return False
    
    @staticmethod
    def load_dataset(filepath: str) -> List[Set]:
        """Load dataset, auto-detecting gzip vs plain text format"""
        if DatasetLoader.is_gzip_file(filepath):
            return DatasetLoader.load_gzip_dataset(filepath)
        
        transactions = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        items = set(map(int, line.split()))
                        transactions.append(items)
        except Exception as e:
            print(f"Error loading dataset from {filepath}: {e}")
            return []
        
        return transactions
    
    @staticmethod
    def get_dataset_info(dataset: List[Set]) -> dict:
        """Get basic information about the dataset"""
        if not dataset:
            return {}
        
        all_items = set()
        for transaction in dataset:
            all_items.update(transaction)
        
        avg_transaction_size = sum(len(t) for t in dataset) / len(dataset)
        max_transaction_size = max(len(t) for t in dataset)
        min_transaction_size = min(len(t) for t in dataset)
        
        return {
            'transaction_count': len(dataset),
            'unique_items': len(all_items),
            'avg_transaction_size': round(avg_transaction_size, 2),
            'max_transaction_size': max_transaction_size,
            'min_transaction_size': min_transaction_size
        }
