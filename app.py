import streamlit as st

def calcular_digito_verificador_ean13(codigo12):
    soma = 0
    for i, digito in enumerate(codigo12):
        n = int(digito)
        soma += n if i % 2 == 0 else n * 3
    return (10 - (soma % 10)) % 10

def ean13_para_dun14(ean13):
    if len(ean13) != 13 or not ean13.isdigit():
        raise ValueError("EAN-13 inválido.")
    corpo = ean13[:-1]
    prefixo = "1"
    novo_dv = calcular_digito_verificador_ean13(prefixo + corpo)
    return prefixo + corpo + str(novo_dv)

def gerar_novo_codigo_custom(codigo):
    if len(codigo) < 3:
        raise ValueError("Código muito curto.")

    inicio = codigo[0]
    corpo = codigo[1:-1]
    try:
        dv = int(codigo[-1])
    except:
        raise ValueError("Dígito verificador inválido.")

    if not inicio.isdigit():
        raise ValueError("Primeiro caractere deve ser um número.")

    novo_inicio = str((int(inicio) + 1) % 10)
    novo_dv = (dv - 3) % 10

    return novo_inicio + corpo + str(novo_dv)

# Streamlit App
st.title("🔁 Conversor/Transformador de Códigos de Barras")

codigo_input = st.text_input("Digite o código EAN-13 ou outro:")

if st.button("Processar"):
    if not codigo_input:
        st.warning("Por favor, digite um código.")
    else:
        codigo = codigo_input.strip()
        try:
            if not codigo.isdigit():
                raise ValueError("O código deve conter apenas números.")
            if codigo.startswith("7") and len(codigo) == 13:
                convertido = ean13_para_dun14(codigo)
                st.success(f"✅ Código identificado como EAN-13\n🔁 Convertido para DUN-14: `{convertido}`")
            elif codigo[0] in "12345689":
                convertido = gerar_novo_codigo_custom(codigo)
                st.success(f"🔁 Código transformado: `{convertido}`")
            else:
                st.error("Código inválido ou não suportado pelas regras atuais.")
        except Exception as e:
            st.error(f"Erro: {e}")
