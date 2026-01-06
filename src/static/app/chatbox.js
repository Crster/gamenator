async function handleOnSubmit(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const inputPrompt = formData.get("prompt");

  try {
    document.getElementById("ai-response").textContent = "";
    document.querySelector("form.prompt > input").disabled = true;
    document.querySelector("form.prompt > button").textContent = "Thinking...";

    const response = await fetch("/prompt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: inputPrompt }),
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    document.getElementById("ai-response").textContent = await response.text();
  } catch (error) {
    alert(`Error: ${error.message}`);
  } finally {
    Object.assign(document.querySelector("form.prompt > input"), {
      disabled: false,
      value: "",
    });
    document.querySelector("form.prompt > button").textContent = "Submit";
  }
}
