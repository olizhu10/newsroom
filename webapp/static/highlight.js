const colors = ['#FFFF00','#FF0000','#FF7F00','#00FF00',
  '#00FFFF','#7FFF00','#FF7F50','#FF1493','#7FFFD4','#00BFFF','#FF00FF',
  '#ADFF2F','#FF69B4','#E0FFFF','#E6E6FA','#FFA07A','#FFA500','#DA70D6','#FF6347']

function htmlDecode(input){
  var e = document.createElement('textarea');
  e.innerHTML = input;
  // handle case of empty input
  return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

function highlight2(keyword, i) {
  var article = document.querySelector("#article-text");
  var summary = document.querySelector("#summary-text");

  var exp = htmlDecode(keyword);
  var esc = escapeRegExp(exp);
  var re = new RegExp(esc, 'g');
  console.log(exp);
  console.log(esc);
  console.log(re);

  article.innerHTML = article.innerHTML.replace(re, '<span class="frag'+i+'">'+exp+'</span>');
  summary.innerHTML = summary.innerHTML.replace(re, '<span class="frag'+i+'">'+exp+'</span>');

  var elements = document.querySelectorAll('.frag'+i);
  for (let x=0; x<elements.length; x++) {
    elements[x].style.backgroundColor = colors[i]
  }
}

function highlight(keyword,i) {
  var article = document.querySelector("#article-text");
  var summary = document.querySelector("#summary-text");

  var exp = htmlDecode(keyword);
  var esc = escapeRegExp(exp);
  var re = new RegExp(esc, 'g');

  var ainstance = new Mark(article);
  var sinstance = new Mark(summary);

  ainstance.mark(keyword, {
    className: 'frag'+i,
    separateWordSearch: false,
    }
  );
  sinstance.mark(keyword, {
    className: 'frag'+i,
    separateWordSearch: false,
    }
  );
  var elements = document.querySelectorAll('.frag'+i);
  for (let x=0; x<elements.length; x++) {
    elements[x].style.backgroundColor = colors[i]
  }
}
