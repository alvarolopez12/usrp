from gnuradio import gr
import numpy as np
import statistics
import random

class L(list):
    def append(self, item):
        list.append(self, item)
        if len(self) > 10: del self[0]

class mac(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="MAC",
            in_sig=[np.float32],
            out_sig=None
            )

        self.channels = {
            "ch1": 2410000000,
            "ch2": 2420000000,
            "ch3": 2430000000,
            "ch4": 2440000000,
            "ch5": 2450000000,}

        self.channel = self.channels['ch1']
        self.l = L()

        # Message ports
        self.message_port_register_out(gr.pmt.intern("channel"))
       
    def work(self, input_items, output_items):

        self.l.append(statistics.mean(input_items[0]))

        if statistics.mean(self.l) > 190:
            self.channel = random.choice(list(self.channels.values()))
            self.message_port_pub(gr.pmt.intern('channel'), gr.pmt.to_pmt({'freq': self.channel }))
        else:
            self.message_port_pub(gr.pmt.intern('channel'), gr.pmt.to_pmt({'freq': self.channel }))

        print (str(statistics.mean(self.l)) + "   " + str(self.channel))
        return (len(input_items[0]))
        
       
  

