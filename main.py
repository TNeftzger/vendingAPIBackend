from flask import Flask, request, make_response
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)

# Var to handle coins
currency = 0


# Soda dict for data
soda = {
    1: {"flavor": "Coke", "price": 2, "count": 5},
    2: {"flavor": "Pepsi", "price": 2, "count": 5},
    3: {"flavor": "Dr. Pepper", "price": 2, "count": 5}
}


# Defining a money class to handle the / endpoint
class money(Resource):
    # GET for testing purposes
    def get(self):
        return currency


    # PUT to update coin
    def put(self):
        global currency
        coin = int(request.form['coin'])
        if coin == 1:
            currency = currency + coin
            customResponse = make_response("X-Coins:" + str(currency))
            customResponse.headers["X-Coins: "] = str(currency)
            customResponse.status_code = 204
            return customResponse
        else:
            return "You must enter only one coin"


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
        return soda


# Defining a stock class to handle the /inventory/<id> endpoint
class stock(Resource):
    def get(self, id):
        return soda[id]


    # PUT to handle transaction endpoint
    def put(self, id):
        global currency
        initialInventoryCount = soda[id]['count']
        purchaseAmount = int(currency / 2)
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
            finalInventoryCount = initialInventoryCount - purchaseAmount
            if finalInventoryCount < 0:
                moneyReturned = currency - (soda[id]['count']*2)
                currency = 0
                soda[id]['count'] = 0
                customResponse = make_response("X-Coins: " + str(moneyReturned))
                customResponse.headers["X-Coins: "] = str(moneyReturned)
                customResponse.headers["X-Inventory-Remaining: "] = str(soda[id]['count'])
                customResponse.status_code = 200
                return customResponse
            else:
                moneyReturned = currency % 2
                currency = 0
                soda[id]['count'] = finalInventoryCount
                customResponse = make_response("X-Coins: " + str(moneyReturned))
                customResponse.headers["X-Coins: "] = str(moneyReturned)
                customResponse.headers["X-Inventory-Remaining: "] = str(soda[id]['count'])
                customResponse.status_code = 200
                return customResponse


# Endpoint resources with parameters
api.add_resource(money, "/")
api.add_resource(inventory, "/inventory")
api.add_resource(stock, "/inventory/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
