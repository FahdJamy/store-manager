const user = document.getElementById('username');
const passwrd = document.getElementById('pass');
const loginButton = document.getElementById('loginBtn');

loginButton.addEventListener('click', (e) => {

	if (user.value === 'admin' && passwrd.value === '123') {
		window.location.href = 'admin.html';
	} else {
		window.location.href = 'home.html';
	}

	e.preventDefault();
});