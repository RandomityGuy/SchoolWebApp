// function signIN() {
//     document.getElementById('middleBox').classList.add('middle-box-anim');
//     document.getElementById('logoId').classList.add('logo-anim');
//     document.getElementById('animbox').style.opacity = "0";
//     document.getElementById('form').style.opacity = "1";   
    
// }

function signIN() {
    document.getElementById('middleBox').classList.toggle('middle-box-anim');
    document.getElementById('logoId').classList.toggle('logo-anim');
    document.getElementById('animbox').style.opacity = "0";
    document.getElementById('form').style.opacity = "1";
    document.getElementById('form').style.transitionDelay = "1s";
    document.getElementById('animbox').style.transitionDelay = "0ms"; 
    document.getElementById('animbox').style.pointerEvents = "none";   
    document.getElementById('form').style.pointerEvents = "auto";   
    
}

function notSignIN() {
    document.getElementById('middleBox').classList.toggle('middle-box-anim');
    document.getElementById('logoId').classList.toggle('logo-anim');
    document.getElementById('animbox').style.opacity = "1";
    document.getElementById('form').style.opacity = "0";
    document.getElementById('form').style.transitionDelay = "0ms";
    document.getElementById('animbox').style.transitionDelay = "0.7s";  
    document.getElementById('form').style.pointerEvents = "none";
    document.getElementById('animbox').style.pointerEvents = "auto";   
}