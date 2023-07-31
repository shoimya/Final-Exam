  let x = document.querySelectorAll(".comma-killer")
  for (let i = 0; i < x.length; i++){x[i].textContent = x[i].textContent.replace(/,([^,]*)$/, '$1')}