# QR Kod ve Video İşleme Uygulaması

Bu proje, QR kodları tespit etmek ve belirli bir süre boyunca video kaydetmek için kullanılan bir Python uygulamasını içerir.

## Nasıl Kullanılır

1. **QR Kodları Okuma ve Kaydetme:**
   - `QR_Code.py` dosyası, QR kodlarını okur ve belirtilen bir dosyaya kaydeder.
   - `QrKodKaydedici` sınıfı, QR kodlarını kaydeden ve daha önce kaydedilen kodları tutan bir yapı sağlar.
   - Görüntü üzerinde QR kodlarını bulmak ve içeriğini kaydetmek için OpenCV ve pyzbar kütüphaneleri kullanılmıştır.
   
2. **Video Kaydı ve İzleme:**
   - `video.py` dosyası, belirli bir süre boyunca video kaydı yapar ve her bir saniyelik segmenti ayrı dosyalar olarak kaydeder.
   - `video_parcalari_kaydet` fonksiyonu, video kaydı yaparken zaman ve konum bilgisini her kareye ekler.
   - Kaydedilen videoları sırayla izlemek için `videolari_sirala_ve_izle` fonksiyonu kullanılır.
   
3. **Çoklu İş Parçacığı ile Eş Zamanlı Çalıştırma:**
   - İki Python betiği, aynı anda çalıştırılmak üzere ayrı iş parçacıklarında başlatılır.
   - `threading` ve `subprocess` modülleri kullanılarak bu işlem gerçekleştirilir.
   
## Kurulum

1. Gerekli kütüphaneleri yüklemek için aşağıdaki komutları kullanın:
    pip install opencv-python pyzbar geocoder
2. `QR_Code.py` ve `video.py` dosyalarını çalıştırarak uygulamayı başlatın.

## Proje Yapısı

- `QR_Code.py`: QR kodlarını okuma ve kaydetme işlemlerini gerçekleştiren Python dosyası.
- `video.py`: Video kaydı ve izleme işlemlerini gerçekleştiren Python dosyası.
- `video_kayitlari/`: Video dosyalarının kaydedildiği klasör.
- `qr_kodlar.txt`: Kaydedilen QR kodlarının tutulduğu dosya.
- `README.md`: Proje hakkında açıklamaları içeren dosya.

## Lisans

Bu proje, [ILGERU-UAV Lisansı]([ILGERU](https://www.linkedin.com/company/ilgeruav/?originalSubdomain=tr)) altında lisanslanmıştır. Daha fazla bilgi için lisans dosyasını inceleyebilirsiniz.
