import openai
import streamlit as st
import os

# Configuração da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY") 

def gerar_proxima_pergunta(contexto):
    """
    Gera a próxima pergunta com base no histórico acumulado utilizando a nova API de chat.
    """
    prompt = f"""
    Você é um orientador de carreira especializado em ajudar estudantes do ensino médio a identificarem a área acadêmica ou profissional mais adequada para eles. 
    Seu objetivo é fazer perguntas estratégicas, baseadas no histórico de interações, para entender melhor os interesses, habilidades e objetivos do estudante.

    Histórico de perguntas e respostas:
    {contexto}

    Elabore uma única pergunta objetiva e estratégica que ajude a entender melhor os interesses, habilidades ou objetivos do estudante para auxiliá-lo na escolha da carreira.
    """

    resposta = openai.chat.completions.create(
        model="gpt-4o-mini",  # Ou "gpt-4", dependendo do seu acesso
        messages=[
            {"role": "system", "content": "Você é um orientador de carreira."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7,
    )
    return resposta.choices[0].message.content.strip()

def recomendar_area(respostas):
    """
    Recomenda uma área acadêmica com base no histórico de respostas.
    """
    prompt = f"""
    Considere o seguinte conjunto de perguntas e respostas dadas por um estudante do ensino médio:
    {respostas}
    Baseado nisso, qual seria a área universitária mais adequada para esse estudante? 
    Explique o motivo da recomendação em detalhes e inclua exemplos de cursos relacionados.
    """
    resposta = openai.chat.completions.create(
        model="gpt-4o-mini",  # Ou "gpt-4", dependendo do seu acesso
        messages=[
            {"role": "system", "content": "Você é um orientador de carreira e deve fazer perguntas relevantes para entender o perfil do estudante e o seu curso."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return resposta.choices[0].message.content.strip()


# Configuração da Interface com Streamlit
st.title("Orientador de Carreira com IA")
st.write("Responda às 5 perguntas a seguir para receber uma recomendação de carreira. Seja bem completo.")

# Inicializa o estado da aplicação
if "contexto" not in st.session_state:
    st.session_state.contexto = ""
if "respostas" not in st.session_state:
    st.session_state.respostas = []
if "finalizado" not in st.session_state:
    st.session_state.finalizado = False
if "resposta_temp" not in st.session_state:  # Armazena o texto temporário
    st.session_state.resposta_temp = ""

# Geração da próxima pergunta
if not st.session_state.finalizado:
    pergunta = gerar_proxima_pergunta(st.session_state.contexto)
    st.write(f"Pergunta: {pergunta}")

    # Captura a resposta e define o botão como não obrigatório
    resposta = st.text_input("Sua resposta:", key="resposta_temp")
    resposta_enviada = st.button("Enviar resposta")

    # Verifica se há texto preenchido (pressionando Enter) ou se o botão foi clicado
    if resposta.strip() != "" and (resposta_enviada or resposta):
        st.session_state.respostas.append({"pergunta": pergunta, "resposta": resposta})
        st.session_state.contexto += f"\nPergunta: {pergunta}\nResposta: {resposta}"

    elif resposta_enviada and resposta.strip() == "":
        st.warning("Por favor, insira uma resposta antes de continuar.")

    # Finaliza automaticamente após 5 respostas
    if len(st.session_state.respostas) >= 5:
        st.session_state.finalizado = True

# Recomenda a área acadêmica após as perguntas
if st.session_state.finalizado:
    recomendacao = recomendar_area(st.session_state.respostas)
    st.subheader("Recomendação de Carreira")
    st.write(recomendacao)

