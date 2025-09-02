from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import io
from datetime import datetime
import time
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app)

class CollatzAnalyzer:
    """Simplified Collatz analyzer for web API"""
    
    def __init__(self):
        self.data = []
    
    def collatz_sequence(self, n: int) -> List[int]:
        """Generate Collatz sequence for a given number"""
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
    
    def analyze_sequence(self, n: int) -> Dict[str, Any]:
        """Analyze a single Collatz sequence"""
        start_time = time.time()
        sequence = self.collatz_sequence(n)
        execution_time = time.time() - start_time
        
        # Find peak value and its position
        max_value = max(sequence)
        peak_index = sequence.index(max_value)
        
        return {
            'starting_number': n,
            'sequence_length': len(sequence),
            'max_value': max_value,
            'steps_to_peak': peak_index,
            'total_steps': len(sequence) - 1,
            'peak_value': max_value,
            'sequence': sequence,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_range(self, start_range: int, end_range: int) -> List[Dict[str, Any]]:
        """Analyze a range of numbers"""
        results = []
        for n in range(start_range, end_range + 1):
            try:
                analysis = self.analyze_sequence(n)
                results.append(analysis)
            except Exception as e:
                print(f"Error processing {n}: {e}")
                continue
        return results
    
    def generate_insights(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights from analysis data"""
        if not data:
            return {"error": "No data available for analysis"}
        
        df = pd.DataFrame(data)
        
        insights = {
            'total_numbers_analyzed': len(data),
            'average_sequence_length': float(df['sequence_length'].mean()),
            'max_sequence_length': int(df['sequence_length'].max()),
            'min_sequence_length': int(df['sequence_length'].min()),
            'average_max_value': float(df['max_value'].mean()),
            'highest_peak_value': int(df['max_value'].max()),
            'average_steps_to_peak': float(df['steps_to_peak'].mean()),
            'numbers_with_longest_sequences': df.nlargest(5, 'sequence_length')[['starting_number', 'sequence_length']].to_dict('records'),
            'numbers_with_highest_peaks': df.nlargest(5, 'max_value')[['starting_number', 'max_value']].to_dict('records'),
            'execution_statistics': {
                'average_execution_time': float(df['execution_time'].mean()),
                'total_execution_time': float(df['execution_time'].sum()),
                'fastest_execution': float(df['execution_time'].min()),
                'slowest_execution': float(df['execution_time'].max())
            }
        }
        
        return insights

# Initialize analyzer
analyzer = CollatzAnalyzer()

@app.route('/')
def home():
    """Serve the main page"""
    return app.send_static_file('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_single():
    """Analyze a single number"""
    try:
        data = request.get_json()
        number = int(data.get('number', 1))
        
        if number <= 0:
            return jsonify({'error': 'Number must be positive'}), 400
        
        result = analyzer.analyze_sequence(number)
        
        # Convert sequence to string for JSON serialization
        result['sequence_str'] = ' → '.join(map(str, result['sequence']))
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-range', methods=['POST'])
def analyze_range():
    """Analyze a range of numbers"""
    try:
        data = request.get_json()
        start_num = int(data.get('start', 1))
        end_num = int(data.get('end', 100))
        
        if start_num <= 0 or end_num <= 0:
            return jsonify({'error': 'Numbers must be positive'}), 400
        
        if start_num > end_num:
            start_num, end_num = end_num, start_num
        
        # Limit range to prevent server overload
        if end_num - start_num > 1000:
            return jsonify({'error': 'Range too large. Maximum 1000 numbers allowed.'}), 400
        
        results = analyzer.analyze_range(start_num, end_num)
        insights = analyzer.generate_insights(results)
        
        # Convert sequences to strings for JSON serialization
        for result in results:
            result['sequence_str'] = ' → '.join(map(str, result['sequence']))
        
        return jsonify({
            'success': True,
            'data': results,
            'insights': insights
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-csv', methods=['POST'])
def download_csv():
    """Generate and download CSV file"""
    try:
        data = request.get_json()
        results = data.get('data', [])
        
        if not results:
            return jsonify({'error': 'No data to export'}), 400
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        # Remove sequence column for CSV export
        if 'sequence' in df.columns:
            df = df.drop('sequence', axis=1)
        
        # Create CSV in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Create response
        response = app.response_class(
            csv_buffer.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=collatz_analysis.csv'}
        )
        
        return response
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

