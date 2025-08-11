from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()


# == 回答するLLMの設定 ==
# システムメッセージテンプレートを作成
development_template = """
0〜6歳くらいまでの子どもの学習や発達に詳しい先生です。
子どもの教育や育児に関する質問に答えます。
回答スタイルは優しい口調で、分かりやすく、家庭でも実践できる具体例を併せて出してください。

質問：{input}
"""

psychology_template = """
あなたは子どもの心理に詳しいアドバイザーです。
子どもの気持ちや行動の背景を心理学的に解説して、親の対応をアドバイスします。
回答スタイルは、落ち着いた口調で、科学的根拠や心理的サポートの視点を重視してアドバイスしてください。

質問：{input}
"""

time_saving_template = """
あなたは子育て時短アドバイザーです。
忙しい親向けに、生活の効率化や時短テクを提案します。
回答スタイルは、カジュアルな口調で、手早く実践できる具体例を出してください。

質問：{input}
"""

prompt_infos = [
    {
        "name": "development",
        "description": "子どもの学習や発達に詳しい専門家です",
        "prompt_template": development_template
    },
    {
        "name": "psychology",
        "description": "子供の心理に詳しい専門家です",
        "prompt_template": psychology_template
    },
    {
        "name": "time_saving",
        "description": "子育て時短アドバイザーです",
        "prompt_template": time_saving_template
    }
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

def process_ai_request(selected_item, input_message):
    # 選択された専門家のプロンプトテンプレートを取得
    prompt_info = next((info for info in prompt_infos if info["name"] in selected_item), None)
    
    # プロンプトテンプレートを作成
    prompt = PromptTemplate(
        input_variables=["input"],
        template=prompt_info["prompt_template"]
    )
        
    # LLMに質問を送信
    response = llm.invoke(prompt.format(input=input_message))
        
    # 回答を表示
    st.write(f"**{prompt_info['description']}の回答:**")
    st.write(response.content)

# == Webアプリの概要や操作方法をユーザーに明示するためのテキストを表示 ==
st.title("教育・育児アドバイザーAI")
st.write("""
##### 子育てや教育の疑問に、AIが専門家として答えます!
質問を入力して、答えてほしい専門家のタイプを選ぶだけ。
""")

st.divider()

st.write("##### ラジオボタンでLLMに振る舞わせる専門家の種類を選択できます。")
st.write("#### 1.幼児教育の先生")
st.write("お子さんの教育に関する悩みや質問に答えます。")
st.write("#### 2.小児心理カウンセラー")
st.write("お子さんの心の悩みや不安について相談できます。")
st.write("#### 3.子育て時短アドバイザー")
st.write("忙しい子育て中の方に向けた時短テクニックを提案します。")

# == LLMに振る舞わせる専門家の種類を選択できるラジオボタンを用意 ==
selected_item = st.radio(
    "相談したい専門家を選択してください。",
    ["1.幼児教育の先生", "2.小児心理カウンセラー", "3.子育て時短アドバイザー"]
)

st.divider()

input_message = st.text_input(
    label="専門家に相談したいことを入力してください。",
    placeholder="例: 子どもが夜泣きするのですが、どうしたらいいですか？")

# == メッセージ送信処理 ==
if st.button("送信"):
    if input_message:
        st.divider()
        
        # AI専門家に質問を送信し、回答を表示
        process_ai_request(selected_item, input_message)
        
    else:
        st.error("メッセージを入力してから「送信」ボタンを押してください。")