#!/usr/bin/env python3
"""
Demonstration of interesting findings from Collatz Conjecture analysis.

This script shows some fascinating patterns and insights discovered through analysis.
"""

from collatz_conjecture import CollatzConjecture
import pandas as pd

def demonstrate_findings():
    """Show interesting findings from Collatz Conjecture analysis."""
    print("=" * 60)
    print("INTERESTING FINDINGS FROM COLLATZ CONJECTURE")
    print("=" * 60)
    
    collatz = CollatzConjecture()
    
    # Analyze a larger range for better insights
    print("\n1. Analyzing numbers 1-5000 for comprehensive insights...")
    data = collatz.run_analysis(1, 5000)
    
    print("\n2. TOP 10 MOST INTERESTING NUMBERS:")
    print("-" * 50)
    
    # Find numbers with longest sequences
    longest_sequences = data.nlargest(10, 'sequence_length')
    print("\nLongest Sequences:")
    for idx, row in longest_sequences.iterrows():
        print(f"  {row['starting_number']:4d}: {row['sequence_length']:3d} steps, peak: {row['max_value']:6d}")
    
    # Find numbers with highest peaks
    highest_peaks = data.nlargest(10, 'max_value')
    print("\nHighest Peaks:")
    for idx, row in highest_peaks.iterrows():
        print(f"  {row['starting_number']:4d}: peaks at {row['max_value']:6d}, length: {row['sequence_length']:3d}")
    
    # Find numbers with most steps to peak
    most_steps_to_peak = data.nlargest(10, 'steps_to_peak')
    print("\nMost Steps to Peak:")
    for idx, row in most_steps_to_peak.iterrows():
        print(f"  {row['starting_number']:4d}: {row['steps_to_peak']:3d} steps to peak, total: {row['sequence_length']:3d}")
    
    print("\n3. STATISTICAL INSIGHTS:")
    print("-" * 50)
    
    insights = collatz.generate_insights()
    
    print(f"Total numbers analyzed: {insights['total_numbers_analyzed']}")
    print(f"Average sequence length: {insights['average_sequence_length']:.2f}")
    print(f"Average peak value: {insights['average_max_value']:.2f}")
    print(f"Average steps to peak: {insights['average_steps_to_peak']:.2f}")
    
    # Calculate some additional statistics
    print(f"\nSequence length statistics:")
    print(f"  Median: {data['sequence_length'].median():.2f}")
    print(f"  Standard deviation: {data['sequence_length'].std():.2f}")
    print(f"  90th percentile: {data['sequence_length'].quantile(0.9):.2f}")
    print(f"  95th percentile: {data['sequence_length'].quantile(0.95):.2f}")
    
    print(f"\nPeak value statistics:")
    print(f"  Median: {data['max_value'].median():.2f}")
    print(f"  Standard deviation: {data['max_value'].std():.2f}")
    print(f"  90th percentile: {data['max_value'].quantile(0.9):.2f}")
    
    print("\n4. INTERESTING PATTERNS:")
    print("-" * 50)
    
    # Find numbers that are powers of 2 (should have short sequences)
    powers_of_2 = [2**i for i in range(1, 13)]  # 2^1 to 2^12
    print("\nPowers of 2 (should have short sequences):")
    for power in powers_of_2:
        if power <= 5000:
            seq = collatz.collatz_sequence(power)
            print(f"  2^{power.bit_length()-1} = {power}: {len(seq)} steps, peak: {max(seq)}")
    
    # Find some numbers with interesting properties
    print("\nNumbers with interesting properties:")
    
    # Find a number with high peak but short sequence
    high_peak_short_seq = data.loc[(data['max_value'] > data['max_value'].quantile(0.9)) & 
                                   (data['sequence_length'] < data['sequence_length'].quantile(0.5))]
    if not high_peak_short_seq.empty:
        interesting = high_peak_short_seq.iloc[0]
        print(f"  High peak, short sequence: {interesting['starting_number']}")
        print(f"    Peak: {interesting['max_value']}, Length: {interesting['sequence_length']}")
    
    # Find a number with long sequence but low peak
    long_seq_low_peak = data.loc[(data['sequence_length'] > data['sequence_length'].quantile(0.9)) & 
                                 (data['max_value'] < data['max_value'].quantile(0.5))]
    if not long_seq_low_peak.empty:
        interesting = long_seq_low_peak.iloc[0]
        print(f"  Long sequence, low peak: {interesting['starting_number']}")
        print(f"    Length: {interesting['sequence_length']}, Peak: {interesting['max_value']}")
    
    print("\n5. CORRELATION ANALYSIS:")
    print("-" * 50)
    
    # Calculate correlations
    correlations = data[['starting_number', 'sequence_length', 'max_value', 'steps_to_peak']].corr()
    
    print("Correlation matrix:")
    print(correlations.round(3))
    
    print("\nKey correlations:")
    print(f"  Starting number vs Sequence length: {correlations.loc['starting_number', 'sequence_length']:.3f}")
    print(f"  Starting number vs Max value: {correlations.loc['starting_number', 'max_value']:.3f}")
    print(f"  Sequence length vs Max value: {correlations.loc['sequence_length', 'max_value']:.3f}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_findings()

