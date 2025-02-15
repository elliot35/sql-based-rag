#!/bin/bash

if [ "$LLM_PROVIDER" = "local" ]; then
    echo "Downloading LLama model..."
    wget -O models/llama-2-7b-chat.gguf \
        https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
    echo "Model downloaded successfully"
else
    echo "Using OpenAI API, no model download needed"
fi 