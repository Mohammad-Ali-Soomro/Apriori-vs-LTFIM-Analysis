import gzip
import time
import psutil
import os
from itertools import combinations
from collections import defaultdict


class Apriori:
    def __init__(self, dataset, min_sup):
        self.dataset = dataset
        self.min_sup = min_sup
        self.transaction_count = len(dataset)
        self.min_sup_count = max(1, int(self.min_sup * self.transaction_count))
        self.frequent_itemsets = []
        self.candidates_generated = 0
    
    def get_frequent_items(self):
        """Find all frequent 1-itemsets"""
        item_count = defaultdict(int)
        
        for transaction in self.dataset:
            for item in transaction:
                item_count[item] += 1
        
        frequent = {}
        for item, count in item_count.items():
            if count >= self.min_sup_count:
                frequent[frozenset([item])] = count
        
        return frequent
    
    def generate_candidates(self, frequent_itemsets):
        """Generate candidate itemsets from previous frequent itemsets"""
        items = list(frequent_itemsets.keys())
        candidates = []
        
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                union = items[i] | items[j]
                if len(union) == len(items[i]) + 1:
                    candidates.append(union)
        
        return candidates
    
    def count_support(self, candidates):
        """Count support for candidate itemsets"""
        support_count = defaultdict(int)
        
        for transaction in self.dataset:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    support_count[candidate] += 1
        
        return support_count
    
    def mine(self):
        """Execute Apriori algorithm"""
        frequent_itemsets = {}
        current_frequent = self.get_frequent_items()
        frequent_itemsets.update(current_frequent)
        
        k = 2
        
        while current_frequent:
            candidates = self.generate_candidates(current_frequent)
            self.candidates_generated += len(candidates)
            
            if not candidates:
                break
            
            support_count = self.count_support(candidates)
            
            current_frequent = {}
            for itemset, count in support_count.items():
                if count >= self.min_sup_count:
                    current_frequent[itemset] = count
            
            if current_frequent:
                frequent_itemsets.update(current_frequent)
            
            k += 1
        
        self.frequent_itemsets = frequent_itemsets
        return frequent_itemsets


class BitwiseVerticalFIM:
    def __init__(self, dataset, min_sup):
        self.dataset = dataset
        self.min_sup = min_sup
        self.transaction_count = len(dataset)
        self.min_sup_count = max(1, int(self.min_sup * self.transaction_count))
        self.frequent_itemsets = []
        self.candidates_generated = 0
        self.vertical_bitmaps = {}
    
    def create_vertical_representation(self):
        """Convert horizontal dataset to vertical bitmap representation"""
        all_items = set()
        
        for transaction in self.dataset:
            for item in transaction:
                all_items.add(item)
        
        for item in all_items:
            bitmap = 0
            for tid, transaction in enumerate(self.dataset):
                if item in transaction:
                    bitmap |= (1 << tid)
            
            support = bin(bitmap).count('1')
            if support >= self.min_sup_count:
                self.vertical_bitmaps[frozenset([item])] = bitmap
    
    def popcount(self, bitmap):
        """Count number of set bits (support)"""
        return bin(bitmap).count('1')
    
    def bitwise_and(self, bitmap1, bitmap2):
        """Perform bitwise AND with zero-skipping optimization"""
        result = bitmap1 & bitmap2
        if result == 0:
            return 0
        return result
    
    def generate_candidates(self, frequent_itemsets):
        """Generate candidates from frequent itemsets"""
        items = list(frequent_itemsets.keys())
        candidates = []
        
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                union = items[i] | items[j]
                if len(union) == len(items[i]) + 1:
                    candidates.append(union)
        
        return candidates
    
    def compute_support(self, candidate, bitmaps_dict):
        """Compute support for a candidate using bitwise operations"""
        items = list(candidate)
        
        if not items:
            return 0
        
        result_bitmap = bitmaps_dict[frozenset([items[0]])]
        
        for item in items[1:]:
            result_bitmap = self.bitwise_and(result_bitmap, 
                                            bitmaps_dict[frozenset([item])])
            if result_bitmap == 0:
                break
        
        return self.popcount(result_bitmap)
    
    def mine(self):
        """Execute Bitwise Vertical FIM algorithm"""
        self.create_vertical_representation()
        frequent_itemsets = dict(self.vertical_bitmaps)
        
        k = 2
        current_frequent = dict(self.vertical_bitmaps)
        
        while current_frequent:
            candidates = self.generate_candidates(current_frequent)
            self.candidates_generated += len(candidates)
            
            if not candidates:
                break
            
            new_frequent = {}
            
            for candidate in candidates:
                items = list(candidate)
                
                result_bitmap = self.vertical_bitmaps[frozenset([items[0]])]
                for item in items[1:]:
                    result_bitmap = self.bitwise_and(
                        result_bitmap,
                        self.vertical_bitmaps[frozenset([item])]
                    )
                    if result_bitmap == 0:
                        break
                
                support = self.popcount(result_bitmap)
                
                if support >= self.min_sup_count:
                    self.vertical_bitmaps[candidate] = result_bitmap
                    new_frequent[candidate] = support
            
            if new_frequent:
                frequent_itemsets.update(new_frequent)
                current_frequent = new_frequent
            else:
                break
            
            k += 1
        
        self.frequent_itemsets = frequent_itemsets
        return frequent_itemsets


class BitwiseVerticalFIMOptimized(BitwiseVerticalFIM):
    """Extended version with optimizations: Zero-Skipping and Multi-threading"""
    
    def __init__(self, dataset, min_sup):
        super().__init__(dataset, min_sup)
        self.use_multithreading = True
    
    def bitwise_and_zero_skip(self, bitmap1, bitmap2):
        """Bitwise AND with zero-skipping optimization"""
        result = bitmap1 & bitmap2
        return result
    
    def mine_multithreaded(self):
        """Execute algorithm with multi-threading support"""
        import threading
        
        self.create_vertical_representation()
        frequent_itemsets = dict(self.vertical_bitmaps)
        
        k = 2
        current_frequent = dict(self.vertical_bitmaps)
        
        while current_frequent:
            candidates = self.generate_candidates(current_frequent)
            self.candidates_generated += len(candidates)
            
            if not candidates:
                break
            
            new_frequent = {}
            lock = threading.Lock()
            
            def process_candidate(candidate):
                items = list(candidate)
                
                result_bitmap = self.vertical_bitmaps[frozenset([items[0]])]
                for item in items[1:]:
                    result_bitmap = self.bitwise_and_zero_skip(
                        result_bitmap,
                        self.vertical_bitmaps[frozenset([item])]
                    )
                    if result_bitmap == 0:
                        break
                
                support = self.popcount(result_bitmap)
                
                if support >= self.min_sup_count:
                    with lock:
                        self.vertical_bitmaps[candidate] = result_bitmap
                        new_frequent[candidate] = support
            
            threads = []
            max_threads = min(4, len(candidates))
            
            for candidate in candidates:
                thread = threading.Thread(target=process_candidate, args=(candidate,))
                threads.append(thread)
                thread.start()
                
                if len(threads) >= max_threads:
                    for t in threads:
                        t.join()
                    threads = []
            
            for t in threads:
                t.join()
            
            if new_frequent:
                frequent_itemsets.update(new_frequent)
                current_frequent = new_frequent
            else:
                break
            
            k += 1
        
        self.frequent_itemsets = frequent_itemsets
        return frequent_itemsets
    
    def mine(self):
        """Execute optimized algorithm with multi-threading"""
        return self.mine_multithreaded()
