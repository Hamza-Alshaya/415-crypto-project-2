###General Configuration
#alice is server
alice_ip = "127.0.0.1"
alice_port = 50501
alice_connection_flag = False

#bob is client
bob_port = 50502
bob_connection_flag = False
#############################################
###RSA configuration:
# Change the size of the RSA key here
rsa_key_size = 2048
#############################################
###Diffie-Hellman configuration
# Set the values of p and g to a specified large prime number
# g will be risen to some power, p will be used as a right modulo operand
# larger p > higher range of selection
# BOTH VALUES MOST BE PRIME
dh_g = 2687
dh_p = 839903
#############################################