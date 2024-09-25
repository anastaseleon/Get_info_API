from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from database import get_db_connection  

app = Flask(__name__)
CORS(app)  



@app.route('/getinfo', methods=['GET'])
def get_info():

    # Get product_id from the query params
    product_id = request.args.get('product_id', type=int)
    field = request.args.get('field')

    conn = None
    try:
        # Get a database connection
        conn = get_db_connection()
        
        # Create a cursor and execute the query with dynamic product_id
        cursor = conn.cursor()
        
        query = f'''
            SELECT {field} 
            FROM Api_view  
            WHERE ProductID = ?
        '''

        # Execute the query with the product_id parameter
        cursor.execute(query, (product_id,))

        # Fetch result
        result = cursor.fetchone()

        # Check if a result is found
        # Return only the value as raw text, without quotes
        response = make_response(str(result[0]), 200)
        response.mimetype = "text/plain"
        return response
        
    
    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
