var zmq = require("zeromq"),
  sock = zmq.socket("pull");
  sock2 = zmq.socket("push")

sock.connect("tcp://127.0.0.1:3000");
sock2.bindSync("tcp://127.0.0.1:3001");
console.log("Worker connected to port 3000");

setInterval(function() {
    console.log("sending work");
    sock2.send("some work from puller to pusher");
  }, 500);

sock.on("message", function(msg) {
  console.log("work from push: %s", msg.toString());
});