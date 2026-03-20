curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -H "Accept: text/event-stream" \
    -d '{
        "query": "如何租房",
        "user": "test-user",
        "conversation_id": null,
        "inputs": {}
    }' \
    -N \
    -k \
    --max-time 60 \
    -v