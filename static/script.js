const backendUrl = "https://pdf-chatbot-zn05.onrender.com";

async function uploadPDF() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("PDF 파일을 선택해주세요.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${backendUrl}/upload_pdf`, {
      method: "POST",
      body: formData
    });

    const result = await response.json();
    alert(result.message || "업로드 완료");
  } catch (error) {
    alert("PDF 업로드 중 오류 발생");
    console.error("❌ 업로드 오류:", error);
  }
}

const form = document.querySelector("#chatForm");
const input = document.querySelector("#input");
const messages = document.querySelector("#messages");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const userMessage = input.value.trim();
  if (!userMessage) return;

  addMessage("나", userMessage);

  try {
    const response = await fetch(`${backendUrl}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: userMessage })
    });

    if (!response.ok) {
      throw new Error("서버 응답 실패");
    }

    const data = await response.json();
    console.log("📥 응답 도착:", data);
    addMessage("GPT", data.answer || "답변을 가져오지 못했습니다.");
  } catch (error) {
    console.error("❌ JS 오류:", error);
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
