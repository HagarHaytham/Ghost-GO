var zmq = require("zeromq"),
  sock = zmq.socket("push");
sock2 = zmq.socket("pull")

sock2.connect("tcp://127.0.0.1:3001");
sock.bindSync("tcp://127.0.0.1:3000");
console.log("Producer bound to port 3000");

sock2.on("message", function(msg) {
    console.log("work from pull: %s", msg.toString());
});

setInterval(function() {
  console.log("sending work");
  sock.send("some work from pusher to puller");
}, 500);

