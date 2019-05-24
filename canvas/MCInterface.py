class MCInterface:
    
    dna = {}
    score = {}
    
    def __init__(self):
        self.dna = {
                    'v_id':0,
                    'bigness':0, 
                    'max_speed':0,
                    'max_acceleration_rate':0,
                    'max_angular_rate':0,
                    'max_thrust':0,
                    'vision_radius':0,
                    'vision_awareness':0                    
                    }
        self.score = {
                      'v_id':0,
                      'score':0
                      }
        pass
        
        
    def model_to_controller(self,
                            v_id=0, 
                            score=0):
        self.score['v_id'] = v_id
        self.score['score'] = score
        pass
        
    def controller_to_model(self,
                            v_id=0, 
                            bigness=0,
                            max_speed=0,
                            max_acceleration_rate=0,
                            max_angular_rate=0,
                            max_thrust=0,
                            vision_radius=0, 
                            vision_awareness=0):
        self.dna['v_id'] = v_id 
        self.dna['bigness'] = bigness
        self.dna['max_speed'] = max_speed
        self.dna['max_acceleration_rate'] = max_acceleration_rate
        self.dna['max_angular_rate'] = max_angular_rate
        self.dna['max_thrust'] = max_thrust
        self.dna['vision_radius'] = vision_radius
        self.dna['vision_awareness'] = vision_awareness
        pass
