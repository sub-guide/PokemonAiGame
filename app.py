import streamlit as st
from google import genai
from google.genai.errors import APIError

# 페이지 기본 설정
st.set_page_config(page_title="포켓몬 AI 게임", page_icon="🎮")
st.title("🎮 포켓몬 AI 게임")

# Streamlit Secrets에서 API 키 로드
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 GEMINI_API_KEY가 설정되어 있지 않습니다.")
    st.stop()

# GenAI 클라이언트 초기화
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 내용 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("행동을 입력하세요 (예: 피카츄, 너로 정했다!):"):
    # 사용자 입력 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 답변 생성
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            answer_text = response.text
            st.markdown(answer_text)
            st.session_state.messages.append({"role": "assistant", "content": answer_text})
            
        except APIError as e:
            if e.code == 503:
                st.warning("현재 AI 서버 트래픽이 많아 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요.")
            else:
                st.error(f"API 오류 발생 ({e.code}): {e.message}")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
