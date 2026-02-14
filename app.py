import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

st.title("エキスパート LLM アシスタント")

st.write("##### 概要")
st.write("このアプリでは、異なる分野の専門家として振る舞うAIに質問や相談ができます。")
st.write("##### 使い方")
st.write("1. 相談したい分野の専門家をラジオボタンから選択してください")
st.write("2. テキストエリアに質問や相談内容を入力してください")
st.write("3. 「回答を得る」ボタンをクリックすると、選択した専門家の視点から回答が表示されます")

# 専門家タイプの定義
experts = {
    "マーケティング専門家": "You are a marketing expert with extensive experience in digital marketing, branding, and customer acquisition. Provide strategic insights and practical advice based on your expertise.",
    "技術コンサルタント": "You are a technical consultant with deep expertise in software architecture, system design, and technology selection. Provide technical insights and best practices based on your knowledge.",
    "ビジネス分析家": "You are a business analyst with expertise in business process optimization, data analysis, and strategic decision-making. Provide analytical insights and actionable recommendations based on your expertise."
}

def get_expert_response(user_input: str, expert_type: str) -> str:
    """
    ユーザー入力と専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        user_input (str): ユーザーからの入力テキスト
        expert_type (str): ラジオボタンで選択された専門家のタイプ
    
    Returns:
        str: LLMからの回答
    """
    # LLMの初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    
    # システムメッセージを選択された専門家タイプに基づいて設定
    system_message = experts[expert_type]
    
    # メッセージの構築
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input),
    ]
    
    # LLMに問い合わせて回答を取得
    result = llm(messages)
    
    return result.content


# 専門家の選択
selected_expert = st.radio(
    "相談したい分野を選択してください。",
    list(experts.keys())
)

st.divider()

# テキスト入力フォーム
user_input = st.text_area(
    "質問や相談内容を入力してください。",
    placeholder="例：新製品を市場に投入する際の戦略について教えてください",
    height=150
)

# 送信ボタン
if st.button("回答を得る"):
    st.divider()
    
    if user_input.strip():
        # ローディング表示
        with st.spinner("回答を生成中..."):
            # 関数を使用して回答を取得
            response = get_expert_response(user_input, selected_expert)
        
        # 回答を表示
        st.write(f"##### {selected_expert}からの回答")
        st.write(response)
    
    else:
        st.error("質問や相談内容を入力してから「回答を得る」ボタンを押してください。")