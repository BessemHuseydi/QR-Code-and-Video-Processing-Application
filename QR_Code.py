import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import os
import geocoder

class QrKodKaydedici:
    """
    QR kodlarını dosyaya kaydetmek için kullanılan sınıf.
    """
    def __init__(self, dosya_adi):
        """
        Sınıfın kurucu fonksiyonu.
        
        Args:
            dosya_adi (str): Kaydedilen QR kodlarının tutulacağı dosya adı.
        """
        self.kayitEdildi= None
        self.dosya_adi = dosya_adi
        self.kaydedilmis_kodlar = set()  # Daha önce kaydedilen kodları tutar.

        # Dosya yoksa oluştur.
        if not os.path.exists(self.dosya_adi):
            with open(self.dosya_adi, "w") as dosya:
                pass

    def qr_kod_kaydet(self, qr_kod_icerigi):
        """
        QR kodunu kaydedilenler listesine ve dosyaya ekler.
        
        Args:
            qr_kod_icerigi (str): QR kodunun içeriği.
        """
        if qr_kod_icerigi in self.kaydedilmis_kodlar:
            return  # QR kodu zaten kaydedilmişse işlem yapma.
        self.kaydedilmis_kodlar.add(qr_kod_icerigi)
        with open(self.dosya_adi, "a") as dosya:
            dosya.write(qr_kod_icerigi + "\n")
        self.kayitEdildi=True
        
    def qr_kod_oku(self,goruntu, qr_kod_kaydedici):
        """
        Görüntü içerisinden QR kodunu okur ve kaydeder.
        
        Args:
            goruntu (ndarray): QR kodunun okunacağı görüntü.
            qr_kod_kaydedici (QrKodKaydedici): QR kod kayıtlarını yöneten sınıf örneği.
        
        Returns:
            list, str: QR kodunun sınırlayıcı kutusu ve içeriği.
        """
        list1 = []
        qr_kodlar = decode(goruntu)

        if qr_kodlar:
            qr_kod_icerigi = qr_kodlar[0].data.decode("utf-8")
            x1, y1, w, h = qr_kodlar[0].rect
            x2, y2 = x1 + w, y1 + h
            list1.extend([x1, y1, x2, y2])
            qr_kod_kaydedici.qr_kod_kaydet(qr_kod_icerigi)
            self.kayitEdildi = True
            return list1, qr_kod_icerigi
        else:
            return None,None

    def get_location(self):
        """
        Cihazın IP adresine dayanarak coğrafi konum bilgilerini alır.
        
        Returns:
            str: Ülke, şehir ve koordinatlar içeren konum bilgisi.
        """
        g = geocoder.ip('me')
        return f"{g.country}, {g.city}, {g.latlng}"

    def goruntuyu_isleme(self,goruntu, qr_kod_kaydedici):
        """
        Görüntü üzerinde QR kodunu okur, sonuçları görüntüye ekler.
        
        Args:
            goruntu (ndarray): QR kodunun okunacağı ve üzerine yazı yazılacak görüntü.
            qr_kod_kaydedici (QrKodKaydedici): QR kod kayıtlarını yöneten sınıf örneği.
        
        Returns:
            ndarray: Üzerine yazı yazılmış görüntü.
        """
        gri_tonlama_goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
        list1, qr_kod_icerigi = self.qr_kod_oku(gri_tonlama_goruntu, qr_kod_kaydedici)

        if qr_kod_icerigi:
            zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            konum = "54"#get_location()
        
            cv2.putText(goruntu, qr_kod_icerigi, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(goruntu, zaman, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(goruntu, konum, (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.rectangle(goruntu, (list1[0], list1[1]), (list1[2], list1[3]), (0, 0, 255), 2)

        return goruntu

def klasordeki_videolari_isle(klasor_yolu,qr_kod_kaydedici):
    """
    Bir klasördeki tüm video dosyalarını sırayla işler.
    
    Args:
        klasor_yolu (str): Video dosyalarının bulunduğu klasörün yolu.
    """
    video_dosyalari = [os.path.join(klasor_yolu, f) for f in os.listdir(klasor_yolu) if f.endswith('.mp4')]
    print(video_dosyalari)
    video_dosyalari.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or -1))

    

    for video_yolu in video_dosyalari:
        print(f"{video_yolu} işleniyor...")
        cap = cv2.VideoCapture(video_yolu)

        if not cap.isOpened():
            print(f"{video_yolu} dosyası açılamadı!")
            continue
        
        while True:
            ret, goruntu = cap.read()
            if not ret:
                break  
            goruntu = qr_kod_kaydedici.goruntuyu_isleme(goruntu, qr_kod_kaydedici)
            cv2.waitKey(100)
            cv2.imshow("QR Kod Okuyucu", goruntu)

        cap.release()
        cv2.destroyAllWindows()
        print(qr_kod_kaydedici.kayitEdildi)
        if qr_kod_kaydedici.kayitEdildi == True:             
            break



qr_kod_kaydedici = QrKodKaydedici("qr_kodlar.txt")
klasor_yolu = 'video_kayitlari'  # Video dosyalarının bulunduğu klasörün yolu
klasordeki_videolari_isle(klasor_yolu,qr_kod_kaydedici)

   
        