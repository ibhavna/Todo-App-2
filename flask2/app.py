from flask import Flask, jsonify , request, render_template #jsonify is a method not the class hence reprensented with small letter
app = Flask(__name__) #__name__ is used to give the unique name, down there we would be creating 5 endpoints

stores = [
    {
        'name':'My Wonderful Store',
        'items' : [
            {
                'name' : 'My Item',
                'price' : 15.99
            }
        ]
    }
]  #we could've created above record in the database directly

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store', methods = ['POST']) #'/' indicates the homepage, as url for homepage ends with '/', we have used 'app.route' decorator, and a decorator is always followed by a function
def create_store():                               #BYDEFAULT app.route method will send get request, so we will specify the method = [POST,GET], we will write both to enable both
    request_data = request.get_json()  #.get_json automatically converts json string to python dictionary
    #print(request_data)
    #print(request_data['name'])
    new_store = {
        'name': request_data.get('name'),
        'items':[]
     }
     #print(new_store)
    stores.append(new_store)
    return jsonify(new_store) #return type shud be a string not a dict hence shud be of type jsonify
    
@app.route('/store/<string:name>') #eg:-http://127.0.0.1:50000/store/some_name (this name is the same variable as given in string:name)
def get_store(name):
    #to retrieve a store:-
    #iterate over stores
    for store in stores:
        if store['name'] == name: #if the store name matches, return it
            return jsonify(store)
    #if none matches return an error
    return jsonify({'message' : 'store not found'})

@app.route('/store') 
def get_stores():
    return jsonify({'stores' : stores}) #this is to convert the list type of store to dictionary type for jsonify

@app.route('/store/<string:name>/item', methods = ['POST']) 
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']
                        
            }
            store['items'].append(new_item)
            return jsonify(new_item)
        return jsonify({'message' : 'store not found'})


@app.route('/store/<string:name>/item') 
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name: 
            return jsonify({'items':store['items']}) #to reteieve item
    return jsonify({'message':'store not found'})
    

if __name__== '__main__':
    app.run(port=8000,debug=True)
#we've to tell our browser here, that when and where to run
#port is the area where the app will return and throw responses from
#Running on http://127.0.0.1:50000/  - this ip-address is reserved for our computer to access the page of our flask app
#rest api in flask returns string usually which can be dealt with javascript
#going to a webpage will always do a GET Request and will return HTML, But we can return other things as well

#POST - Used to receive data (but browser will use it to send data)
#GET - Used to send data back only (but browser will use it to get the data)
