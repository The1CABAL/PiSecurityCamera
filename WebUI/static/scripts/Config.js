var counter = 1; 
document.getElementById("showCam").style.display = "none";
var addCamSubmit = document.getElementById("addCamSubmit");
addCamSubmit.style.display = "none";

function showForm() {
    var applicationChbx = document.getElementById("applicationId");
    var form = document.getElementById("form");
    var addField = document.getElementById("showCam");

    if (typeof (applicationChbx) != 'undefined' && applicationChbx != null) {
        if (applicationChbx.checked == true) {
            form.style.display = "block";
            addField.style.display = "block";
            addCamSubmit.style.display = "block";
        }
        else {
            form.style.display = "none";
            addField.style.display = "none";
            addCamSubmit.style.display = "none";
        }
    }
}

function addInput(divName) {
    var newRow = document.createElement('div');
    var newColCam = document.createElement('div');
    var newColIp = document.createElement('div');
    newRow.className = "row";
    newRow.id = "addedRow" + counter;
    document.getElementById(divName).appendChild(newRow);

    newColCam.className = "col-lg-12";
    newColCam.innerHTML = "<label>Camera Name: </label> <input class='formTextInput' type='text' id='CameraName" + counter + "' name='CameraName" + counter + "' placeholder='FrontDoor' required/>";

    document.getElementById('addedRow' + counter).appendChild(newColCam);

    newColIp.className = "col-lg-12";
    var id = "addedRow" + counter;
    newColIp.innerHTML = "<label>Camera Ip: </label> <input class='formTextInput' type='text' id='CameraIp" + counter + "' name='CameraIp" + counter + "' placeholder='0.0.0.0' required/> <input type='button' class='formButton' onclick='return deleteInput(" + '"' + id + '"' + ")' value='Remove' />";

    document.getElementById('addedRow' + counter).appendChild(newColIp);
    counter++;
}

function deleteInput(id) {
    var element = document.getElementById(id);
    element.remove();
    counter--;
}

