#!  /usr/bin/env python

class KeyInput:
    
    def __init__(self, pel, mode='y/n'):
        self.mode=mode
        self.pel=pel
        
    def log_err(self, msg):
        print msg
        self.pel.set(msg)
    
    def get_yesno(self,question, ermsg=""):
        inp = raw_input(question+" ["+self.mode+"]:")
        while True:
            if inp.find("yes") != -1 or inp.find("y") != -1:
                return True
    
            if inp.find("no") != -1 or inp.find("n") != -1:
                self.log_err(ermsg)
                return False
    
            inp = raw_input('Enter "yes" or "no" to continue:')
    
    def bit_indep(self,question,_func,check):
        #While loop to check each bit independently
        print "not define"
            
    def msg_cont(self,msg):
        raw_input(msg + ": Press any key to continue...")