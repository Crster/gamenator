async function handleOnSubmit(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const inputPrompt = formData.get("prompt");

  try {
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

    const data = await response.text();

    console.log(data);
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}
