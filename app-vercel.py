from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import time
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app)

def collatz_sequence(n: int) -> List[int]:
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

def analyze_sequence(n: int) -> Dict[str, Any]:
    """Analyze a single Collatz sequence"""
    start_time = time.time()
    sequence = collatz_sequence(n)
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

@app.route('/')
def home():
    """Home page"""
    return jsonify({
        'message': 'Collatz Conjecture API',
        'endpoints': {
            '/api/analyze': 'POST - Analyze single number',
            '/api/analyze-range': 'POST - Analyze range of numbers',
            '/api/health': 'GET - Health check'
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_single():
    """Analyze a single number"""
    try:
        data = request.get_json()
        number = int(data.get('number', 1))
        
        if number <= 0:
            return jsonify({'error': 'Number must be positive'}), 400
        
        result = analyze_sequence(number)
        
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
        
        results = []
        for n in range(start_num, end_num + 1):
            try:
                analysis = analyze_sequence(n)
                results.append(analysis)
            except Exception as e:
                print(f"Error processing {n}: {e}")
                continue
        
        return jsonify({
            'success': True,
            'data': results,
            'total_analyzed': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'message': 'Collatz Conjecture API is running!'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
