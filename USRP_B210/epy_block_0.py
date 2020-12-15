from gnuradio import gr
import re
import numpy as np
import time
import re


class mac(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="MAC",
            in_sig=[np.float32],
            out_sig=None
            )
        # Message portsw
        self.message_port_register_out(gr.pmt.intern("transmit_packet"))
        self.message_port_register_in(gr.pmt.intern("time_unit"))
        self.message_port_register_in(gr.pmt.intern("ack"))
        self.set_msg_handler(gr.pmt.intern('time_unit'), self.send_packet)
        self.set_msg_handler(gr.pmt.intern('ack'), self.ack_handler)
        self.sensing_input = 0
        self.interation_wait_ack = 30 # interation_wait_ack * 3ms = 30ms waiting
        self.packet_num_send = 0
        self.packet_num_received = -1
        self.transmit = True
        
        
    def ack_handler(self, msg):
        
        msg_vec = gr.pmt.cdr(msg)

        # Convert the PMT vector into a Python list
        msg_data = []
        for i in range(48):
            msg_data.append(gr.pmt.u8vector_ref(msg_vec, i))
            
        a = 0           
        for i in msg_data[1:]:
            a = a + i
        
        self.packet_num_received =  a * 255 + msg_data[0]

        # print(self.packet_num_received)
                
        
    def send_packet(self, msg):
    
        # White space and ACK of the last packet received
        if (self.sensing_input < 3000 and self.transmit == True):
        
            # Set up the pdu body with the number of the packet
            send_str = self.packet_num_send.to_bytes(48, 'little', signed=True) 
            send_pmt = gr.pmt.make_u8vector(len(send_str), 0)
        
            for i in range(len(send_str)):
                gr.pmt.u8vector_set(send_pmt, i, send_str[i])
        
            msg = gr.pmt.cons(gr.pmt.PMT_NIL, send_pmt)   
            self.message_port_pub(gr.pmt.intern('transmit_packet'), msg)
            
            # Decrease the time out in one unit, take down the transmit flag and print sended packet number
            self.interation_wait_ack -= 1
            self.transmit = False
            print ("Transimitting packet number " + str(self.packet_num_send))

        # Spectrum busy
        elif self.sensing_input > 3000:
            print ("Waiting for the whitespace in the channel")
            
        # ACK Received, reestablish time out, increase packet number and flag
        elif (self.packet_num_received == self.packet_num_send):
            self.interation_wait_ack = 30
            self.packet_num_send += 1
            self.transmit = True
            print ("ACK of " + str(self.packet_num_send) + " received")
        
        elif (self.interation_wait_ack > 0 and self.packet_num_received != self.packet_num_send):
            self.interation_wait_ack -= 1
            self.transmit = False
        
        else:
            self.transmit = True
            print ("NACK of " + str(self.packet_num_send) + " received")
            print ("Retransmitting packet number " + str(self.packet_num_send))
            
        
    def work(self, input_items, output_items):
        self.sensing_input = sum(input_items[0]) / len(input_items[0]) 
        return (len(input_items[0]))
        
       
  

