import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests 
from uuid import uuid4
from urllib.parse import urlparse

# create block chain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1 , previous_hash = '0') #this will create the genesis block(the first block)
        self.nodes = set()
        
    def create_block(self, proof, previous_hash):
        block = {
              
            'index':len(self.chain)+1,
            'timestamp': str(datetime.datetime.now()),
            'proof':proof,
            'previous_hash': previous_hash,
            'transactions' : self.transactions
        }
        self.transactions = [] # previous transaction needs to be empetied after inserting it in a mined block
        self.chain.append(block)
        
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            if(hash_operation[:4] == "0000"):
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        
        while(block_index < len(chain)):
            curr_block = chain[block_index]
            
            if(self.hash(previous_block) != curr_block['previous_hash']):
                return False
        
            previous_proof = previous_block['proof']
            curr_proof = curr_block['proof']
            
            hash_operation =  hash_operation = hashlib.sha256(str(curr_proof**2 - previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4] != "0000"):
                return False
            
            previous_block = curr_block
            block_index += 1
            
        return True
            
    
    def add_transactions(self , sender , receiver , amount):
        self.transactions.append({
            'sender' : sender,
            'receiver' : receiver,
            'amount' : amount
            })
        
        # this function returns the index of the new block where this transaction will be stored
        
        # return len(self.chain) + 1 # can we do this???????
    
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc #parsed_url.netloc= '127.0.0.1:5000'
    
                       
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        else:
                return False
    
    
    
    
    
# mining blockchain

# set up flask web app

app = Flask(__name__)

# creating an address for node on port 5000
node_addres = str(uuid4()).replace('-','')

# create an instance of Blockchain class
blockchain = Blockchain()

# mining a new block

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    curr_proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(sender=node_addres, receiver='Himanshu', amount=1) 
    
    mined_block = blockchain.create_block(curr_proof, previous_hash)
    
    response = {
        'message' : 'Congratulations, you just mined a new BLOCK',
        'index' : mined_block['index'],
        'timestamp' : mined_block['timestamp'],
        'proof' : mined_block['proof'],
        'previous_hash' : mined_block['previous_hash'],
        'transactions' : mined_block['transactions']
        }
    return jsonify(response),200

# getting full chain

@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
         }

    return jsonify(response),200

# check if chain is valid
@app.route('/is_valid',methods=['GET'])
def is_valid():
    
    if blockchain.is_chain_valid(blockchain.chain):
        response = {'valid' : 'True'}
    else:
        response = {'valid' : 'False'}
        
    return jsonify(response)


# post request to add a new transaction
@app.route('/add_transaction',methods=['POST'])
def add_transaction():
    json = request.get_json()
    transactions_keys = ['sender','receiver','amount']
    if not all [key in json for key in transactions_keys]:
        return 'some keys are missing in the transaction', 400 # bad request
    index = blockchain.add_transactions(json['sender'],json['receiver'],json['amount'])
    response = {'message' : f'This transaction will be added to block {index}'}
    return jsonify(response),201 # success code for post(creation)

# decentralising the blockchain

#connecting new nodes
@app.route('/connect_node',methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node',400
    
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message' : 'All the nodes are now connected. The monticoins blockchain contains the following nodes',
        'total_nodes' : list(blockchain.nodes)
        }
    
    return jsonify(response),201


# replacing the chain with the longest chain if needed
@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
                    'message' : 'The chain was replaced by the longest chain',
                    'new_chain' : blockchain.chain
                    }
    else:
        response = {
            'message' : 'The chain is longest',
            'actual_chain' : blockchain.chain
            }
        
    return jsonify(response),200

# running the app


app.run(host = '0.0.0.0' , port= 5000)











































   
   




            
            
            
            
            
            
            
            
            
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
