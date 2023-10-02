import requests
def create( content ):
    # 日記内容をOpenAIに投げる
    api_key = ""
    header = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {api_key}",
    }
    body = {
        "model": "gpt-4-0613",
        "messages": [
            {"role": "system", "content": "あなたは、大阪のおかん。一人称はおかん。歳は49歳です。大阪のおかんらしく、元気で明るく振る舞ってください。次の文章は息子の文書です。100文字程度で簡潔にコメントしてください。"}, 
            {"role": "user", "content":f"{content}"},
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers = header, json = body)
    rj = response.json()
    return rj
