var deleteButton = document.getElementById("koro-sensei");
var inputField = document.getElementById("verify-deletion");

function verifyDeletion() {
    if (inputField.value == "Nezuko") {
        deleteButton.setAttribute("class", "danger");
        deleteButton.disabled = false;
    } else {
        deleteButton.setAttribute("class", "secondary");
        deleteButton.disabled = true;
    }
}