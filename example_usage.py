#!/usr/bin/env python3
"""
Simple example demonstrating the Collatz Conjecture analysis.

This script shows basic usage of the CollatzConjecture class.
"""

from collatz_conjecture import CollatzConjecture

def simple_example():
    """Demonstrate basic Collatz Conjecture analysis."""
    print("=== Simple Collatz Conjecture Example ===\n")
    
    # Initialize the analyzer
    collatz = CollatzConjecture()
    
    # Example 1: Analyze a famous number (27)
    print("1. Analyzing the famous number 27:")
    analysis = collatz.analyze_sequence(27)
    print(f"   Starting number: {analysis['starting_number']}")
    print(f"   Sequence length: {analysis['sequence_length']}")
    print(f"   Peak value: {analysis['max_value']}")
    print(f"   Steps to peak: {analysis['steps_to_peak']}")
    print(f"   Total steps: {analysis['total_steps']}")
    print(f"   Execution time: {analysis['execution_time']:.6f} seconds")
    
    # Show the sequence
    sequence = analysis['sequence']
    print(f"   Sequence: {' → '.join(map(str, sequence[:10]))}...")
    if len(sequence) > 10:
        print(f"            ...{' → '.join(map(str, sequence[-5:]))}")
    
    print()
    
    # Example 2: Quick analysis of first 10 numbers
    print("2. Quick analysis of numbers 1-10:")
    for n in range(1, 11):
        seq = collatz.collatz_sequence(n)
        print(f"   {n}: {len(seq)} steps, peak: {max(seq)}")
    
    print()
    
    # Example 3: Find some interesting numbers
    print("3. Finding interesting numbers (1-100):")
    data = collatz.run_analysis(1, 100)
    
    # Find longest sequence in this range
    longest = data.loc[data['sequence_length'].idxmax()]
    print(f"   Longest sequence: {longest['starting_number']} ({longest['sequence_length']} steps)")
    
    # Find highest peak in this range
    highest_peak = data.loc[data['max_value'].idxmax()]
    print(f"   Highest peak: {highest_peak['starting_number']} (peaks at {highest_peak['max_value']})")
    
    print()
    
    # Example 4: Generate insights
    print("4. Key insights from the data:")
    insights = collatz.generate_insights()
    print(f"   Average sequence length: {insights['average_sequence_length']:.2f}")
    print(f"   Average peak value: {insights['average_max_value']:.2f}")
    print(f"   Average steps to peak: {insights['average_steps_to_peak']:.2f}")
    
    print("\n=== Example Complete ===")

if __name__ == "__main__":
    simple_example()

