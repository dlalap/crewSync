var roomName = '{{ room_name|escapejs }}';
console.log('loaded from control.js');
var chatSocket = new WebSocket(
  'ws://' + window.location.host + '/ws/spotcontrol/' + roomName + '/',
);

chatSocket.onmessage = function(e) {
  var data = JSON.parse(e.data);
  var control = data['control'];
  document.querySelector('#control-log').value += control + '\n';
};

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

document.querySelector('#sync-previous').onclick = function(e) {
  console.log('PREV');
  chatSocket.send(
    JSON.stringify({
      control: 'PREVIOUS',
    }),
  );
};
document.querySelector('#sync-pause').onclick = function(e) {
  console.log('PAUSE');
  chatSocket.send(
    JSON.stringify({
      control: 'PAUSE',
    }),
  );
};
document.querySelector('#sync-play').onclick = function(e) {
  console.log('PLAY');
  chatSocket.send(
    JSON.stringify({
      control: 'PLAY',
    }),
  );
};
document.querySelector('#sync-next').onclick = function(e) {
  console.log('NEXT');
  chatSocket.send(
    JSON.stringify({
      control: 'NEXT',
    }),
  );
};

function rewind() {
  console.log('hello, world.');
}
