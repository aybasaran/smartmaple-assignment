## Projenin Amacı

KitapYurdu sitesinden kitap bilgilerini kazıyıp, MongoDB veritabanına kaydeden bir uygulama geliştirmek.

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

KitayYurdu.com sitesi static bir site olduğu için, requests kütüphanesi ile sayfaları istek atarak alabiliyoruz. Daha sonra BeautifulSoup kütüphanesi ile sayfaları parse ediyoruz. Siteyi biraz incelediğimizde kitapyurdu.com/index.php?route=product/category&sort=purchased_365&order=DESC&path=1&filter_category_all=true&filter_in_shelf=1 şöyle bir url ile karşılaşıyoruz. Parametreleri incelediğimizde bütün kategorilerdeki kitapları listeleyebileceğimizi farkediyoruz. Bu url ile istek atıp, gelen sayfayı parse ediyoruz. Pagination olduğu için sayfaları dolaşmak gerekiyor. Pagination için gelen sayfadaki pagination div'ini bulup, içindeki toplam sayfa sayısını buluyoruz. Daha sonra for döngüsü ile sayfaları dolaşıyoruz. Her bir kitap .product-cr class'ına sahip. Bu class'ı bulup, içindeki bilgileri çekiyoruz. Çektiğimiz bilgileri bir dict'e atıyoruz. Daha sonra bu dict'i MongoDB veritabanına kaydediyoruz.

## Projenin Özellikleri

- [x] Kitap bilgilerini kazıma
- [x] Kitap bilgilerini MongoDB veritabanına kaydetme
- [x] Uzun bir süreç olduğu için (200 sayfa iterasyonu ile yaklasik 15K kitap bilgisi çektim), her 100 kitapta bir kaldığımız yerin kaydedilmesi

## Linkler

[Kazılmış Örnek Kitaplar](https://drive.google.com/file/d/1PK0uotnxCXOeiQvYFfISxYovwITYpGAZ/view?usp=sharing)
