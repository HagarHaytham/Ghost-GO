var zmq = require ('zeromq')
var sock = zmq.socket ('sub');

sock.connect('tcp://127.0.0.1:3001');
sock.subscribe('hello');
console.log('Subscriber connected to port 3001');

sock.on('message', function(messagedata) {
  console.log(messagedata.toString("utf8"));
});

var sock2 = zmq.socket('pub');

sock2.bindSync("tcp://127.0.0.1:3000");
console.log("Publisher bound to port 3000");

setInterval(function() {
  console.log("sending a multipart message envelope");
  sock.send(["kitty cats", "meow!"]);
}, 500);

