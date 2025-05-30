const form = document.querySelector("form");
const input = document.querySelector("#input");
const messages = document.querySelector("#messages");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const userMessage = input.value.trim();
  if (!userMessage) return;

  addMessage("나", userMessage);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();
    addMessage("GPT", data.response);
  } catch (error) {
    console.error("오류 발생:", error);
    addMessage("GPT", "⚠️ 오류가 발생했어요. 다시 시도해주세요.");
  }

  input.value = "";
});

function addMessage(sender, text) {
  const div = document.createElement("div");
  div.className = "message";
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}
