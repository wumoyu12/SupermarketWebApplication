window.addEventListener("load", InitControls);
window.addEventListener("load", addListener);

function InitControls()
{
	document.getElementById("txtusername").focus();
}

function addListener()
{
	document.getElementById("btnsubmit").addEventListener("click",Submit)
}
