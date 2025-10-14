from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load data and similarity matrix
data = joblib.load('song_list.pkl')
similarity = joblib.load('similarity.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['input']
    user_input_lower = user_input.lower()
    
    # Find index of song matching user input
    index_list = data[data['combined'].str.lower().str.contains(user_input_lower)].index.tolist()
    
    if not index_list:
        return jsonify({'error': 'Song not found in dataset.'})
    
    index = index_list[0]
    
    # Calculate similarity scores
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    # Top 5 recommendations
    top_songs = [data['Title'][i] for i, _ in scores[1:6]]
    
    return jsonify({'recommendations': top_songs})

if __name__ == '__main__':
    app.run(debug=True)