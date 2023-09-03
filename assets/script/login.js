class Login{
    constructor(form, fields){
        this.form = form;
        this.fields = fields;
        this.validateonSubmit();
    }

    validateonSubmit(){
        let self = this;

        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            var error = 0;
            self.fields.forEach((field) => {
                const input = document.querySelector('#'+field);
                if (self.validateFields(input) == false) {
                    error++;
                }
            });
            if (error == 0) {
				var dataIn = {
					username: document.getElementById('username').value,
					password: document.getElementById('password').value
				};

				fetch("http://127.0.0.1:8000/auth/login", {
					method: "POST",
					headers: {
						"Content-Type": "application/json; charset=UTF-8",
					},
					body: JSON.stringify(dataIn),
				})
				.then((response) => response.json())
				.then((data) => {
					if (data.status == "success") {
						fetch("http://127.0.0.1:8000/findusers/"+dataIn.username, {
							method: "POST",
							headers: {
								"Content-Type": "application/json; charset=UTF-8",
							},
						}).then((response) => response.json())
						.then((details) =>{
							localStorage.setItem('user', JSON.stringify(details.data));
						})
						localStorage.setItem('auth', 1);
                		window.location.replace('/dashboard');
					}else{
						console.error("Error", data.msg);
						document.querySelector(".error-message-all").style.display = "block";
						document.querySelector(".error-message-all").innerText = "Your Username or Password is incorrect";
						document.getElementById("password").value = "";
					}
					// console.log(data.status);
				})
				.catch((data) =>{
					console.error("Error", data.msg);
				});
            }
        });
    }
    validateFields(field) {
		if (field.value.trim() === "") {
			this.setStatus(
				field,
				`${field.parentElement.nextElementSibling.innerText} cannot be blank`,
				"error"
			);
			return false;
		} else {
			if (field.type == "password") {
				if (field.value.length < 8) {
					this.setStatus(
						field,
						`${field.parentElement.nextElementSibling.innerText} must be at least 8 characters`,
						"error"
					);
					return false;
				} else {
					this.setStatus(field, null, "success");
					return true;
				}
			} else {
				this.setStatus(field, null, "success");
				return true;
			}
		}
	}
    setStatus(field, message, status) {
		const errorMessage = field.parentElement.parentElement.querySelector(".error-message");

		if (status == "success") {
			if (errorMessage) {
				errorMessage.innerText = "";
			}
		}

		if (status == "error") {
			document.getElementById("password").value = "";
			errorMessage.innerText = message;
			errorMessage.style.display = "block";
		}
	}
}

const form = document.querySelector(".form");
if (form) {
	const fields = ["username", "password"];
	const validator = new Login(form, fields);
}