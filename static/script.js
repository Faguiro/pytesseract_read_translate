const formulario = document.getElementById("formulario");
const imagem = document.getElementById("imagem");
const resultado = document.getElementById("resultado");
const imagemPreview = document.getElementById("imagem-preview");
const errorMessage = document.getElementById("error-message");

formulario.addEventListener("submit", (event) => {
    event.preventDefault();
    
    // Limpa mensagens de erro anteriores
    errorMessage.innerHTML = "";

    const formData = new FormData();
    formData.append("image", imagem.files[0]);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/extract");

    // Exibe a prévia da imagem após a seleção
    imagemPreview.src = URL.createObjectURL(imagem.files[0]);
    imagemPreview.style.display = "block";

    xhr.onload = () => {
        if (xhr.status === 200) {
            const resposta = JSON.parse(xhr.responseText);
            const { text, lang, translations } = resposta;

            resultado.innerHTML = `
            <h1 class="extracted-text">Texto Extraído: </h1>
            <p>${text}</p>

            <div class="result-header">                
                <p class="detected-language">Idioma Detectado: ${lang}</p>
                
            </div>

            <h3 class="translations-title">Traduções:</h3>

            <ul class="translations-list">
                <li class="translation-item">Português: ${translations.pt}</li>
                <li class="translation-item">Inglês: ${translations.en}</li>
                <li class="translation-item">Alemão: ${translations.de}</li>
                <li class="translation-item">Espanhol: ${translations.es}</li>
            </ul>
        `;
        } else {
            // Exibe mensagem de erro em caso de resposta não 200
            errorMessage.innerHTML = "Erro ao processar a imagem. Por favor, tente novamente.";
        }

        // Esconde o texto "Processando..." após o término da solicitação
        document.getElementById("loading").style.display = "none";
    };

    // Exibe o texto "Processando..." enquanto aguarda a resposta
    document.getElementById("loading").style.display = "block";

    xhr.send(formData);
});