var closBtn = document.getElementById('closure');
var openBtn = document.getElementById('user_1');
var openBtn2 = document.getElementById('user_2');
var openBtn3 = document.getElementById('user_3');
var modalOpen = document.getElementById('user_role');

closBtn.addEventListener('click', closeWindow);
openBtn.addEventListener('click', openWindow);
openBtn2.addEventListener('click', openWindow);
openBtn3.addEventListener('click', openWindow);
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