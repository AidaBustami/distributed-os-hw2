from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask import  request, jsonify
from sqlalchemy.orm import load_only
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class catalog(db.Model):
	item_id = db.Column(db.String, primary_key=True)
	number_in_stock = db.Column(db.Integer ,nullable=False)
	cost=  db.Column(db.Integer, nullable=False)
	topic = db.Column(db.String(100), nullable=False)
	titel=db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"catalog2(number_in_stock = {number_in_stock}, cost = {cost}, topic = {topic},titel={titel})"



	

	
		
db.create_all()
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('item_id', 'number_in_stock', 'cost', 'topic','titel')


class ProductSchema2(ma.Schema):
  class Meta2:
    fields = ('item_id','titel')
# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
products_schema2=ProductSchema2(many=True)
catalog_put_args = reqparse.RequestParser()
catalog_put_args.add_argument("number_in_stock", type=int, help="#stock not avalible", required=True)
catalog_put_args.add_argument("cost", type=int, help="cost not", required=True)
catalog_put_args.add_argument("topic", type=str, help="topic not", required=True)
catalog_put_args.add_argument("titel", type=str, help="topic not", required=True)
catalog_update_args = reqparse.RequestParser()
catalog_update_args.add_argument("number_in_stock", type=int, help="#stock not avalible", required=False)
catalog_update_args.add_argument("cost", type=int, help="cost not" ,required=False)
catalog_update_args.add_argument("topic", type=str, help="topic not",required=False)



catalog_put_args999 = reqparse.RequestParser()
catalog_put_args999.add_argument("number_in_stock", type=int, help="#stock not avalible", required=False)
catalog_put_args999.add_argument("cost", type=int, help="cost not", required=False)
catalog_put_args999.add_argument("topic", type=str, help="topic not", required=False)
catalog_put_args999.add_argument("titel", type=str, help="topic not", required=False)





catalog_update_args2 = reqparse.RequestParser()

catalog_update_args2.add_argument("item_id", type=str, help="#id")

catalog_update_args2.add_argument("topic", type=str, help="topic not")



catalog77_update_args = reqparse.RequestParser()

catalog77_update_args.add_argument("item_id", type=str, help="#id")


catalog88_update_args = reqparse.RequestParser()

catalog88_update_args.add_argument("cost", type=int, help="#id")
catalog88_update_args.add_argument("number_in_stock", type=int, help="#id")


resource_fields = {
	'item_id': fields.String,
	'number_in_stock': fields.Integer,
	'cost': fields.Integer,
	'topic': fields.String

	 
}

class catalog7(Resource):
	def patch(self ):
		args = catalog77_update_args.parse_args()
		result = catalog.query.filter_by(item_id=args['item_id']).first()
		if not result:
			return ({"exsist" :-1 }) 
		elif(result.number_in_stock)>0:
			x=result.number_in_stock
			result.number_in_stock = result.number_in_stock -1
			db.session.commit()
			return({"exsist" :x })

		    
		
		else:
		    return ({"exsist" :-2 })

		

api.add_resource(catalog7, "/book2")
class catalog2(Resource):
	@marshal_with(resource_fields)
	def get(self):
		args = catalog_update_args2.parse_args()
		t= not args['item_id']
		y=not args['topic']
		if t and y :
			
			abort(404,message="spesify in the body of  the message the topic if yoy want to search using cost or  spesify iteme id if you want to search by item id ")
		if args['item_id']:
			result = catalog.query.filter_by(item_id=args['item_id']).first()
			if not result:
				abort(404,message="book with this id does not exsist")
		elif args['topic']:
			all_products = catalog.query.filter_by(topic=args['topic']).all()
			result = products_schema.dump(all_products)
            
            
			
		if not result:
			abort(404, message="this topic does not exsist")
		
		return result
api.add_resource(catalog2, "/get_by_id_or_by_topic")
class catalog3(Resource):
	@marshal_with(resource_fields)
	def put(self, book_id):
		args = catalog_put_args.parse_args()
		result = catalog.query.filter_by(item_id=book_id).first()
		if result:
			abort(409, message="book id already  taken...")

		video = catalog(item_id=book_id, number_in_stock=args['number_in_stock'], cost=args['cost'], topic=args['topic'],titel=args['titel'])
		db.session.add(video)
		db.session.commit()
		return video, 201
api.add_resource(catalog3, "/create_book1/<int:book_id>")
class catalog4(Resource):
	#@marshal_with(resource_fields)
	def post(self, video_id):
		args = catalog_update_args.parse_args()
		result = catalog.query.filter_by(item_id=video_id).first()
		if not result:
			abort(404, message="book doesn't exist")
		x=	not args['number_in_stock']
		y=  not  args['cost']
		z=  not args['topic']
		if x and y and z:
			return jsonify({"message" : "spesify one at least of the cost or topic or number_in_stock"})
		if args['number_in_stock']:
			result.number_in_stock = args['number_in_stock']
		if args['cost']:
			result.cost = args['cost']
		if args['topic']:
			result.topic = args['topic']	
		db.session.commit()
		return  product_schema.jsonify(result)

api.add_resource(catalog4, "/update_book_cost_or_topic_or_number_in_stock/<int:video_id>")



@app.route('/GET_ALL_BOOKS', methods=['GET'])
def get_products():
  all_products = catalog.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)
	


@app.route('/update_book_cost_and_number_in_stock/<id>', methods=['POST'])
def update_product(id):
	args = catalog88_update_args.parse_args()
	product = catalog.query.get(id)
	x= args['number_in_stock']
	y= args['cost']
	if(x):
	  number_in_stock = request.json['number_in_stock']
	  product.number_in_stock = number_in_stock
	if(y) :
	  cost = request.json['cost']
	  product.cost = cost  
	db.session.commit()
	return product_schema.jsonify(product)



    
    






@app.route('/book_decraese_in_stock', methods=['POST'])
def update_product5():
	catalog89_update_args = reqparse.RequestParser()
	catalog89_update_args.add_argument("item_id", type=str, help="#id")
	args = catalog89_update_args.parse_args()
	product = catalog.query.get(args['item_id'])
	output2 =[]
	user_data = {}
	
	
		

		
	
	if not product :
		user_data['titel'] = None
		user_data['item_id'] = None
		user_data['cost'] = None
		user_data['number_in_stock'] = None
		output2.append(user_data)
		return jsonify (output2)

	
	
	

    
	
	
	user_data['titel'] = "zero"
	user_data['item_id'] = "zero"
	user_data['cost'] = "zero"
	user_data['number_in_stock'] = "zero"

	if product.number_in_stock == 0:
		output2.append(user_data)
		return jsonify (output2)

	  
	user_data['titel'] = product.titel
	user_data['item_id'] = product.item_id
	user_data['cost'] = product.cost
	
	product.number_in_stock = product.number_in_stock -1
	db.session.commit()
	user_data['number_in_stock'] = product.number_in_stock
	output2.append(user_data)
	
	return jsonify (output2)




    
	    
    
	
	



  
  

  
  

@app.route('/book_incraese_in_stock', methods=['POST'])

def update_product6():
	catalog89_update_args = reqparse.RequestParser()
	catalog89_update_args.add_argument("item_id", type=str, help="#id")
	args = catalog89_update_args.parse_args()
	product = catalog.query.get(args['item_id'])
	if not product :
		return  None
	product.number_in_stock = product.number_in_stock + 1
	db.session.commit()
	return product_schema.jsonify(product)  






    
    
	  

  
  

  
  

  

  





@app.route('/delete_book/<id>', methods=['DELETE'])
def delete_product(id):
  product = catalog.query.get(id)
  if not product:
	  return jsonify({'message' : 'book does not exsit!'})
  db.session.delete(product)
  db.session.commit()

  return  jsonify({"message" :" book has  been deleted" })


@app.route('/new_book/<id>', methods=['POST'])
def add_product(id):
	
  
  product = catalog.query.get(id)
  if product:
	  return  jsonify({"message" : "already existing  book" })
  args = catalog_put_args999.parse_args()
  
  if (not args['cost'] ) or  (not args['topic']) or   (not args['titel']) or  (not args ['number_in_stock']) :
	  return  jsonify({"message" :" please enter cost and topic and titel and number_in_stock in  body in json format" })
  cost = request.json['cost']
  topic = request.json['topic']
  titel = request.json['titel']	  
  number_in_stock=request.json['number_in_stock']	
	    
  new_product = catalog(item_id=id,cost=cost, topic=topic, titel=titel, number_in_stock=number_in_stock)
  db.session.add(new_product)
  db.session.commit()
  return product_schema.jsonify(new_product)




@app.route('/lookup', methods=['GET'])
def get_product_byid():
	catalog89_update_args = reqparse.RequestParser()
	catalog89_update_args.add_argument("item_id", type=str, help="#id")
	args = catalog89_update_args.parse_args()
	product = catalog.query.get( args['item_id'])
	if not product :
		return None
	return product_schema.jsonify(product)	

    
	

  

@app.route('/search', methods=['GET'])
def get_product_bytopic():
	catalog89_update_args = reqparse.RequestParser()
	catalog89_update_args.add_argument("topic", type=str, help="#id")
	args = catalog89_update_args.parse_args()
	
	





	

	all_products = catalog.query.filter_by(topic=args['topic']).all()
	if not all_products :
	  return None
	#begin
	output = []
	for p in all_products:
		user_data = {}
		user_data['titel'] = p.titel
		user_data['item_id'] = p.item_id
		output.append(user_data)
	return jsonify( output)
	#end




	

    
        
        
        
        
        

    
	 
	#result = products_schema.dump(all_products)
	#return jsonify(result)
	'''output = {}
	for booky in all_products:
		output[booky.titel]=booky.item_id
		
	return jsonify({'items' : output})	'''



     
      

    

	



    


@app.route('/updatecost_by_json/<id>', methods=['PUT'])
def update_product_cost_by_json(id):
  product = catalog.query.get(id)
  if( not product):
	  return "no  such book like that"
  
  catalog_update_args2 = reqparse.RequestParser()
  catalog_update_args2.add_argument("cost", type=int, help="#id")
  args = catalog_update_args2.parse_args()
  cost = request.json['cost']
  if(cost==0) :
	  product.cost = cost
	  
  elif not args['cost'] :
	  return " please spesify cost as json object"
  	 
  elif(cost<0) :
	  return "cosst can not be nagative"
  else :

	  product.cost = cost
  db.session.commit()  
  return product_schema.jsonify(product)  



  
  
    

@app.route('/updatecost_by_url/<id>/<cost>', methods=['PUT'])
def update_product_cost_url(id,cost):
  product = catalog.query.get(id)
  if( not product):
	  return "no  such book like that"
  if(int(cost) <0):
	  return "cost can not be  negative"
  product.cost = cost
  db.session.commit()
  return product_schema.jsonify(product)
@app.route('/updatetopicbyjson/<id>', methods=['PUT'])
def update_product_topic_by_json(id):
  product = catalog.query.get(id)
  if( not product):
	  return "no  such book like that"
  
  catalog_update_args2 = reqparse.RequestParser()
  catalog_update_args2.add_argument("topic", type=str, help="#id")
  args = catalog_update_args2.parse_args()
  if not args['topic'] :
	  return " please spesify topic as json object"
  topic = request.json['topic']	  
  product.topic = topic
  db.session.commit()
  return product_schema.jsonify(product)    

@app.route('/updatetopic_by_url/<id>/<topic>', methods=['PUT'])
def update_product_topic_url(id,topic):
  product = catalog.query.get(id)
  if( not product):
	  return "no  such book like that"
  
  product.topic = topic
  db.session.commit()
  return product_schema.jsonify(product)



	  
    
			

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port="6000")

