function getUserControl() {
  return {
    aiResponse: document.getElementById("ai-response"),
    promptInput: document.getElementById("prompt-input"),
    promptPrompt: document.getElementById("prompt-prompt"),
    promptQuery: document.getElementById("prompt-query"),
  };
}

async function handlePrompt() {
  const ctrl = getUserControl();

  try {
    ctrl.aiResponse.textContent = "";
    ctrl.promptInput.disabled = true;
    ctrl.promptQuery.disabled = true;
    Object.assign(ctrl.promptPrompt, {
      disabled: true,
      textContent: "Thinking...",
    });

    const response = await fetch("/prompt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: ctrl.promptInput.value }),
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    ctrl.aiResponse.textContent = await response.text();
  } catch (error) {
    alert(`Error: ${error.message}`);
  } finally {
    ctrl.promptQuery.disabled = false;

    Object.assign(ctrl.promptInput, {
      disabled: false,
      value: "",
    });

    Object.assign(ctrl.promptPrompt, {
      disabled: false,
      textContent: "Prompt",
    });
  }
}

async function handleQuery() {
  const ctrl = getUserControl();

  try {
    ctrl.aiResponse.textContent = "";
    ctrl.promptInput.disabled = true;
    ctrl.promptPrompt.disabled = true;
    Object.assign(ctrl.promptQuery, {
      disabled: true,
      textContent: "Thinking...",
    });

    const url = new URL("/prompt", location.href);
    url.searchParams.set("query", ctrl.promptInput.value);

    const response = await fetch(url, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const json = await response.json();

    ctrl.aiResponse.textContent = JSON.stringify(json, null, 2)
  } catch (error) {
    alert(`Error: ${error.message}`);
  } finally {
    ctrl.promptPrompt.disabled = false;

    Object.assign(ctrl.promptInput, {
      disabled: false,
      value: "",
    });

    Object.assign(ctrl.promptQuery, {
      disabled: false,
      textContent: "Query",
    });
  }
}
