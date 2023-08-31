class authApi{
    constructor(){
        document.querySelector("body").style.display = "none";
        const auth = localStorage.getItem("auth");
        this.validateAuth(auth);
    }

    validateAuth(auth){
        if(auth != 1){
            window.location.replace('/');
        }else{
            document.querySelector("body").style.display = "block";
        }
    }

    logout() {
        localStorage.removeItem('auth');
        localStorage.removeItem('user');
        window.location.replace('/');
    }
}
