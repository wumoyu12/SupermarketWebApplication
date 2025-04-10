window.addEventListener("load", InitControls);
window.addEventListener("load", addListeners);

function InitControls() {
    document.getElementById("txtloginusername").value = "";
    document.getElementById("txtloginpassword").value = "";
    document.getElementById("txtsignupusername").value = "";
    document.getElementById("txtsignuppassword").value = "";
    document.getElementById("txtsignuprpassword").value = "";
    document.getElementById("txtloginusername").focus();
}

function addListeners() {
    document.getElementById("showsignup").addEventListener("click", showSignUp);
    document.getElementById("showlogin").addEventListener("click", showLogIn);
}

function showSignUp(event) {
    event.preventDefault();
    document.getElementById("divlogin").style.display = "none";
    document.getElementById("divsignup").style.display = "block";
    document.getElementById("txtsignupusername").focus();
}

function showLogIn(event) {
    event.preventDefault();
    document.getElementById("divsignup").style.display = "none";
    document.getElementById("divlogin").style.display = "block";
    document.getElementById("txtloginusername").focus();
}
