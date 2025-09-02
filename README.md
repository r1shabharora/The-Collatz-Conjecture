# The Collatz Conjecture Analysis

A comprehensive Python application that demonstrates and analyzes the Collatz Conjecture using data science techniques, pandas for data management, and matplotlib/seaborn for visualizations.

## What is the Collatz Conjecture?

The Collatz Conjecture is one of the most famous unsolved problems in mathematics. It states that for any positive integer n:

1. If n is even, divide it by 2
2. If n is odd, multiply it by 3 and add 1
3. Repeat until you reach 1

The conjecture claims that this process will always reach 1, regardless of which positive integer is chosen to start the sequence.

**Example**: Starting with n = 6
- 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1

## Features

### 🔢 Core Functionality
- **Sequence Generation**: Generate Collatz sequences for any positive integer
- **Batch Analysis**: Analyze multiple numbers simultaneously
- **Performance Tracking**: Monitor execution times and computational efficiency

### 📊 Data Analysis & Insights
- **Comprehensive Metrics**: Track sequence length, peak values, steps to peak, and more
- **Statistical Analysis**: Calculate averages, distributions, and correlations
- **Pattern Recognition**: Identify numbers with longest sequences and highest peaks

### 📈 Visualizations
- **Individual Sequence Plots**: Visualize specific Collatz sequences with both linear and log scales
- **Distribution Analysis**: Histograms and box plots showing sequence characteristics
- **Correlation Analysis**: Heatmaps showing relationships between different metrics
- **Performance Analysis**: Execution time vs sequence length relationships
- **Top Performers**: Bar charts showing numbers with longest sequences

### 💾 Data Management
- **Pandas Integration**: Store all data in structured DataFrames
- **CSV Export**: Save analysis results for further processing
- **Timestamp Tracking**: Record when each analysis was performed

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the main script to see a complete demonstration:

```bash
python collatz_conjecture.py
```

This will:
1. Analyze individual sequences for numbers 27, 97, 871, and 6171
2. Perform batch analysis on numbers 1-1000
3. Generate comprehensive insights and statistics
4. Create multiple visualizations
5. Save data to CSV files

### Advanced Usage

You can also use the `CollatzConjecture` class programmatically:

```python
from collatz_conjecture import CollatzConjecture

# Initialize the analyzer
collatz = CollatzConjecture()

# Analyze a single number
analysis = collatz.analyze_sequence(27)
print(f"Sequence length: {analysis['sequence_length']}")
print(f"Peak value: {analysis['max_value']}")

# Analyze a range of numbers
data = collatz.run_analysis(1, 100)

# Generate insights
insights = collatz.generate_insights()
print(insights)

# Create visualizations
collatz.create_visualizations()

# Plot individual sequence
collatz.plot_individual_sequence(27)

# Save data
collatz.save_data('my_analysis.csv')
```

## Output Files

The application generates several output files:

- **`collatz_data.csv`**: Raw analysis data in CSV format
- **`collatz_analysis.png`**: Comprehensive dashboard with 9 different visualizations
- **`collatz_sequence_*.png`**: Individual sequence plots for specific numbers

## Key Insights You Can Discover

### Mathematical Patterns
- **Sequence Length Distribution**: Most sequences are relatively short, but some can be very long
- **Peak Values**: Some numbers reach surprisingly high values before converging to 1
- **Correlation Analysis**: Relationships between starting numbers and sequence characteristics

### Computational Insights
- **Performance Patterns**: How execution time relates to sequence length
- **Efficiency Analysis**: Which numbers require the most computational resources
- **Scalability**: How the system performs with larger datasets

### Notable Numbers
- **Longest Sequences**: Numbers that take the most steps to reach 1
- **Highest Peaks**: Numbers that reach the largest values during their sequence
- **Interesting Patterns**: Numbers that exhibit unusual behavior

## Example Analysis Results

For the range 1-1000, you might discover:
- Average sequence length: ~17 steps
- Longest sequence: ~178 steps (for number 871)
- Highest peak: ~250,504 (for number 871)
- Most sequences reach their peak within the first few steps

## Technical Details

### Data Structure
The application tracks the following metrics for each analyzed number:
- `starting_number`: The initial number
- `sequence_length`: Total number of values in the sequence
- `max_value`: Highest value reached during the sequence
- `steps_to_peak`: Number of steps to reach the maximum value
- `total_steps`: Total number of operations performed
- `execution_time`: Time taken to compute the sequence
- `timestamp`: When the analysis was performed

### Visualization Types
1. **Histograms**: Distribution of sequence lengths and steps to peak
2. **Scatter Plots**: Relationships between different metrics
3. **Correlation Heatmap**: Statistical relationships between variables
4. **Box Plots**: Statistical summaries of distributions
5. **Bar Charts**: Top performers in various categories
6. **Line Plots**: Individual sequence trajectories

## Contributing

Feel free to extend this project with additional features:
- Parallel processing for faster batch analysis
- Additional mathematical metrics and patterns
- Interactive visualizations using Plotly or Bokeh
- Machine learning analysis of sequence patterns
- Web interface for easy interaction

## Mathematical Background

The Collatz Conjecture remains unproven despite extensive computational verification. As of 2023, it has been verified for all numbers up to 2^68. This project helps explore the patterns and characteristics of these fascinating sequences.

## License

This project is open source and available under the MIT License.

---

**Note**: This is a demonstration project for educational and research purposes. The Collatz Conjecture itself remains an unsolved mathematical problem.

