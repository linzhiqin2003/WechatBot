from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

# model_id = "ep-20241015211239-c5hv6"
def reply_by_assistant_single(msg,model_id):
    completion = client.chat.completions.create(
        model=model_id,
        messages = msg,
        )
    return completion.choices[0].message.content
