document.getElementById("showDeleteButtons").addEventListener("click", function() {
    var deleteButtons = document.querySelectorAll(".delete-btn");
    
    deleteButtons.forEach(function(button) {
        button.style.display = "inline-block"; // Show the buttons
    });
});