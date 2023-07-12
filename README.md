## Projenin Amacı

Kitapyurdu ve Kitapsepeti sitelerindeki kitapları kazıyıp, MongoDB veritabanına kaydetmek.

## Kullanılan Teknolojiler

- Python 3.11.4
- BeautifulSoup (bs4)
- MongoDB (PyMongo)

## Kurulum

Projeyi klonlayın.

```bash
git clone https://github.com/aybasaran/smartmaple-assignment.git
```

Proje dizinine gidin

```bash
cd smartmaple-assignment
```

Gerekli paketleri yükleyin.

```bash
pip install -r requirements.txt
```

Uygulamayı çalıştırın.

```bash
python app.py
```

## Nasıl Çalışır?

Kitapyurdu.com ve Kitapsepeti.com siteleri static bir site olduğu için, requests kütüphanesi ile sayfaları istek atarak alabiliyoruz. Daha sonra BeautifulSoup kütüphanesi ile sayfaları parse ediyoruz. Öncelikle sitede tüm kitapları tek seferde listelemek için url olup olmadığını araştıyoruz. Kendi araştırmalarım sonucunda kitapyurdun'da index.php?route=product/category&filter_category_all=true&path=1&filter_in_stock=1&filter_in_shelf=1&sort=purchased_365&order=DESC&limit=100 gibi bir url
in yapıcağımız işe uygun olduğunu fark ediyorum.Kitapsepeti.com'da /roman?stock=1 üzerinden ilerliyor olacağız. İki site'de öncelikle kaç adet sayfa olduğunu bulmak için ilgili pagination elementlerinin içini scrape ederek gerekli veriyi parse ediyoruz. Bunu sayfaları gezinmekte kullanacağız. Daha sonra sayfaları gezerek kitapların bulunduğu div elementlerini scrape ediyoruz. Bu elementlerin içindeki bilgileri parse ederek, kitap bilgilerini elde ediyoruz. Daha sonra bu bilgileri MongoDB veritabanına kaydediyoruz. Bu işlemi yaparken, her sayfada bir kaldığımız yerin kaydedilmesini sağlıyoruz. Böylece program herhangi bir sebepten dolayı durduğunda, kaldığı yerden devam edebiliyor.

## Projenin Özellikleri

- [x] Kitap ve pagination bilgilerinin kazıma
- [x] Kitap bilgilerini MongoDB veritabanına kaydetme
- [x] Her Sayfa başlangıcında kaldığı yerin kaydedilmesi

## Linkler

[Kazılmış Örnek Kitaplar - Kitapyurdu](https://drive.google.com/file/d/1PK0uotnxCXOeiQvYFfISxYovwITYpGAZ/view?usp=sharing)
[Kazılmış Örnek Kitaplar - Kitapsepeti](https://drive.google.com/file/d/1m5sSmST6FmOBohUmERyvLY4fJnNiDngF/view?usp=sharing)

## Ekran Görüntüleri

Giriş ekranı
![Komut Satırı giriş](https://gcdnb.pbrd.co/images/zlg3JpX4w8R8.png)

Kitapyurdu.com kazıma
![Komut Satırı seçim](https://gcdnb.pbrd.co/images/6vZPFAofAHSI.png)

Kitapsepeti.com Çıktı
![Komut Satırı çıktı](https://gcdnb.pbrd.co/images/ZjnTalRXMrBk.png)
