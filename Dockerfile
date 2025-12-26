## syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV POEMS_CSV_PATH=data/poems.csv

EXPOSE 8000
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
diff --git a/Dockerfile b/Dockerfile
new file mode 100644
index 0000000000000000000000000000000000000000..f716fa4274da364f6bbc2ca91a20d3511c49e817
--- /dev/null
+++ b/Dockerfile
@@ -0,0 +1,12 @@
+FROM python:3.11-slim
+
+WORKDIR /app
+
+COPY requirements.txt ./
+RUN pip install --no-cache-dir -r requirements.txt
+
+COPY . .
+ENV POEMS_CSV_PATH=data/poems.csv
+
+EXPOSE 8000
+CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
