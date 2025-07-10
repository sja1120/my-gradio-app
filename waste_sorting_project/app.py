import gradio as gr
import pandas as pd
import difflib
import os

# CSV 파일 불러오기
df = pd.read_csv("trash_data_extended.csv")

def classify_text(user_input):
    user_input = user_input.strip()
    items = df['item'].tolist()
    tips = df['tips'].tolist()

    # item, tips에 입력값이 포함된 품목 찾기
    item_matches = [item for item in items if user_input in item]
    tip_matches = [items[i] for i, tip in enumerate(tips) if user_input in str(tip)]
    combined_matches = list(dict.fromkeys(item_matches + tip_matches))

    # 오타 보정: item, tips 모두에서 유사 품목 추천
    close_item_matches = difflib.get_close_matches(user_input, items, n=5, cutoff=0.5)
    close_tip_matches = [items[i] for i, tip in enumerate(tips)
                         if difflib.SequenceMatcher(None, user_input, str(tip)).ratio() > 0.5]
    close_combined = list(dict.fromkeys(close_item_matches + close_tip_matches))

    candidates = combined_matches or close_combined

    if candidates:
        main_item = candidates[0]
        row = df[df['item'] == main_item]
        if not row.empty:
            category = row['category'].values[0]
            tips_val = row['tips'].values[0]
            trash_type = row['type'].values[0]
            suggestions = candidates[1:]
            main_result = f"♻️ 분리배출 유형: {trash_type}\n✅ 분류: {category}\n💡 팁: {tips_val}"
            return main_result, suggestions
    return "❗ 해당 품목은 데이터에 없어요. 다른 걸 입력해보세요.", []

with gr.Blocks(title="분리배출 AI 가이드") as demo:
    gr.Markdown("### ♻️ 분리배출 AI 가이드\n텍스트 입력만으로 분리배출 정보를 안내해줍니다.")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="분리배출 품목 이름 또는 키워드 입력")
            text_output = gr.Textbox(label="검색 결과")
            suggestion_state = gr.State([])
            suggestion_buttons = [gr.Button("", visible=False) for _ in range(5)]

    def update_suggestions(user_input):
        result, suggestions = classify_text(user_input)
        padded_suggestions = suggestions + [""] * (5 - len(suggestions))
        btn_updates = []
        for i, s in enumerate(padded_suggestions):
            btn_updates.append(gr.update(value=s, visible=bool(s)))
        return [result] + btn_updates + [suggestions]

    text_input.change(
        update_suggestions,
        inputs=text_input,
        outputs=[text_output] + suggestion_buttons + [suggestion_state]
    )

    def suggestion_click(suggestion, state):
        if suggestion:
            result, suggestions = classify_text(suggestion)
            padded_suggestions = suggestions + [""] * (5 - len(suggestions))
            btn_updates = []
            for i, s in enumerate(padded_suggestions):
                btn_updates.append(gr.update(value=s, visible=bool(s)))
            return [suggestion, result] + btn_updates + [suggestions]
        else:
            btn_updates = [gr.update(visible=False) for _ in range(5)]
            return [gr.update(), gr.update()] + btn_updates + [[]]

    for i, btn in enumerate(suggestion_buttons):
        btn.click(
            suggestion_click,
            inputs=[btn, suggestion_state],
            outputs=[text_input, text_output] + suggestion_buttons + [suggestion_state]
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)