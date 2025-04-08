import csv
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

"""
Script to calculate MRR and Recall@k metrics from search evaluation results
"""

RESULTS_CSV = "backend/evaluation/search_evaluation_results.csv"
METRICS_OUTPUT = "backend/evaluation/search_metrics_results.csv"
CHARTS_DIR = "backend/evaluation/charts"

def calculate_mrr(ranks):
    """
    Calculate Mean Reciprocal Rank (MRR)
    
    Args:
        ranks: List of ranks (positions), with 0 or "not found" meaning not found
        
    Returns:
        float: The MRR value
    """
    numeric_ranks = []
    for rank in ranks:
        if isinstance(rank, str) and rank == "not found":
            numeric_ranks.append(0)
        else:
            try:
                numeric_ranks.append(int(rank))
            except (ValueError, TypeError):
                numeric_ranks.append(0)
    
    reciprocal_ranks = []
    for rank in numeric_ranks:
        if rank > 0:
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)
    
    if not reciprocal_ranks:
        return 0.0
    
    return sum(reciprocal_ranks) / len(reciprocal_ranks)

def calculate_recall_at_k(ranks, k):
    """
    Calculate Recall@k (percentage of queries where the correct document
    was found within the first k results)
    
    Args:
        ranks: List of ranks (positions), with 0 or "not found" meaning not found
        k: The k value for Recall@k
        
    Returns:
        float: The Recall@k value
    """
    numeric_ranks = []
    for rank in ranks:
        if isinstance(rank, str) and rank == "not found":
            numeric_ranks.append(0)
        else:
            try:
                numeric_ranks.append(int(rank))
            except (ValueError, TypeError):
                numeric_ranks.append(0)
    
    found_within_k = sum(1 for rank in numeric_ranks if 1 <= rank <= k)
    
    if not numeric_ranks:
        return 0.0
    
    return found_within_k / len(numeric_ranks)

def calculate_metrics(results_file):
    """
    Calculate MRR and Recall@k metrics from search evaluation results
    
    Args:
        results_file: Path to the CSV file with search evaluation results
        
    Returns:
        dict: Dictionary with calculated metrics
    """
    if not os.path.exists(results_file):
        print(f"Results file not found: {results_file}")
        return None
    
    try:
        df = pd.read_csv(results_file)
    except Exception as e:
        print(f"Error reading results file: {e}")
        return None
    
    keyword_ranks = df['keyword_search'].tolist()
    semantic_ranks = df['semantic_search'].tolist()
    
    keyword_mrr = calculate_mrr(keyword_ranks)
    semantic_mrr = calculate_mrr(semantic_ranks)
    
    metrics = {
        'keyword_search': {
            'mrr': keyword_mrr,
            'recall@1': calculate_recall_at_k(keyword_ranks, 1),
            'recall@3': calculate_recall_at_k(keyword_ranks, 3),
            'recall@5': calculate_recall_at_k(keyword_ranks, 5)
        },
        'semantic_search': {
            'mrr': semantic_mrr,
            'recall@1': calculate_recall_at_k(semantic_ranks, 1),
            'recall@3': calculate_recall_at_k(semantic_ranks, 3),
            'recall@5': calculate_recall_at_k(semantic_ranks, 5)
        }
    }
    
    return metrics

def generate_charts(metrics, output_dir):
    """
    Generate comparison charts for the metrics
    
    Args:
        metrics: Dictionary with calculated metrics
        output_dir: Directory to save the charts
    """
    os.makedirs(output_dir, exist_ok=True)
    
    search_methods = list(metrics.keys())
    mrr_values = [metrics[method]['mrr'] for method in search_methods]
    recall_1_values = [metrics[method]['recall@1'] for method in search_methods]
    recall_3_values = [metrics[method]['recall@3'] for method in search_methods]
    recall_5_values = [metrics[method]['recall@5'] for method in search_methods]
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.bar(search_methods, mrr_values, color=['blue', 'orange'])
    plt.title('Mean Reciprocal Rank (MRR)')
    plt.ylabel('MRR')
    plt.ylim(0, 1)
    
    plt.subplot(2, 2, 2)
    plt.bar(search_methods, recall_1_values, color=['blue', 'orange'])
    plt.title('Recall@1')
    plt.ylabel('Recall')
    plt.ylim(0, 1)
    
    plt.subplot(2, 2, 3)
    plt.bar(search_methods, recall_3_values, color=['blue', 'orange'])
    plt.title('Recall@3')
    plt.ylabel('Recall')
    plt.ylim(0, 1)
    
    plt.subplot(2, 2, 4)
    plt.bar(search_methods, recall_5_values, color=['blue', 'orange'])
    plt.title('Recall@5')
    plt.ylabel('Recall')
    plt.ylim(0, 1)
    
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, 'search_metrics_comparison.png'))
    
    plt.figure(figsize=(10, 6))
    
    labels = ['MRR', 'Recall@1', 'Recall@3', 'Recall@5']
    keyword_values = [metrics['keyword_search'][metric] for metric in ['mrr', 'recall@1', 'recall@3', 'recall@5']]
    semantic_values = [metrics['semantic_search'][metric] for metric in ['mrr', 'recall@1', 'recall@3', 'recall@5']]
    
    x = np.arange(len(labels))
    width = 0.35 
    
    plt.bar(x - width/2, keyword_values, width, label='Keyword Search')
    plt.bar(x + width/2, semantic_values, width, label='Semantic Search')
    
    plt.ylabel('Value')
    plt.title('Search Metrics Comparison')
    plt.xticks(x, labels)
    plt.legend()
    plt.ylim(0, 1)
    
    for i, v in enumerate(keyword_values):
        plt.text(i - width/2, v + 0.02, f'{v:.2f}', ha='center')
    
    for i, v in enumerate(semantic_values):
        plt.text(i + width/2, v + 0.02, f'{v:.2f}', ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'search_metrics_combined.png'))
    
    print(f"Charts saved to {output_dir}")

def main():
    """
    Main function to calculate metrics and generate charts
    """
    print("Calculating search evaluation metrics...")
    
    metrics = calculate_metrics(RESULTS_CSV)
    
    if not metrics:
        print("No metrics calculated. Exiting.")
        return
    
    print("\n===== SEARCH EVALUATION METRICS =====")
    for search_method, method_metrics in metrics.items():
        print(f"\n{search_method.upper()}")
        for metric_name, metric_value in method_metrics.items():
            print(f"  {metric_name}: {metric_value:.4f}")
    
    with open(METRICS_OUTPUT, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Keyword Search', 'Semantic Search'])
        writer.writerow(['MRR', metrics['keyword_search']['mrr'], metrics['semantic_search']['mrr']])
        writer.writerow(['Recall@1', metrics['keyword_search']['recall@1'], metrics['semantic_search']['recall@1']])
        writer.writerow(['Recall@3', metrics['keyword_search']['recall@3'], metrics['semantic_search']['recall@3']])
        writer.writerow(['Recall@5', metrics['keyword_search']['recall@5'], metrics['semantic_search']['recall@5']])
    
    print(f"\nMetrics saved to {METRICS_OUTPUT}")
    
    generate_charts(metrics, CHARTS_DIR)

if __name__ == "__main__":
    main()