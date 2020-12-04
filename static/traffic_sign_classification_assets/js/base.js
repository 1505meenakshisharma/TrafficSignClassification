function hide_button_show_loader()
{
    document.getElementById("predictButton").style.display = "none";
    document.getElementById("loader").style.display = "block";
    setTimeout("hide_loader_show_result()", 2000);
}

function hide_loader_show_result()
{
    document.getElementById("loader").style.display = "none";
    document.getElementById("result").style.display = "block";
}