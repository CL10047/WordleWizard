document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('change-username').style.display = "none";
    document.getElementById('change-username').style.display = "none";
    document.getElementById('change-email').style.display = "none";
    document.getElementById('change-password').style.display = "none";
    document.getElementById('password_requirement').style.display = "none";
});

function showUserInfo() {
    document.getElementById('user-info').style.display = "block";
    document.getElementById('change-username').style.display = "none";
    document.getElementById('change-email').style.display = "none";
    document.getElementById('change-password').style.display = "none";
}

function showUsername() {
    document.getElementById('user-info').style.display = "none";
    document.getElementById('change-username').style.display = "block";
    document.getElementById('change-email').style.display = "none";
    document.getElementById('change-password').style.display = "none";
}

function showEmail() {
    document.getElementById('user-info').style.display = "none";
    document.getElementById('change-username').style.display = "none";
    document.getElementById('change-email').style.display = "block";
    document.getElementById('change-password').style.display = "none";
}

function showPassword() {
    document.getElementById('user-info').style.display = "none";
    document.getElementById('change-username').style.display = "none";
    document.getElementById('change-email').style.display = "none";
    document.getElementById('change-password').style.display = "block";
}
  
