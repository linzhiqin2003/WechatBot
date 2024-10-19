def flow_monitoring(user_name,messages):
    # 日志记录流量监控
    messages_list = [content['content'] for content in messages]
    word_amount = sum([(len(messages_list[i]) * (len(messages_list) - i)) for i in range(len(messages_list))])
    record = f'Session{user_name} has used token(approximately)：{word_amount}'
    return record


# 动态管理上下文长度
def context_management(message):
    adjusted_context = message
    # 计算当前上下文长度
    context_length = sum([len(content['content']) for content in message])
    # 如果超过2000个字，那就将记忆缩短到两千字内
    if context_length > 2000:
        adjusted_context = [message[0]].extend(message[3:])
        return context_management(adjusted_context)
    return adjusted_context




