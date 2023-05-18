const inputField = document.getElementById("input-field");
const paintArea = document.getElementById("paint-area");
const sendButton = document.getElementById("send-button");

sendButton.onclick = async ()=>{
  const input = inputField.value;
  const html = paintArea.innerHTML;
  const data = {"command": input, "html": html}
  console.log(data);
    const response = await fetch("/paint", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  alert("updated!")
  paintArea.innerHTML = await response.json();
}