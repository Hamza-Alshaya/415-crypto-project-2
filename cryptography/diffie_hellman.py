import sys
sys.path.append('./')
from util.config_file import dh_g as g, dh_p as p

def generator(secret):
    return pow(g, secret, p)

def agreement(public, secret):
    shared_secret = pow(public, secret, p)
    return shared_secret

'''
#test driver
alice_secret =  123132
bob_secret =    124124
alice_public = generator(alice_secret)
bob_public = generator(bob_secret)
print('alice, bob public = ', alice_public, bob_public)
print('agreements = ', agreement(alice_public, bob_secret), agreement(bob_public, alice_secret))
'''