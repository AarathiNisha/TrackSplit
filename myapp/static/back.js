const showConfirm = document.getElementById("showConfirm");
const confirmButtons = document.getElementById("confirmButtons");
const cancelButton = document.getElementById("cancelButton");

if (showConfirm && confirmButtons && cancelButton) {
    showConfirm.addEventListener("click", function () {
        showConfirm.style.display = "none";
        confirmButtons.style.display = "inline";
    });

    cancelButton.addEventListener("click", function () {
        confirmButtons.style.display = "none";
        showConfirm.style.display = "block";
    });
}