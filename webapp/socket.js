$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var cluster = []

  $(document).on('submit', 'form#cluster', function(e) {
      e.preventDefault()
      let cluster_id = $('input#cluster').val()
      socket.emit('cluster id submitted', {
        cluster_id : cluster_id
      });
      console.log(cluster_id)
      $( 'input#cluster' ).val('').focus()
    } );

  socket.on('cluster received', function(json) {
    let cluster = json['cluster']
  })

  $(document).on('submit', 'form#summary-form', function(e) {
    e.preventDefault()
    let index = $('select#summary-select').val()
    $('div#summary')
  })

  $('#summary').on('submit', function(e) {
    e.preventDefault()
    let num = $('input#summary_submit').val()
    $('div.summaries').hide()
    $('div#num.summaries').show()
  });

  $('#article').on('submit', function(e) {
    e.preventDefault()
    let num = $('input#article_submit').val()
    $('div.articles').hide()
    $('div#num.articles').show()
  });

  socket.on('article selected', function(json) {
    var p = document.createElement('p')
    var text = document.createTextNode(json['text'])
    p.appendChild(text)
    var div = document.getElementbyId('article')
    div.appendChild(p)
  });

  socket.on('summary selected', function(json) {
    var p = document.createElement('p')
    var text = document.createTextNode(json['text'])
    p.appendChild(text)
    var div = document.getElementbyId('summary')
    div.appendChild(p)
  });

});
