const inputField = document.getElementById("recorder");
const sendButton = document.getElementById("send-button");
const transcriptField = document.getElementById("transcript-field");
const responseField = document.getElementById("response-field");

sendButton.onclick = async ()=>{
  const fd = new FormData();
  const input_file = inputField.files[0];
  console.log(input_file)
		fd.append('uploadfile', input_file);
    const response = await fetch("/upload_audio", {
      method: "POST",
      body: fd,
    });
  const responseJson = await response.json();
  console.log(responseJson);
  transcriptField.innerHTML = responseJson["transcript"];
  responseField.innerHTML = responseJson["response"];
}