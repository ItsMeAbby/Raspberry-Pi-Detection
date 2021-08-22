fetch("http://localhost:5000/read")
  // fetch("testt2.json")
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

function rangeValues(i, data, mainKeys, mainContainer) {
  var rangeKey = Object.keys(data[mainKeys[i]]);
  // console.log(rangeKey);

  for (var j = 0; j < rangeKey.length; j++) {
    var maindiv = document.createElement("div");
    // console.log(data[mainKeys[i]][rangeKey[j]]);
    maindiv.classList.add("list");
    mainContainer.appendChild(maindiv);

    var mainList = document.getElementsByClassName("list");
    var len = mainList.length;

    var mainList = document.getElementsByClassName("list")[len - 1];
    var div = document.createElement("div");
    div.classList.add("label");

    div.innerHTML = rangeKey[j] + ":  ";
    mainList.appendChild(div);
    var div = document.createElement("input");
    div.setAttribute("type", "range");
    div.setAttribute("min", data[mainKeys[i]][rangeKey[j]]["min"]);
    div.setAttribute("max", data[mainKeys[i]][rangeKey[j]]["max"]);
    div.setAttribute("step", 0.001);
    div.setAttribute("value", data[mainKeys[i]][rangeKey[j]]["value"]);
    div.setAttribute("oninput", "this.nextElementSibling.value = this.value");
    div.classList.add("input-" + rangeKey[j]);
    div.classList.add("input");
    div.classList.add("slider");
    div.setAttribute("name", rangeKey[j]);
    mainList.appendChild(div);
    var div = document.createElement("output");
    div.classList.add("value");
    div.innerHTML = data[mainKeys[i]][rangeKey[j]]["value"];
    mainList.appendChild(div);
  }
}
function selectValues(i, data, mainKeys, mainContainer) {
  var selectKey = Object.keys(data[mainKeys[i]]);
  // console.log(selectKey);

  for (var j = 0; j < selectKey.length; j++) {
    var maindiv = document.createElement("div");
    // console.log(data[mainKeys[i]][selectKey[j]]);
    maindiv.classList.add("list");
    mainContainer.appendChild(maindiv);

    var mainList = document.getElementsByClassName("list");
    var len = mainList.length;

    var mainList = document.getElementsByClassName("list")[len - 1];
    var div = document.createElement("div");
    div.classList.add("label");
    div.innerHTML = selectKey[j] + ":  ";
    mainList.appendChild(div);
    var div = document.createElement("select");
    div.classList.add("select-" + selectKey[j]);
    div.classList.add("input");
    // console.log(div.setAttribute("label", selectKey[j]));
    div.setAttribute("selected", data[mainKeys[i]][selectKey[j]]["selected"]);

    div.setAttribute("name", selectKey[j]);
    mainList.appendChild(div);

    var valueKeys = Object.keys(data[mainKeys[i]][selectKey[j]]["value"]);
    // console.log(mainKeys.length);
    for (var k = 0; k < valueKeys.length; k++) {
      var innerList = document.getElementsByClassName(
        "select-" + selectKey[j]
      )[0];

      var div = document.createElement("option");
      div.setAttribute(
        "value",
        data[mainKeys[i]][selectKey[j]]["value"][valueKeys[k]]
      );
      // console.log(
      //   data[mainKeys[i]][selectKey[j]]["value"][valueKeys[k]] == true
      // );
      // console.log(data[mainKeys[i]][selectKey[j]]["selected"] == true);
      // console.log(
      //   (data[mainKeys[i]][selectKey[j]]["selected"] == true) &
      //     (data[mainKeys[i]][selectKey[j]]["value"][valueKeys[k]] == true)
      // );
      // console.log(data[mainKeys[i]][selectKey[j]]["value"][valueKeys[k]]);
      if (
        (data[mainKeys[i]][selectKey[j]]["selected"] == true) &
          (data[mainKeys[i]][selectKey[j]]["value"][valueKeys[k]] == true) ||
        (data[mainKeys[i]][selectKey[j]]["selected"] == false) &
          (data[mainKeys[i]][selectKey[j]]["value"][valueKeys[k]] == false)
      ) {
        div.selected = "selected";
      }
      div.innerHTML = data[mainKeys[i]][selectKey[j]]["value"][valueKeys[k]];
      innerList.appendChild(div);
    }
  }
}
function numberValues(i, data, mainKeys, mainContainer) {
  var numberKey = Object.keys(data[mainKeys[i]]);
  // console.log(numberKey);

  for (var j = 0; j < numberKey.length; j++) {
    var maindiv = document.createElement("div");
    // console.log(data[mainKeys[i]][numberKey[j]]);
    maindiv.classList.add("list");
    mainContainer.appendChild(maindiv);

    var mainList = document.getElementsByClassName("list");
    var len = mainList.length;

    var mainList = document.getElementsByClassName("list")[len - 1];
    var div = document.createElement("div");
    div.classList.add("label");
    div.innerHTML = numberKey[j] + ":  ";

    mainList.appendChild(div);
    var div = document.createElement("input");
    div.setAttribute("type", "number");
    div.setAttribute("placeholder", data[mainKeys[i]][numberKey[j]]["value"]);
    div.setAttribute("max", data[mainKeys[i]][numberKey[j]]["max"]);
    div.setAttribute("min", data[mainKeys[i]][numberKey[j]]["min"]);
    div.classList.add("number-" + numberKey[j]);
    div.classList.add("input");
    console.log(numberKey[j]);
    div.setAttribute("name", numberKey[j]);

    mainList.appendChild(div);
  }
}
function textValues(i, data, mainKeys, mainContainer) {
  var stringKey = Object.keys(data[mainKeys[i]]);
  // console.log(stringKey);

  for (var j = 0; j < stringKey.length; j++) {
    var maindiv = document.createElement("div");
    // console.log(data[mainKeys[i]][stringKey[j]]);
    maindiv.classList.add("list");
    mainContainer.appendChild(maindiv);

    var mainList = document.getElementsByClassName("list");
    var len = mainList.length;

    var mainList = document.getElementsByClassName("list")[len - 1];
    var div = document.createElement("div");
    div.classList.add("label");
    div.innerHTML = stringKey[j] + ":  ";
    mainList.appendChild(div);
    var div = document.createElement("input");
    div.setAttribute("type", "text");
    div.setAttribute("placeholder", data[mainKeys[i]][stringKey[j]]["value"]);
    div.setAttribute("max", data[mainKeys[i]][stringKey[j]]["max"]);
    div.setAttribute("min", data[mainKeys[i]][stringKey[j]]["min"]);
    div.setAttribute("name", stringKey[j]);
    div.classList.add("string-" + stringKey[j]);
    div.classList.add("input");
    mainList.appendChild(div);
  }
}

function appendData(data) {
  var mainKeys = Object.keys(data);
  var mainContainer = document.getElementsByClassName("values-form")[0];
  // console.log(mainKeys.length);
  for (var i = 0; i < mainKeys.length; i++) {
    if (mainKeys[i] == "range") {
      rangeValues(i, data, mainKeys, mainContainer);
    } else if (mainKeys[i] == "select") {
      selectValues(i, data, mainKeys, mainContainer);
    } else if (mainKeys[i] == "number") {
      numberValues(i, data, mainKeys, mainContainer);
    } else if (mainKeys[i] == "string") {
      textValues(i, data, mainKeys, mainContainer);
    }
  }
  var button = document.createElement("input");
  button.setAttribute("type", "submit");
  button.classList.add("submitButton");
  mainContainer.appendChild(button);
}
