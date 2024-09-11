from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
csv_file = 'bank_branches.csv'
df = pd.read_csv(csv_file)

@app.route('/banks', methods=['GET'])
def get_banks():
    
    banks = df[['bank_id', 'bank_name']].drop_duplicates().to_dict(orient='records')
    return jsonify(banks)



@app.route('/branches', methods=['GET'])
def get_branches():
    
    bank_id = request.args.get('bank_id', type=int)

    
    if bank_id:
        branches = df[df['bank_id'] == bank_id]
    else:
        branches = df

    
    edges = [
        {
            "node": {
                "branch": row['branch'],
                "ifsc": row['ifsc'],
                "bank": {
                    "name": row['bank_name']
                }
            }
        } for _, row in branches.iterrows()
    ]

    return jsonify({"edges": edges})


if __name__ == "__main__":
    app.run(debug=True)
