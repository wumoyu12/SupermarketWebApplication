window.addEventListener("load", addListeners);

where = "login";
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
		CheckLogin()
	}
	
}

function CheckLogin()
{
	loginusername = document.getElementById("txtloginusername").value;
	loginpassword = document.getElementById("txtloginpassword").value;
	if (loginusername == "")
	{
		alert("Can't leave any blank")
	}
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
