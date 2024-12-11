#certificate format:
'''
"certificate" = {
    "id": "XXXXXX"
    "public_key": "YYYYYY"
    "signature": hash of the public key, encrypted by CA's private key
}
'''
#CSR format:
'''
A CSR must contain the following fields in JSON:
{"csr":
    {
        "id": "XXXXX",
        "public_key": "YYYYY"
    }
}
'''

import sys
sys.path.append('./')
from cryptography.asymmetric import rsa_encrypt, rsa_decrypt, generate_rsa_keys
from cryptography.md5 import md5_hash

from flask import Flask, request, jsonify
import json
app = Flask(__name__)

public_key, private_key = generate_rsa_keys()

issued_certificates = {}

#function that simulates signing a certificate request (CALLED AFTER VALIDATING THE REQUEST'S FORMAT).
def sign_certificate_request(csr):
    #print(f'CSR = {csr}\ntype:{type(csr)}\n\n')
    
    id, public_key = csr['id'], csr['public_key']
    signature = rsa_encrypt(md5_hash(public_key), private_key)
    
    #add a new entry to the dictionary
    issued_certificates[csr['id']] = {"id": id, "public_key": csr['public_key'], "signature": signature}
    
    print(f'\n==================\nCERTIFICATE GENERATED:\n-=-=-=-=-=\n{issued_certificates}\n-=-=-=-=-=\n==================')
    database = open('database.json', 'w')
    
    #output the database to a file
    with open("database.json", "w") as outputfile: 
        json.dump(issued_certificates, outputfile, indent=4)
    
    return f"Signed Certificate for CSR: {csr}"


#route for issuing an existing certificate.
@app.route('/certificates/<cert_id>', methods=['GET'])
def get_certificate(cert_id):
    """
    Retrieve an existing certificate by its ID.
    """
    cert = issued_certificates.get(cert_id)
    if cert:
        #return the certificate
        return jsonify({"status": "success", "certificate": cert}), 200
    else:
        #if the certificate is not found
        return jsonify({"status": "error", "message": "Certificate does not exist"}), 404
############################################

#route for creating and signing a certificate request.
@app.route('/certificates', methods=['POST'])
def create_and_sign_certificate():
    """
    Create and sign a certificate based on the provided Certificate Signing Request (CSR).
    """
    data = request.get_json()
    
    #print(f"\n\ndata.keys() = {data.keys()}\n\n")
    #if parent field did not adhere to the standard
    if str(data.keys()) != 'dict_keys([\'csr\'])':
        return jsonify({"status": "error", "message": "invalid CSR format: json should only contain one parent object: \"csr\" ."}), 400
    
    #if subfields did not adhere to the standard
    if (str(data['csr'].keys()) != ("dict_keys(['id', 'public_key'])")):
        return jsonify({"status": "error", "message": "invalid CSR format: subfields should only contain an id and a public key string."}), 400
     
    #if ID already exists in the database
    if (issued_certificates.get(data['csr']['id'])):
        return jsonify({"status": "error", "message": "invalid request: ID already exists in the database."}), 400
        
    #sign the certificate if all conditions were met.
    signed_certificate = sign_certificate_request(data['csr'])

    return jsonify({"status": "success", "message": signed_certificate, "certificate": issued_certificates[data['csr']['id']]}), 201
############################################

#route for obtaining the CA's public key for decrypting the signature
@app.route('/key', methods=['GET'])
def return_public_key():
    return jsonify({"status": "success", "public_key":public_key}), 200

if __name__ == '__main__':
    app.run(debug=True, port = 42021)
