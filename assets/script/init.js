const auth = new authApi();
var details = localStorage.getItem('user');
var user = JSON.parse(details);

console.log(user);
document.getElementById('name').innerText = user[0]['username'];

document.querySelector("#logout").addEventListener("click", (e) => {
	auth.logout();
});