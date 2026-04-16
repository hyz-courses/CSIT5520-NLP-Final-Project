# CSIT5520 NLP Final Project

A multi-purpose modular RAG pipeline powered by dify.

## Backend Maintenance Guide

Maintainence with `systemctl`:

```bash
sudo systemctl _______ csit5520-backend
               enable       -> register startup when boot
               start        -> Start service
               status       -> Inspect status
               restart      -> Restart Service
               stop         -> stop service
```

> [!NOTE] Make sure you stop the service when start making changes to the code.

View logs with `journalctl`:

```bash
sudo journalctl \
-u csit5520-backend \
______
-f      -> Realtime View Log
-n 100  -> Read first 100 lines
-p err  -> Only view err level or above
```

Deal with milvus corruption:

```bash
bash standalone_embed.sh delete
bash standalone_embed.sh restart

# Re-connect milvus to docker network
docker network connect docker_default milvus-standalone
```