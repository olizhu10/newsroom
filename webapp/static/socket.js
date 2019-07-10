var socket = io.connect('http://' + document.domain + ':' + location.port);
var cluster;
var summary;
var article;

$(document).on('submit', 'form#select-form', function(e) {
  e.preventDefault();
  socket.emit('send cluster');
});

socket.on('cluster retrieved', function(msg) {
  cluster = msg;
  console.log(cluster);
  show_summary(cluster);
  show_article(cluster);
  if (summary===undefined || article===undefined) {}
  else {
    json = {'summary':summary,
            'article':article}
    socket.emit('send info', json);
  }
});

socket.on('info sent', function(json) {
  let density = json['density'];
  let coverage = json['coverage'];
  let compression = json['compression']
  let fragments = json['fragments']

  update_info(density, coverage, compression, fragments);
})

function show_summary(cluster) {
  let index = $('select#summary-select').val();
  summary = index
  let summary_text = document.getElementById('summary-text');
  summary_text.innerHTML = cluster[index][1];
}

function show_article(cluster) {
  let index = $('select#article-select').val();
  article = index
  let article_text = document.getElementById('article-text');
  article_text.innerHTML = cluster[index][0];
}

function update_info(density, coverage, compression, fragments) {
  var pcov = document.getElementById('coverage')
  var pdens = document.getElementById('density')
  var pcomp = document.getElementById('compression')
  var pfrag = document.getElementById('fragments')

  pcov.innerHTML = "Coverage: "+coverage;
  pdens.innerHTML = "Density: "+density;
  pcomp.innerHTML = "Compression: "+compression;
  pfrag.innerHTML = "Fragments: "+fragments;
}
