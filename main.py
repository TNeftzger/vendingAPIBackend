from flask import Flask, request, make_response
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)

# Use while loop to decipher whether coin is $.25

# Var to handle coins
currency = 0


# Soda dict for data
soda = {
    1: {"flavor": "Coke", "price": 2, "quantity": 5},
    2: {"flavor": "Pepsi", "price": 2, "quantity": 5},
    3: {"flavor": "Dr. Pepper", "price": 2, "quantity": 5}
}

# Meet the array requirements for inventory
quantityArray = []


# Defining a money class to handle the / endpoint
class money(Resource):
    # GET for testing purposes
    def get(self):
        return currency


    # PUT to update coin
    def put(self):
        global currency
        coin = int(request.form["coin"])
        if coin == 1:
            currency = currency + coin
            customResponse = make_response("X-Coins:" + str(currency))
            customResponse.headers["X-Coins: "] = str(currency)
            customResponse.status_code = 204
            return customResponse
        else:
            return "You must enter a coin and only one coin."


    # DELETE to return coins entered into the vending machine
    def delete(self):
        global currency
        moneyReturned = currency
        currency = 0
        customResponse = make_response("X-Coins:" + str(moneyReturned))
        customResponse.headers["X-Coins: "] = str(moneyReturned)
        customResponse.status_code = 204
        return customResponse


# Defining an inventory class to handle the /inventory endpoint
class inventory(Resource):
    def get(self):
        # Updated to deliver array of integers for quantity
        quantityArray = [int(soda[1]['quantity']),int(soda[2]['quantity']),int(soda[3]['quantity'])]
        # Originally returned soda dictionary
        return quantityArray


# Defining a stock class to handle the /inventory/<id> endpoint
class stock(Resource):
    def get(self, id):
        return int(soda[id]['quantity'])# Updated to return an integer as specified in directions


    # PUT to handle transaction endpoint
    def put(self, id):
        global currency
        initialInventoryCount = soda[id]['quantity']
        if initialInventoryCount == 0:
            customResponse = make_response("Out of stock. Please choose another item.")
            customResponse.headers["X-Coins: "] = str(currency)
            customResponse.status_code = 404
            return customResponse
        elif currency <= 1:
            customResponse = make_response("All sodas cost 2 coins. Please enter more money.")
            customResponse.headers["X-Coins: "] = str(currency)
            customResponse.status_code = 403
            return customResponse
        else:
            finalInventoryCount = initialInventoryCount - 1
            moneyReturned = currency - 2
            currency = 0
            soda[id]['quantity'] = finalInventoryCount
            customResponse = make_response("X-Coins: " + str(moneyReturned))
            customResponse.headers["X-Coins: "] = str(moneyReturned)
            customResponse.headers["X-Inventory-Remaining: "] = str(soda[id]['quantity'])
            customResponse.status_code = 200
            return customResponse



# Endpoint resources with parameters
api.add_resource(money, "/")
api.add_resource(inventory, "/inventory")
api.add_resource(stock, "/inventory/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
