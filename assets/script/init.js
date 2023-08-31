const auth = new authApi();

document.querySelector("#logout").addEventListener("click", (e) => {
	auth.logout();
});