import cv2
import os
import shutil
from datetime import datetime

def video_parcalari_kaydet(baslangic_sayaci, sure_saniye, konum, fps=20, klasor='video_kayitlari'):
    """
    Belirli bir süre boyunca video kaydeder ve her bir saniyelik segmenti ayrı bir dosya olarak kaydeder.
    
    Args:
    baslangic_sayaci (int): Dosya adlandırmada kullanılacak başlangıç sayısı.
    sure_saniye (int): Video kaydının süresi, saniye olarak.
    konum (str): Videoda gösterilecek konum bilgisi.
    fps (int): Videonun saniyedeki kare sayısı. Varsayılan değer 20.
    klasor (str): Video dosyalarının kaydedileceği klasörün adı. Varsayılan değer 'video_kayitlari'.
    """
    # Klasör yoksa oluştur
    if not os.path.exists(klasor):
        os.makedirs(klasor)
    
    # Video yakalama nesnesi
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("http://192.168.1.102:8080/")
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Her bir saniye için bir video dosyası oluştur
    for i in range(sure_saniye):
        video_adi = f'{klasor}/kayit_{baslangic_sayaci + i}.mp4'
        out = cv2.VideoWriter(video_adi, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        baslangic_zamani = datetime.now()
        
        # 1 saniyelik video kaydı 
        while (datetime.now() - baslangic_zamani).seconds < 1:
            ret, frame = cap.read()
            if ret:
                # Zaman ve konum bilgisini frame üzerine yaz
                zaman_bilgisi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cv2.putText(frame, f'Zaman: {zaman_bilgisi} Konum: {konum}', (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                out.write(frame)
                # cv2.imshow('Video Kaydediliyor...', frame)

        out.release()

    cap.release()
    cv2.destroyAllWindows()



def videolari_sirala_ve_izle(klasor='video_kayitlari'):
    """
    Belirli bir klasördeki tüm video dosyalarını sıralar ve ardından izler.
    
    Args:
    klasor (str): Video dosyalarının bulunduğu klasörün adı. Varsayılan değer 'video_kayitlari'.
    """
    # Video dosyalarını bul ve sırala
    video_dosyalari = [os.path.join(klasor, f) for f in os.listdir(klasor) if f.endswith('.mp4')]
    video_dosyalari.sort()

    # Sırayla her bir videoyu izle
    for video_yolu in video_dosyalari:


        cap = cv2.VideoCapture(video_yolu)

        if not cap.isOpened():
            print(f"{video_yolu} dosyası açılamadı!")
            continue

        print(f"{video_yolu} izleniyor...")
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Video', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

def klasor_temizle(klasor):
    """
    Belirli bir klasördeki tüm dosya ve alt klasörleri siler.
    
    Args:
   

 klasor (str): Temizlenecek klasörün adı.
    """
    # Klasördeki dosya ve alt klasörleri sil
    if os.path.exists(klasor):
        shutil.rmtree(klasor)
        print(f"'{klasor}' klasorundeki tum dosyalar basariyla silindi.")
    else:
        print(f"'{klasor}' klasörü bulunamadı.")

# Örnek kullanım
klasor_temizle('video_kayitlari')
video_parcalari_kaydet(baslangic_sayaci=1, sure_saniye=5, konum='Turkiye', fps=20)
# videolari_sirala_ve_izle('video_kayitlari')
