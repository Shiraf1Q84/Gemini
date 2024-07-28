import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import markdown
import re
import tempfile

# Streamlitページ設定
st.set_page_config(
    page_title="Gemini PDFベースチャットボット",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# セッション状態の初期化
if "documents" not in st.session_state:
    st.session_state.documents = []
if "checkbox_values" not in st.session_state:
    st.session_state.checkbox_values = {}
if "file_names" not in st.session_state:
    st.session_state.file_names = {}
if "next_file_id" not in st.session_state:
    st.session_state.next_file_id = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_markdown(file):
    content = file.read().decode("utf-8")
    html = markdown.markdown(content)
    text = re.sub('<[^<]+?>', '', html)
    return text

# 2列レイアウトの作成
left_column, right_column = st.columns([1, 3])

with left_column:
    # APIキー入力欄
    st.title("Google API キー")
    api_key = st.text_input("APIキーを入力してください:", type="password")
    if st.button("APIキーを設定"):
        genai.configure(api_key=api_key)
        st.success("APIキーが設定されました")

    # モデル選択
    model_name = st.selectbox("モデルを選択してください:", ["gemini-1.5-pro", "gemini-pro"])

    # ファイルアップロード
    uploaded_files = st.file_uploader(
        "PDFまたはマークダウンファイルを選択してください",
        accept_multiple_files=True,
        type=["pdf", "md"],
    )

    # ファイル処理
    if uploaded_files:
        new_files = [file for file in uploaded_files if file.name not in st.session_state.file_names.values()]
        for uploaded_file in new_files:
            file_extension = os.path.splitext(uploaded_file.name)[1]
            if file_extension == ".pdf":
                text = extract_text_from_pdf(uploaded_file)
            elif file_extension == ".md":
                text = extract_text_from_markdown(uploaded_file)
            else:
                st.warning(f"未対応のファイル形式です: {uploaded_file.name}")
                continue

            file_id = str(st.session_state.next_file_id)
            st.session_state.next_file_id += 1
            st.session_state.documents.append({"id": file_id, "content": text})
            
            # ファイル名を保存/更新
            st.session_state.file_names[file_id] = uploaded_file.name
            
            # チェックボックスの初期状態を設定
            st.session_state.checkbox_values[file_id] = True

        if new_files:
            st.success(f"{len(new_files)}個の新しいファイルがアップロードされました。")

    # アップロードされたファイル一覧の表示
    st.subheader("アップロードされたファイル")
    for doc in st.session_state.documents:
        file_id = doc["id"]
        file_name = st.session_state.file_names.get(file_id, "Unknown File")
        checked = st.checkbox(
            file_name,
            value=st.session_state.checkbox_values.get(file_id, True),
            key=f"checkbox_{file_id}"
        )
        # チェックボックスの状態を更新
        st.session_state.checkbox_values[file_id] = checked

with right_column:
    st.title("PDFベースチャットボット (Gemini)")

    # システムプロンプト設定
    system_prompt = st.text_area(
        "システムプロンプトを入力してください",
        """
        あなたはナレッジベースに提供されている書類に関する情報を提供するチャットボットです。
        利用者の質問に、正確かつなるべく詳細に、参考資料を引用しながら答えてください。
        情報は800文字以上、4000文字以内に収めてください。
        マークダウン形式で見やすく出力してください。
        情報源を明記して回答するように努めてください。
        複数の解釈がある場合は、それぞれを提示してください。
        与えられた情報だけでは判断できない場合には、判断できない旨を伝えてください。
        """,
        height=300
    )

    # チャット履歴の表示
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力
    user_input = st.chat_input("質問を入力してください")

    if user_input and api_key:
        # ユーザーの質問をチャット履歴に追加
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Geminiモデルの初期化
        model = genai.GenerativeModel(model_name)

        # チェックされているドキュメントのみを使用してコンテキストを作成
        context = ""
        for doc in st.session_state.documents:
            if st.session_state.checkbox_values.get(doc["id"], True):
                context += f"ファイル名: {st.session_state.file_names.get(doc['id'], 'Unknown File')}\n"
                context += f"内容:\n{doc['content']}\n\n"

        # プロンプトの作成
        prompt = f"""
        {system_prompt}

        参考文書:
        {context}

        ユーザーの質問: {user_input}
        """

        # ストリーミング出力のための空のプレースホルダーを作成
        response_placeholder = st.empty()

        # ストリーミングレスポンスを生成
        response = model.generate_content(prompt, stream=True)

        # ストリーミング出力
        full_response = ""
        for chunk in response:
            full_response += chunk.text
            response_placeholder.markdown(full_response + "▌")

        # 最終的な応答を表示
        response_placeholder.markdown(full_response)

        # アシスタントの回答をチャット履歴に追加
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    elif not api_key:
        st.warning("APIキーを設定してください。")