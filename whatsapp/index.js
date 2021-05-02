const axios = require('axios');
const venom = require('venom-bot');
const Responder = require('./processor')


// venom.create().then((client) => start(client)).catch((error) => console.log(error));

// start = (client) => {
//     client.onMessage((message) => {
//         if (message.from === '263786087836@c.us' && message.isGroupMsg === false) {
//             axios.post('http://127.0.0.1:5000/newmessage', { from: message.from, message: message.body })
//                 .then((response) => new Responder(client, response).sendResponse())
//                 .catch((error) => console.log(error));
//         }
//     });
// }

axios.post('http://127.0.0.1:5000/contacts/buycontacts', { from: "message.from", message: "message.body" })
    .then((response) => console.log(response.data))
    .catch((error) => console.log(error));