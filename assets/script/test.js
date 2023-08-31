var data = {
    username: "aftaza",
    password: "Aftaza"
};
// console.log(JSON.stringify(data));
fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json; charset=UTF-8",
    },
    body: JSON.stringify(data),
})
.then((response) => response.json())
.then((data) => {
    console.log(data);
})
.catch((data) =>{
    console.error("Error", data.msg);
});

// fetch('https://a1dc-158-140-169-176.ngrok-free.app/auth/login', {
//   method: 'POST',
//   body: JSON.stringify({
//     username :"Halo",
//     password: "Hahaha",
//   }),
//   headers: {
//     'Content-type': 'application/json; charset=UTF-8',
//   }
//   })
//   .then(function(response){ 
//   return response.json()})
//   .then(function(data)
//   {
//     console.log(data)
// }).catch(error => console.error('Error:', error)); 

