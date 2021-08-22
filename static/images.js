// fetch("http://localhost:5000/read")
fetch("blinking.json")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    appendData(data);
  })
  .catch(function (err) {
    console.log("error: " + err);
    console.log("HAHAHHA");
  });
function appendData(data) {}
