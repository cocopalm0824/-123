import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 AI 상담 챗봇")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 채팅 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("연애 고민을 입력해보세요...")

if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 생성 중..."):

            try:
                # 대화 기록 구성
                conversation = []

                system_prompt = """
                너는 공감 능력이 뛰어난 연애상담 AI야.
                사용자의 감정을 존중하고 따뜻하게 답변해.
                필요하면 현실적인 조언도 제공해.
                너무 공격적이거나 단정적으로 말하지 마.
                """

                conversation.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=system_prompt)]
                    )
                )

                for msg in st.session_state.messages:
                    conversation.append(
                        types.Content(
                            role=msg["role"],
                            parts=[types.Part(text=msg["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=conversation
                )

                ai_response = response.text

                st.markdown(ai_response)

                # AI 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:
                error_message = f"❌ 오류가 발생했습니다: {e}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
