
function init() {
  var geoSuccess = function(position) {
    var url = 'http://localhost:5000/path/'
    url += position.coords.latitude + '/'
    url += position.coords.longitude

    var callback = function(result) {
      document.body.innerHTML = result;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if(xhttp.readyState == 4 && xhttp.status == 200)
        callback(xhttp.response);
    }

    xhttp.open("GET", url, true);
    xhttp.send();
  }
    
  navigator.geolocation.getCurrentPosition(geoSuccess);
}
