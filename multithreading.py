import threading
import subprocess

def run_script(script_name):
    # subprocess.call fonksiyonu ile Python scripti çalıştırılır
    subprocess.call(["python", script_name])

# dosya1.py ve dosya2.py için iki iş parçacığı oluştur
t1 = threading.Thread(target=run_script, args=("video.py",))
t2 = threading.Thread(target=run_script, args=("QR_Code.py",))

# İş parçacıklarını başlat
t1.start()
t2.start()

# Her iki iş parçacığının da bitmesini bekleq
t1.join()
t2.join()

print("Her iki script de çalıştırıldı.")