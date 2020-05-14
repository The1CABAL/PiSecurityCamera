function showForm() {
	var applicationChbx = document.getElementById("applicationId");
	var form = document.getElementById("form");
	if (typeof (applicationChbx) != 'undefined' && applicationChbx != null) {
		if (applicationChbx.checked == true) {
			form.style.display = "block";
		}
		else {
			form.style.display = "none";
		}
	}
}