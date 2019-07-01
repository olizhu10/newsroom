var socket = io.connect('http://' + document.domain + ':' + location.port);

$('form#cluster').on('submit', function(e)) {
    e.preventDefault()
    let cluster_id = $('input.cluster').val()
    socket.emit('cluster id submitted', {
      cluster_id : cluster_id
    })
    $( 'input.cluster' ).val('').focus()
  } )


$('#summary').on('submit', function(e)) {
  e.preventDefault()
  let num = $('input#summary_submit').val()
  $('div.summaries').hide()
  $('div#num.summaries').show()
}

$('#article').on('submit', function(e)) {
  e.preventDefault()
  let num = $('input#article_submit').val()
  $('div.articles').hide()
  $('div#num.articles').show()
}
