function changeCam() {
	ddl = document.getElementById("chooseCamera").value;

	var list = document.getElementById("cameras").getElementsByTagName("div");
	for (var i = 0; i < list.length; i++) {
		var id = list[i].id;
		if (id && id.search(/^cam-/) != -1) {
			if (ddl == "0")
				document.getElementById(id).style.display = "block";
			else if (ddl != id)
				document.getElementById(id).style.display = "none";
			else
				document.getElementById(id).style.display = "block";
		}
	}
}