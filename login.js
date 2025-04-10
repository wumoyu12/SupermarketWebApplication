window.addEventListener("load", InitControls);
window.addEventListener("load", addListeners);

var where ;
where = "login";

function InitControls()
{
	document.getElementById("txtloginusername").textContent="";
	document.getElementById("txtloginpassword").textContent="";
	
	document.getElementById("txtsignupusername").textContent="";
	document.getElementById("txtsignuppassword").textContent="";
	document.getElementById("txtsignuprpassword").textContent="";
	
	document.getElementById("txtloginusername").focus();
	document.getElementById("txtsignupusername").focus();
}

function addListeners()
{
	document.getElementById("btnsubmit").addEventListener("click", CheckInfo);
    document.getElementById("showsignup").addEventListener("click", showSignUp);
    document.getElementById("showlogin").addEventListener("click", showLogIn);
}

function CheckInfo()
{
	if (where=="login")
	{
		CheckLogin();
	}
	else
	{
		SigninCheck();
	}
	
}

function CheckLogin()
{
	var loginusername, loginpassword;
	username = document.getElementById("txtloginusername").value;
	loginpassword = document.getElementById("txtloginpassword").value;
	
	if (username == "" || loginpassword == "")
	{
		alert("Information is missing!");
		document.getElementById("txtloginusername").value;
		document.getElementById("txtloginusername").focus();
	}
}

function SigninCheck()
{
	var username, fpassword, rpassword;
	username = document.getElementById("txtsignupusername").value;
	fpassword = document.getElementById("txtsignuppassword").value;
	rpassword = document.getElementById("txtsignuprpassword").value;
}

function showSignUp() 
{
	where = "signup";
    document.getElementById("divlogin").style.display = "none";
    document.getElementById("divsignup").style.display = "block";
    document.getElementById("txtsignupusername").focus();
}

function showLogIn() 
{
	where = "login";
    document.getElementById("divsignup").style.display = "none";
    document.getElementById("divlogin").style.display = "block";
    document.getElementById("txtloginusername").focus();
}
