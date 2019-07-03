
var socket = io.connect('http://' + document.domain + ':' + location.port);
var cluster;

$(document).on('submit', 'form#summary-form', function(e) {
  e.preventDefault();
  socket.emit('send summary cluster')
});

$(document).on('submit', 'form#article-form', function(e) {
  e.preventDefault();
  socket.emit('send article cluster')
});

socket.on('summary cluster retrieved', function(msg) {
  let cluster = msg;
  console.log(cluster);
  let index = $('select#summary-select').val();
  let summary = document.getElementById('summary-text');
  summary.innerHTML = cluster[index][1];
});

socket.on('article cluster retrieved', function(msg) {
  let cluster = msg;
  console.log(cluster);
  let index = $('select#article-select').val();
  let article = document.getElementById('article-text');
  article.innerHTML = cluster[index][0];
});
