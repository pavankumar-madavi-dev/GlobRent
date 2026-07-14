# १. अधिकृत पायथन इमेज वापरूया
FROM python:3.11-slim

# २. ऑपरेटिंग सिस्टम अपडेट करून SSH साठी आवश्यक गोष्टी इन्स्टॉल करूया
RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*

# ३. प्रोजेक्ट डिरेक्टरी सेट करूया
WORKDIR /app

# ४. लायब्ररीजची फाईल कॉपी करून इन्स्टॉल करूया
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ५. सर्व कोड कॉपी करूया
COPY . .

# ६. अ‍ॅप रन करण्याची कमांड
CMD ["python", "main.py"]
