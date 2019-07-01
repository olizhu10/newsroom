

function createDiv(data) {
  var toAdd
}

function generateSummaryButtons() {
  var toAdd
  buttons = []
  for (i=0, i < cluster.length; i++) {
    var newButton = document.createElement('button');
    newButton.value = "s"+i
    newButton.class = "summary"
    newButton.innerHTML = newButton.value
    newButton.onClick
    toAdd.appendChild(newButton)
  }
  document.appendChild(toAdd)
}

function generateArticleButtons() {
  var toAdd
  buttons = []
  for (i=0, i < cluster.length; i++) {
    var newButton = document.createElement('button');
    newButton.value = "a"+i
    newButton.class = "summary"
    newButton.innerHTML = newbutton.value
    toAdd.appendChild(newButton)
  }
  document.appendChild(toAdd)
}

function generateDiv() {
  var toAdd
  buttons = []
  for (i=0, i < cluster.length; i++) {
    var newDiv = document.createElement('div');
    newDiv.value = "b"+i
    newDiv.class = "summary"
    toAdd.appendChild(newDiv)
  }
  document.appendChild(toAdd)
}
