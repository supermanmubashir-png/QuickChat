let socket = io();
let username = "";
let device = navigator.userAgent;

function enter(){
    username = document.getElementById("username").value;
    localStorage.setItem("user", username);

    document.getElementById("login").style.display="none";
    document.getElementById("chat").style.display="block";
}

function sendMsg(){
    let msg = document.getElementById("msg").value;

    socket.send({
        user: username,
        device: device.includes("Mobile") ? "Phone 📱" : "Desktop 💻",
        msg: msg
    });

    document.getElementById("msg").value="";
}

function typing(){
    socket.emit("typing", username + " is typing...");
}

socket.on("typing", data=>{
    document.getElementById("typing").innerText = data;
    setTimeout(()=>{document.getElementById("typing").innerText=""},1000);
});

socket.on("message", data=>{
    let div = document.createElement("div");
    div.className="msg";

    div.innerHTML = `
    <b>${data.user}</b><br>
    <span class="device">${data.device}</span><br>
    ${data.msg} <small>${data.time}</small>
    `;

    document.getElementById("messages").appendChild(div);
});