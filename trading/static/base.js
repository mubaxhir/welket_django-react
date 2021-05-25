const inboxButton = document.getElementById("inbox-dropdown-btn");
const inboxDropDown = document.getElementById('InboxDropdown');
const backDrop = document.getElementById('backdrop');
const inboxWrapper = document.querySelector('.inbox-wrapper');
// const inboxWrapper = document.getElementsByClassName(".inbox-wrapper");



inboxButton.addEventListener('click', toggleInbox);

function toggleInbox(event) {
	event.preventDefault();
	if (inboxWrapper.style.display === 'block') {
		inboxWrapper.style.display = 'none';
	} else {
		inboxWrapper.style.display = 'block';
	}
}



document.querySelector('.main-body').addEventListener('click', () => {
	if (!event.target.classList.contains('send-message-btn')) {
		inboxWrapper.style.display = 'none';
	}
})

function showInbox(event) {
	console.log('-------------------');
	event.preventDefault();
	inboxWrapper.style.display = 'block';
}




// code for chat box

const chats = document.querySelector('.chats');
const chatBox = document.getElementById('InboxDropdownChat');
const backButton = document.getElementById('chatbox-back-btn');

// const room = document.querySelector('#room').value
// print(room)


// these global vars are changes everytime user click on the other chat

let CHAT_URL;
let SENDER, RECEIVER;
function showChatBox(requestUserId, chatUserId,flag=false) {
	SENDER = requestUserId;
	RECEIVER = chatUserId;
	console.log(requestUserId, chatUserId);
	

	// UI 
	showInbox(event);
	console.log('--------------------');
	if (event.target.classList.contains('chat-profile')) {
		chatBox.style.display = 'block';
	} else if (event.target.parentElement.classList.contains('chat-profile')) {
		chatBox.style.display = 'block';	
	}
	if (flag) {
		chatBox.style.display = 'block';
	}
	const messagesOutputElement = document.querySelector('.chat-messages');
	messagesOutputElement.innerHTML = '<div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>';
	// Getting the data from api
	const url = `/api/messages/${Number(requestUserId)}/${Number(chatUserId)}`;
	CHAT_URL = url;
	fetch(url)
		.then(response => {
			return response.json();
		}).then((data) => {
			showMessages(data);
		}).catch(error => {
			console.log(error);
		});

	event.preventDefault();

}



function showMessages({ messages }) {
	let output = '';
	const messagesOutputElement = document.querySelector('.chat-messages');
	messages.forEach(message => {
		if (message.sender == currentUser ){
		output += ` 
		<div class='card chat-message-sender'>
			<b>${message.sender} </b>
			<p>${message.message}</p>
		</div>`
		}
		else{
		output += `
		<div class='card chat-message-receiver'>
			<b>${message.sender} </b>
			<p>${message.message}</p>
		</div>
		`;
		}
	});
	messagesOutputElement.innerHTML = output;
}

// Sending messages
const sendMessageButton = document.getElementById('send-msg-btn');


var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == 'https:') {
	wsStart = 'wss://'
}

var socket = new WebSocket(wsStart + window.location.host +'/ws?session_key='+sessionKey);

socket.onerror = function(e){
	console.log("erro",e);
}

socket.onopen = function(e){
	console.log("real time chat",e);
}

socket.onclose = function(e){
	console.log("real time chat ",e);
}


socket.onmessage = function(e) {
	const data = JSON.parse(e.data);
	console.log("real time ",data);
	if (data.receiver == currentUser) {
		const messagesOutputElement = document.querySelector('.chat-messages');
		messagesOutputElement.innerHTML += `
		<div class='card chat-message-receiver'>
		<b>${data.sender} </b>
		<p>${data.message}</p>
		</div>`;
		$.notify("You received new messages!",data.receiver);

	}

}



sendMessageButton.addEventListener('click', () => {
	const message = document.getElementById('post-message').value;
	if (message !== '') {
		sendMessageButton.innerHTML = 'Sending...';
		const data = {
			sender: SENDER,
			receiver: RECEIVER,
			message:message
		}
		console.log(data);
		fetch(CHAT_URL, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(data)
		}).then((response) => {
			return response.json();
		}).then(data => {
			// add message to the list
			if (data.sender === currentUser) {
				const messagesOutputElement = document.querySelector('.chat-messages');
				messagesOutputElement.innerHTML += `
				<div class='card chat-message-sender'>
				<b>${data.sender} </b>
				<p>${data.message}</p>
				</div>`;
			}	
			else {
				alert('error',data);
			}	
			document.getElementById('post-message').value = '';
			sendMessageButton.innerHTML = 'Send';
			
		}).catch(err => {
			console.log(err);
		});
	}
	
});


window.onscroll = function() {myFunction()};

var header = document.getElementById("myHeader");
var sticky = header.offsetTop;

function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}
