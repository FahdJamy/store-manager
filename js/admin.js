let closBtn = document.getElementById('closure');
let openBtn = document.getElementById('updateBtn');
let openBtn2 = document.getElementById('updateBtn2');
let openBtn3 = document.getElementById('updateBtn3');
let openBtn4 = document.getElementById('updateBtn4');
let openBtn5 = document.getElementById('updateBtn5');
let openBtn6 = document.getElementById('updateBtn6');
let openBtn7 = document.getElementById('updateBtn7');
let openBtn8 = document.getElementById('updateBtn8');
let modalOpen = document.getElementById('update_modal');

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

// Add product
let addBtn = document.getElementById('create_pdt');
let addModal = document.getElementById('add_modal');
let closAddModal = document.getElementById('closeModalAdd');

addBtn.addEventListener('click', addProduct);
closAddModal.addEventListener('click', closeModalAdd);

function addProduct () {
	addModal.style.display = 'block';
}

function closeModalAdd () {
	addModal.style.display = 'none';
}


//// Close modal view on outside click of modal view ////
function outSideClose (e) {
	if (e.target === modalOpen) {
		modalOpen.style.display = 'none';
	} else if (e.target === addModal) {
		addModal.style.display = 'none';
	}
}