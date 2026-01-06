function handleOnSubmit(event) {
  event.preventDefault();
  
  const formData = new FormData(event.target);
  const inputPrompt = formData.get('prompt');

  alert(inputPrompt);
}