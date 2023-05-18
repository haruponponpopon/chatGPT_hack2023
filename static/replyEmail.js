const inputField = document.getElementById("input-field");
const sendButton = document.getElementById("send-button");
const responseField = document.getElementById("response-field");

sendButton.onclick = async ()=>{
  const input = inputField.value;
  const data = {"email_str": input}
  console.log(data);
    const response = await fetch("/replyEmail", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  responseField.innerHTML = await response.json();
}

