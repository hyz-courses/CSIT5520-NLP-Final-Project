curl -X POST https://dify.docsearch.love/v1/chat-messages \
  -H "Authorization: Bearer <replace_with_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "你好，请介绍一下你自己",
    "user": "direct-test",
    "response_mode": "streaming",
    "inputs": {},
    "conversation_id": null
  }' \
  -N \
  -k \
  --max-time 60 \
  -v