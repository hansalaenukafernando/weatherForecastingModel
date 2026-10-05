from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
# Oya kalin hadapu models (rf_model, xgb_model, final_lstm) saha 
# dataset eka (df, X, y) me file eke load karaganna awashyai.

app = Flask(__name__)

@app.route('/')
def index():
    # Meken index.html file eka load karanawa
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        target_date = data.get('date')
        
        # Dataset eken date eka hoyaganima
        target_index = df[df['Date Time'] == target_date].index[0]
        actual_temp = float(y.iloc[target_index])

        # Predictions ganeema
        tabular_data = X.iloc[[target_index]]
        lookback_data = X.iloc[target_index - 6 : target_index].values
        sequence_data = lookback_data.reshape(1, 6, X.shape[1])

        rf_pred = float(rf_model.predict(tabular_data)[0])
        xgb_pred = float(xgb_model.predict(tabular_data)[0])
        lstm_pred = float(final_lstm.predict(sequence_data, verbose=0)[0][0])

        return jsonify({
            'success': True,
            'actual': round(actual_temp, 2),
            'rf': round(rf_pred, 2),
            'xgb': round(xgb_pred, 2),
            'lstm': round(lstm_pred, 2)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)