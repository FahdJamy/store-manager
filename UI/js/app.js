var closBtn = document.getElementById('closure');
var openBtn = document.getElementById('openBtn_1');
var openBtn2 = document.getElementById('openBtn_2');
var openBtn3 = document.getElementById('openBtn_3');
var openBtn4 = document.getElementById('openBtn_4');
var openBtn5 = document.getElementById('openBtn_5');
var openBtn6 = document.getElementById('openBtn_6');
var openBtn7 = document.getElementById('openBtn_7');
var openBtn8 = document.getElementById('openBtn_8');
var modalOpen = document.getElementById('modal');

closBtn.addEventListener('click', closeWindow);
openBtn.addEventListener('click', openWindow);
openBtn2.addEventListener('click', openWindow);
openBtn3.addEventListener('click', openWindow);
openBtn4.addEventListener('click', openWindow);
openBtn5.addEventListener('click', openWindow);
openBtn6.addEventListener('click', openWindow);
openBtn7.addEventListener('click', openWindow);
openBtn8.addEventListener('click', openWindow);
window.addEventListener('click', outSideClose);

//// Close modal view on click of "x" close btn ////
function closeWindow () {
	modalOpen.style.display = 'none';
}
//// Open modal view on click of "View detail" btn ////
function openWindow () {
	modalOpen.style.display = 'block';
}
//// Close modal view on outside click of modal view ////
function outSideClose (e) {
	if (e.target === modalOpen) {
		modalOpen.style.display = 'none';
	}
}