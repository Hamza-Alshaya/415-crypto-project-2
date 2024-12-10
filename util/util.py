#convert a string to encoded utf-8 bytes, then convert those bytes to an integer
def encode_string(input_string):
    encoded_bytes = input_string.encode('ascii')
    encoded_integer = int.from_bytes(encoded_bytes, byteorder='big')
    return encoded_integer

#reverse operation: convert an integer to bytes, then decode the bytes to an ascii string
def decode_string(input_encoded_integer):
    decoded_bytes = input_encoded_integer.to_bytes((input_encoded_integer.bit_length() + 7) // 8, byteorder='big')
    decoded_message = decoded_bytes.decode('ascii')
    return decoded_message