from multiprocessing.dummy.connection import Connection
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'bot',
    'password': '',
    'database': 'apdcl_chat bot'
}

@app.route('/user_information/<int:consumer_no>', methods=['GET'])
def get_user_information(consumer_no):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT Name, phone_no, Address, meter_no FROM user_information where Consumer_no = %s"
        cursor.execute(query,(consumer_no,))
        data = cursor.fetchall()

        for row in data:
            user_info = {
                'name': row[0], 
                'phone_no': row[1],
                'address': row[2],
                'meter_no': row[3]
            }


        cursor.close()
        connection.close()

        return jsonify(user_info)
    

    except Exception as e:
        return jsonify({'error': str(e)})





#new api for bills
@app.route('/check_bills', methods=['GET'])
def check_bills():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT `Bill_id`, `Bill_amount`, `Due_date` FROM `bill_information` WHERE `Bill_id` = %s"
        cursor.execute(query, (101,))
        result = cursor.fetchall()
        for bill in result:
            bill_dict = {
                "Bill_id": bill[0],
                "Bill_amount": bill[1],
                "Due_date": bill[2]
            }
        return jsonify(bill_dict)
    except Exception as e:
        return jsonify({"error": str(e)})
    # return "hello"


#complaint
@app.route('/complaints', methods=['GET'])
def complaints ():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT `Complaint_id`, `Consumer_no`, `Complaint_date` FROM `customer_complaints` WHERE `Complaint_id` = 1022"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            complaint_dict = {
                "Complaint_id": result[0],
                "Consumer_no": result[1],
                "Complaint_date": result[2]
            }
        return jsonify(complaint_dict)
    except Exception as e:
        return jsonify({"error": str(e)})






#service
@app.route('/service', methods=['GET'])
def get_service():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT `Disconnection_id`, `Consumer_no`, `Disconnection_date` FROM `disconnected_services` WHERE `Disconnection_id` = 222"
        cursor.execute(query)
        service = cursor.fetchone()

        if service:
            service_dict = {
                "Disconnection_id": service[0],
                "Consumer_no": service[1],
                "Disconnection_date": service[2]
            
            }
        return jsonify(service_dict)
        
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
