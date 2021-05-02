module.exports = class MessageResponder {
    constructor(client, message) {
        this.client = client;
        this.message = message.data;
    }

    sendResponse = () => {
        if (this.message.type === 'text') {
            this.sendText();
        } else if (this.message.type === 'file') {
            this.sendFile()
        } else if (this.message.type === 'image') {
            this.sendImage();
        }
    }
    sendText = async() => {;
        this.client.sendText(this.message.to, this.message.text)
            .then((result) => console.log(`|===== Text Message send to ${result.to.remote.user} =====|`))
            .catch((error) => console.error('Error when sending: ', error));
        return true;
    }
    sendImage = async() => {
        await this.client.sendImage(this.message.to, this.message.imageurl, this.message.filename, this.message.caption)
            .then((result) => console.log(`|===== Image Message send to ${result.to.remote.user} =====|`))
            .catch((error) => console.error('Error when sending: ', error));
        return true;
    }
    sendFile = async() => {
        await this.client.sendFile(this.message.to, this.message.fileurl, this.message.filename, this.message.caption)
            .then((result) => console.log(`|===== File Message send to ${result.to.remote.user} =====|`))
            .catch((erro) => console.error('Error when sending: ', erro));
        return true;
    }
}