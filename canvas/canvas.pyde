from World import World
add_library('httprequests_processing')

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
    post = PostRequest("http://httprocessing.heroku.com")
    post.addData("name", "Rune");
    post.send();
    println("Reponse Content: " + post.getContent());
    println("Reponse Content-Length Header: " + post.getHeader("Content-Length"));
