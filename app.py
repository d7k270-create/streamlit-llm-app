import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Streamlitページ設定
st.set_page_config(page_title="Expert LLM Assistant", layout="wide")

# ページタイトルと説明
st.title("🤖 エキスパート LLM アシスタント")
st.markdown("""
### 📋 使い方
1. **専門家を選択**: ラジオボタンから、相談したい分野の専門家を選択してください
2. **質問を入力**: テキストボックスに質問や相談内容を入力してください
3. **送信ボタンをクリック**: 「回答を得る」ボタンをクリックすると、選択した専門家の視点から回答が表示されます

### 🎯 利用可能な専門家
- **マーケティング専門家**: マーケティング戦略、ブランディング、顧客獲得について
- **技術コンサルタント**: ソフトウェア設計、システムアーキテクチャ、技術選定について
- **ビジネス分析家**: ビジネスプロセス、データ分析、意思決定について

---
""")

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


# サイドバーでレイアウト
with st.sidebar:
    st.header("⚙️ 設定")
    
    # 専門家の選択
    selected_expert = st.radio(
        "相談したい分野を選択してください：",
        options=list(experts.keys()),
        index=0
    )

# メインエリア
st.subheader("💬 質問・相談内容")

# テキスト入力フォーム
user_input = st.text_area(
    "ここに質問や相談内容を入力してください：",
    placeholder="例：新製品を市場に投入する際の戦略について教えてください",
    height=150,
    label_visibility="collapsed"
)

# 送信ボタン
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("回答を得る", type="primary"):
        if user_input.strip():
            # ローディング表示
            with st.spinner("回答を生成中..."):
                # 関数を使用して回答を取得
                response = get_expert_response(user_input, selected_expert)
            
            # 回答を表示
            st.divider()
            st.subheader(f"📝 {selected_expert}からの回答")
            st.markdown(response)
            st.divider()
        else:
            st.warning("⚠️ 質問や相談内容を入力してください")