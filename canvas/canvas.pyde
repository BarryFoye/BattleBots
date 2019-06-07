from World import World
add_library('httprequests_processing')
import json

w = 400
h = 400

world = World(w, h,3, 3, 0)

def setup():
    SendHTTPRequest()
    size(w, h)
    

def draw():
    background(255)
    world.run()
    
def SendHTTPRequest():
    ### POST request
    #post = PostRequest("http://localhost:63079/get_random_generation")
    #post.send();
    #println("Reponse Content: " + str(post.getContent()));
    #println("Reponse Content-Length Header: " + post.getHeader("Content-Length"));
    
    ##Get request
    get = GetRequest("http://localhost:5555/get_random_generation");
    get.send();
    println("Reponse Content: " + get.getContent());
    println("Reponse Content-Length Header: " + get.getHeader("Content-Length"));
    
