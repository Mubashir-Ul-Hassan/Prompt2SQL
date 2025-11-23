FROM ollama/ollama:latest AS ollama

FROM python:3.10-slim

# Copy Ollama from the builder image
COPY --from=ollama /usr/bin/ollama /usr/bin/ollama
COPY --from=ollama /root/.ollama /root/.ollama

# Install Python dependencies
RUN pip install --no-cache-dir streamlit pandas openpyxl sqlite-utils requests altair

# Copy app
WORKDIR /app
COPY . .

# Pull model during build (choose your model)
RUN ollama pull llama3.1:8b

EXPOSE 8501

CMD ollama serve & streamlit run app.py --server.port 8501 --server.address 0.0.0.0
