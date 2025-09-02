import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple
import time
from datetime import datetime

class CollatzConjecture:
    """
    A class to demonstrate and analyze the Collatz Conjecture.
    
    The Collatz Conjecture states that for any positive integer n:
    1. If n is even, divide it by 2
    2. If n is odd, multiply it by 3 and add 1
    3. Repeat until you reach 1
    
    This class tracks the sequence, analyzes patterns, and creates visualizations.
    """
    
    def __init__(self):
        """Initialize the Collatz Conjecture analyzer."""
        self.data = pd.DataFrame({
            'starting_number': pd.Series(dtype='int64'),
            'sequence_length': pd.Series(dtype='int64'),
            'max_value': pd.Series(dtype='int64'),
            'steps_to_peak': pd.Series(dtype='int64'),
            'total_steps': pd.Series(dtype='int64'),
            'peak_value': pd.Series(dtype='int64'),
            'sequence': pd.Series(dtype='object'),
            'execution_time': pd.Series(dtype='float64'),
            'timestamp': pd.Series(dtype='datetime64[ns]')
        })
        
    def collatz_sequence(self, n: int) -> List[int]:
        """
        Generate the Collatz sequence for a given number.
        
        Args:
            n (int): Starting number
            
        Returns:
            List[int]: The complete Collatz sequence
        """
        if n <= 0:
            raise ValueError("Starting number must be positive")
            
        sequence = [n]
        current = n
        
        while current != 1:
            if current % 2 == 0:  # Even
                current = current // 2
            else:  # Odd
                current = 3 * current + 1
            sequence.append(current)
            
        return sequence
    
    def analyze_sequence(self, n: int) -> dict:
        """
        Analyze a Collatz sequence and extract key metrics.
        
        Args:
            n (int): Starting number
            
        Returns:
            dict: Analysis results
        """
        start_time = time.time()
        sequence = self.collatz_sequence(n)
        execution_time = time.time() - start_time
        
        # Find peak value and its position
        max_value = max(sequence)
        peak_index = sequence.index(max_value)
        
        # Calculate metrics
        analysis = {
            'starting_number': n,
            'sequence_length': len(sequence),
            'max_value': max_value,
            'steps_to_peak': peak_index,
            'total_steps': len(sequence) - 1,  # Exclude starting number
            'peak_value': max_value,
            'sequence': sequence,
            'execution_time': execution_time,
            'timestamp': datetime.now()
        }
        
        return analysis
    
    def run_analysis(self, start_range: int, end_range: int) -> pd.DataFrame:
        """
        Run Collatz analysis for a range of numbers.
        
        Args:
            start_range (int): Starting number of the range
            end_range (int): Ending number of the range
            
        Returns:
            pd.DataFrame: Analysis results for all numbers in range
        """
        print(f"Analyzing Collatz sequences for numbers {start_range} to {end_range}...")
        
        results = []
        for n in range(start_range, end_range + 1):
            try:
                analysis = self.analyze_sequence(n)
                results.append(analysis)
                
                # Progress indicator
                if n % 100 == 0:
                    print(f"Processed {n} numbers...")
                    
            except Exception as e:
                print(f"Error processing {n}: {e}")
                continue
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Store sequence as string for DataFrame compatibility
        df['sequence_str'] = df['sequence'].apply(lambda x: str(x))
        
        # Ensure proper data types for numeric columns
        numeric_columns = ['starting_number', 'sequence_length', 'max_value', 'steps_to_peak', 'total_steps', 'peak_value', 'execution_time']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Update main data
        self.data = pd.concat([self.data, df], ignore_index=True)
        
        print(f"Analysis complete! Processed {len(results)} numbers.")
        return df
    
    def generate_insights(self) -> dict:
        """
        Generate insights from the collected data.
        
        Returns:
            dict: Key insights and statistics
        """
        if self.data.empty:
            return {"error": "No data available for analysis"}
        
        insights = {
            'total_numbers_analyzed': len(self.data),
            'average_sequence_length': self.data['sequence_length'].mean(),
            'max_sequence_length': self.data['sequence_length'].max(),
            'min_sequence_length': self.data['sequence_length'].min(),
            'average_max_value': self.data['max_value'].mean(),
            'highest_peak_value': self.data['max_value'].max(),
            'average_steps_to_peak': self.data['steps_to_peak'].mean(),
            'numbers_with_longest_sequences': self.data.nlargest(5, 'sequence_length')[['starting_number', 'sequence_length']].to_dict('records'),
            'numbers_with_highest_peaks': self.data.nlargest(5, 'max_value')[['starting_number', 'max_value']].to_dict('records'),
            'execution_statistics': {
                'average_execution_time': self.data['execution_time'].mean(),
                'total_execution_time': self.data['execution_time'].sum(),
                'fastest_execution': self.data['execution_time'].min(),
                'slowest_execution': self.data['execution_time'].max()
            }
        }
        
        return insights
    
    def create_visualizations(self, save_plots: bool = True):
        """
        Create comprehensive visualizations of the Collatz data.
        
        Args:
            save_plots (bool): Whether to save plots to files
        """
        if self.data.empty:
            print("No data available for visualization")
            return
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Create a figure with multiple subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Sequence Length Distribution
        plt.subplot(3, 3, 1)
        plt.hist(self.data['sequence_length'], bins=30, alpha=0.7, edgecolor='black')
        plt.title('Distribution of Sequence Lengths')
        plt.xlabel('Sequence Length')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        # 2. Max Value vs Starting Number
        plt.subplot(3, 3, 2)
        plt.scatter(self.data['starting_number'], self.data['max_value'], alpha=0.6, s=20)
        plt.title('Peak Value vs Starting Number')
        plt.xlabel('Starting Number')
        plt.ylabel('Peak Value')
        plt.grid(True, alpha=0.3)
        
        # 3. Sequence Length vs Starting Number
        plt.subplot(3, 3, 3)
        plt.scatter(self.data['starting_number'], self.data['sequence_length'], alpha=0.6, s=20)
        plt.title('Sequence Length vs Starting Number')
        plt.xlabel('Starting Number')
        plt.ylabel('Sequence Length')
        plt.grid(True, alpha=0.3)
        
        # 4. Steps to Peak Distribution
        plt.subplot(3, 3, 4)
        plt.hist(self.data['steps_to_peak'], bins=30, alpha=0.7, edgecolor='black')
        plt.title('Distribution of Steps to Peak')
        plt.xlabel('Steps to Peak')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        
        # 5. Correlation Heatmap
        plt.subplot(3, 3, 5)
        numeric_cols = ['starting_number', 'sequence_length', 'max_value', 'steps_to_peak', 'total_steps']
        correlation_matrix = self.data[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True)
        plt.title('Correlation Matrix')
        
        # 6. Box Plot of Sequence Lengths
        plt.subplot(3, 3, 6)
        plt.boxplot(self.data['sequence_length'])
        plt.title('Box Plot of Sequence Lengths')
        plt.ylabel('Sequence Length')
        plt.grid(True, alpha=0.3)
        
        # 7. Execution Time Analysis
        plt.subplot(3, 3, 7)
        plt.scatter(self.data['sequence_length'], self.data['execution_time'], alpha=0.6, s=20)
        plt.title('Execution Time vs Sequence Length')
        plt.xlabel('Sequence Length')
        plt.ylabel('Execution Time (seconds)')
        plt.grid(True, alpha=0.3)
        
        # 8. Top 10 Longest Sequences
        plt.subplot(3, 3, 8)
        top_10 = self.data.nlargest(10, 'sequence_length')
        plt.barh(range(len(top_10)), top_10['sequence_length'])
        plt.yticks(range(len(top_10)), top_10['starting_number'])
        plt.title('Top 10 Longest Sequences')
        plt.xlabel('Sequence Length')
        plt.ylabel('Starting Number')
        
        # 9. Sequence Length vs Max Value
        plt.subplot(3, 3, 9)
        plt.scatter(self.data['sequence_length'], self.data['max_value'], alpha=0.6, s=20)
        plt.title('Sequence Length vs Peak Value')
        plt.xlabel('Sequence Length')
        plt.ylabel('Peak Value')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig('collatz_analysis.png', dpi=300, bbox_inches='tight')
            print("Visualizations saved as 'collatz_analysis.png'")
        
        plt.show()
    
    def plot_individual_sequence(self, n: int, save_plot: bool = True):
        """
        Plot an individual Collatz sequence.
        
        Args:
            n (int): Starting number
            save_plot (bool): Whether to save the plot
        """
        try:
            sequence = self.collatz_sequence(n)
            
            plt.figure(figsize=(12, 8))
            
            # Plot the sequence
            plt.subplot(2, 1, 1)
            plt.plot(range(len(sequence)), sequence, 'b-o', linewidth=2, markersize=4)
            plt.title(f'Collatz Sequence for n = {n}')
            plt.xlabel('Step')
            plt.ylabel('Value')
            plt.grid(True, alpha=0.3)
            plt.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='Target (1)')
            plt.legend()
            
            # Plot log scale for better visualization of large values
            plt.subplot(2, 1, 2)
            plt.semilogy(range(len(sequence)), sequence, 'g-o', linewidth=2, markersize=4)
            plt.title(f'Collatz Sequence for n = {n} (Log Scale)')
            plt.xlabel('Step')
            plt.ylabel('Value (Log Scale)')
            plt.grid(True, alpha=0.3)
            plt.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='Target (1)')
            plt.legend()
            
            plt.tight_layout()
            
            if save_plot:
                plt.savefig(f'collatz_sequence_{n}.png', dpi=300, bbox_inches='tight')
                print(f"Sequence plot saved as 'collatz_sequence_{n}.png'")
            
            plt.show()
            
        except Exception as e:
            print(f"Error plotting sequence for {n}: {e}")
    
    def save_data(self, filename: str = 'collatz_data.csv'):
        """
        Save the analysis data to a CSV file.
        
        Args:
            filename (str): Output filename
        """
        if not self.data.empty:
            # Create a copy without the sequence column for CSV export
            export_data = self.data.drop(['sequence', 'sequence_str'], axis=1, errors='ignore')
            export_data.to_csv(filename, index=False)
            print(f"Data saved to '{filename}'")
        else:
            print("No data to save")

def main():
    """Main function to demonstrate the Collatz Conjecture analysis."""
    print("=" * 60)
    print("THE COLLATZ CONJECTURE ANALYSIS")
    print("=" * 60)
    
    # Initialize the analyzer
    collatz = CollatzConjecture()
    
    # Example 1: Analyze a single sequence
    print("\n1. Analyzing individual sequences...")
    test_numbers = [27, 97, 871, 6171]
    
    for n in test_numbers:
        print(f"\nAnalyzing sequence for n = {n}")
        analysis = collatz.analyze_sequence(n)
        print(f"  Sequence length: {analysis['sequence_length']}")
        print(f"  Peak value: {analysis['max_value']}")
        print(f"  Steps to peak: {analysis['steps_to_peak']}")
        print(f"  Total steps: {analysis['total_steps']}")
        
        # Plot individual sequence
        collatz.plot_individual_sequence(n)
    
    # Example 2: Analyze a range of numbers
    print("\n2. Analyzing range of numbers (1-1000)...")
    range_data = collatz.run_analysis(1, 1000)
    
    # Example 3: Generate insights
    print("\n3. Generating insights...")
    insights = collatz.generate_insights()
    
    print("\nKEY INSIGHTS:")
    print("-" * 40)
    for key, value in insights.items():
        if key not in ['numbers_with_longest_sequences', 'numbers_with_highest_peaks', 'execution_statistics']:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\nTop 5 Longest Sequences:")
    for item in insights['numbers_with_longest_sequences']:
        print(f"  {item['starting_number']}: {item['sequence_length']} steps")
    
    print("\nTop 5 Highest Peaks:")
    for item in insights['numbers_with_highest_peaks']:
        print(f"  {item['starting_number']}: peak at {item['max_value']}")
    
    # Example 4: Create visualizations
    print("\n4. Creating visualizations...")
    collatz.create_visualizations()
    
    # Example 5: Save data
    print("\n5. Saving data...")
    collatz.save_data()
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\nFiles generated:")
    print("- collatz_data.csv: Raw analysis data")
    print("- collatz_analysis.png: Comprehensive visualizations")
    print("- collatz_sequence_*.png: Individual sequence plots")

if __name__ == "__main__":
    main()
