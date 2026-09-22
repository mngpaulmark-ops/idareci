# Otomatik Güncelleme Kuralý

Kullanýcý sana "güncelle", "sistemi güncelle" veya benzeri bir komut verdiðinde, görevin terminal üzerinden þu komutlarý sýrasýyla çalýþtýrmaktýr:

1. git add .
2. git commit -m "Otomatik güncelleme: Vercel, Neon ve Github"
3. git push origin main

Bu komutlar, projedeki tüm deðiþiklikleri GitHub'a gönderecek ve Vercel'in otomatik olarak yeni versiyonu yayýnlamasýný saðlayacaktýr. Ýþlem bitince kullanýcýya Vercel'in güncellendiðini haber ver.
