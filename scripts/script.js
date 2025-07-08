const formatosSelecionados = [];
function alternarFormatoDeObra(botao, simbolo) {
  const index = formatosSelecionados.indexOf(simbolo);

  if (index === -1) {
    formatosSelecionados.push(simbolo);
    botao.classList.add("active");
  } else {
    formatosSelecionados.splice(index, 1);
    botao.classList.remove("active");
  }

  document.getElementById("formato").value = formatosSelecionados.join("");
  document.getElementById("formatPreview").innerText =
    formatosSelecionados.length ? formatosSelecionados.join(" ") : "(vazio)";
}

function enviarFormularioIndicacao(event) {
  event.preventDefault();

  const form = event.target;
  const campoDataEnvio = form.querySelector("#dataEnvio");
  const campoNome = form.querySelector("#obra");
  const dataAtual = new Date().toISOString().split("T")[0];

  campoDataAtt.value = dataAtual;

  alert(
    "Indicação enviada com sucesso!\n" +
    "Obra: " + campoNome.value.trim() +
    "\nData de envio: " + campoDataEnvio
  );
  form.reset();
}

function enviarFormularioObra(event) {
  event.preventDefault();

  const form = event.target;
  const campoDataEnvio = form.querySelector("#dataEnvio");
  const campoNome = form.querySelector("#obra");
  const dataAtual = new Date().toISOString().split("T")[0];

  campoDataAtt.value = dataAtual;

  const dados = {
    obra: form.obra.value.trim(),
    status: form.status.value,
    formato: form.formato.value,
    capitulo: form.capitulo.value,
    minutagem: form.minutagem.value,
    // ...outros campos conforme necessidade
    dataEnvio: dataAtual
  };

  alert(
    "Obra enviada com sucesso!\n" +
    "Obra: " + campoNome.value.trim() +
    "\nData de atualização: " + campoDataEnvio
  );
}