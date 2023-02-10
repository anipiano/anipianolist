var deleteButton = document.getElementById("koro-sensei");
var inputField = document.getElementById("verify-deletion");

function verifyDeletion(passcode) {
    if (inputField.value == passcode) {
        deleteButton.setAttribute("class", "danger");
        deleteButton.disabled = false;
    } else {
        deleteButton.setAttribute("class", "secondary");
        deleteButton.disabled = true;
    }
}