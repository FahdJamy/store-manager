var closBtn = document.getElementById('closure');
var recordBtn = document.getElementById('recordBtn');
var modalOpen = document.getElementById('modal');

closBtn.addEventListener('click', closeWindow);
recordBtn.addEventListener('click', openWindow);
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