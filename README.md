# <b>DYOS-1 PORT SCANNER</b>

### <b>PROJE AMACI</b> 
<p>Sistemde çalışan uygulamaların potansiyel güvenlik zafiyetlerini tespit etmek ve kullanıcıya bu zafiyetlerin adlarını ve ilişkili kaynaklardaki daha fazla bilgiye erişebilecekleri linkleri sunmaktır.</p>

### <b>PROJE ÖZELLİKLERİ</b>
<p>Sistemdeki portları tarama: Proje, belirli bir IP adresinde veya IP aralığında çalışan uygulamaları ve portlarını tarayarak tespit edecektir.</p>
<p>Uygulama ve zafiyet araştırması: Taranan uygulamalar ile ilgili veritabanındaki ve internet kaynaklarındaki bilgiler kullanılarak potansiyel güvenlik zafiyetleri tespit edilecektir.</p>
<p>Kullanıcıya bilgi sunma: Tespit edilen zafiyetlerin adları ve ilişkili kaynaklardaki daha fazla bilgiye erişebilecekleri linkler kullanıcıya sunulacaktır.</p>
<p></p>

### <b>PROJENİN KULLANIMI</b>
* "--ip" argümanı: Tarama yapmak istediğiniz hedefin IP bilgisini girin.
* "--port" argümanı: Tarama yapmak istediğiniz hedefin port bilgisini girin.
* "--file" argümanı: Hedef veya hedeflerle ilgili IP ve port bilgilerini içeren bir txt dosyası vermenizi sağlar. Bu argümanı kullandığınızda "--ip" ve "--port" argümanlarını kullanmanıza gerek kalmaz.
* "--ping" argümanı: Ping taraması, hedefinizin aktif durumda olup olmadığını tespit eder ve size sunar.
* "--tcpsyn" argümanı: TCP SYN taraması, ağda mevcut olan açık TCP portlarını taramak için kullanılan bir tarama türüdür.
* "--os" argümanı: Hedef sistemin işletim sistemini tespit etmek için kullanılır.
* "--showcve" argümanı: DYOS, portlar üzerinde tespit ettiği sürüm veya uygulama bilgisine göre web'den çeşitli kaynaklardan bilgi toplayabilir. Bu bilgi ilgili CVE'leri içerir.
 * "--askdb" argümanı: DYOS, çeşitli kaynaklardan elde ettiği CVE'leri saklar. Bu parametreyi kullanarak web araması yapmadan basit bir sonuç alabilirsiniz.

### <b>GEREKLILIKLER</b>
<p>Python3.10 programlama dili kullanılarak kodlanmıştır. Bu nedenle, projemizi çalıştırmak için Python3.10 veya üstü sürümlerinin yüklü olması gerekir. Ayrıca, projemizde ipaddress, , argparse, python-nmap, requests, beautifulSoup4 ve lxml kütüphanelerini kullanmaktayız. Bu kütüphanelerin yüklü olması, projemizin doğru bir şekilde çalışması için gereklidir. Eğer bu kütüphaneler yüklü değilse, projemizi çalıştırmak için öncelikle bu kütüphaneleri yüklemeniz gerekmektedir. Örnek olarak <b>"pip install -r requipments.txt"</b> gibi komutları kullanabilirsiniz. Projemiz arkada oluşturduğu paketler ve işlemlerden dolayı çalıştığı sistemde super user (su) yetkisine ihtiyaç duymaktadır.</p>

### <b>ÖRNEK KULLANIM</b>
- <p>"--ip": Projemiz, kullanıcının belirli bir hedef IP veya IP bloğunu taramak için kullanabileceği "--ip" argümanını sunmaktadır. Örneğin, kullanıcı "python3 dyos.py --ip 192.168.1.1" şeklinde komutu kullanarak 192.168.1.1 IP adresini tarayabilir veya "python3 dyos.py --ip 192.168.1.0/24" şeklinde kullanarak 192.168.1.0/24 IP bloğunu tarayabilir. Bu argümanın kullanımı ile hedef IP veya IP bloğu belirtilir ve proje tarama işlemlerini bu IP veya IP bloğu üzerinde gerçekleştirir.</p>
- ```python3 dyos.py --ip 192.168.1.1```
- ```python3 dyos.py --ip 192.168.1.0/24```
<br><br>
- <p>"--port" argümanı ile, hedef sistemdeki taranacak portları belirleyebilirsiniz. Kullanıcı, tek bir port numarası olarak (örneğin "80") ya da birden fazla port numarası olarak (örneğin "80,443,22") ya da bir port aralığı olarak (örneğin "1-100") belirtebilir. Örnek kullanım: "--port 80" veya "--port 1-100" veya "--port 80,443,22" gibi. Bu şekilde belirlenen portlar aracılığıyla, hedef sistemdeki açık portlar tespit edilerek tarama yapılır.</p>
- ```python3 dyos.py --port 23```
- ```python3 dyos.py --port 23,24,25```
- ```python3 dyos.py --port 1-100```
<br><br>
- <p>"--file" argümanı, kullanıcının hedefleri bir txt dosyası olarak tanımlama seçeneğidir. Bu argümanı kullanarak, kullanıcı "--ip" veya "--port" argümanlarını kullanmak yerine, tarama işlemini gerçekleştirmek istediği hedefleri içeren bir txt dosyasını verir. Bu dosya, her satırda sadece bir hedef içermelidir ve bu hedef, IP adresi veya IP adresi ve port numarası şeklinde yazılmalıdır. Örneğin, "192.168.1.1:80" veya "192.168.1.1" şeklinde. Bu argümanın kullanımı, tarama işlemlerini önceden tanımlanmış hedefler üzerinde gerçekleştirmek için kullanıcıya pratik bir seçenek sunar.</p>
- ```python3 dyos.py --file list.txt```
- list.txt: <br>![image](https://user-images.githubusercontent.com/102908626/215258511-bf64d776-1a95-4765-9228-31e9d5b91e21.png)
<br><br>
- <p>--ping taraması, kullanıcının belirlediği hedef sistemin aktif olup olmadığını tespit etmek için kullanabileceği bir tarama türüdür. Bu parametre kullanıldığında --port parametresine ihtiyaç duyulmaz ve boolean bir parametredir. Yani kullanıcı --ping parametresini kullanmak istiyorsa, sadece "--ping" olarak komut satırına yazması yeterlidir. Bu argüman kullanılması halinde sadece sistemin aktif olup olmadığını tespit etmek için kullanılır.</p>
- ```python3 dyos.py --ip 192.168.72.129 --ping```
- ![image](https://user-images.githubusercontent.com/102908626/215259085-8ab5e7ba-bc84-48c4-948d-972c20dab694.png)
<br><br>
- <p>"--tcpsyn" parametresi, hedef sistemin belirtilen portlarını taramak için kullanılabilir. Bu parametre boolean bir parametredir ve kullanıldığında, hedef sistemin belirtilen portlarındaki uygulamaların varlığını ve çalışma durumlarını tespit etmeye çalışır. Bu tarama yöntemi, TCP SYN tarama yöntemi olarak bilinir ve sistemlerdeki açık TCP portlarını tespit etmek için kullanılır. Örnek olarak, "--tcpsyn" parametresi kullanılarak belirtilen portlar arasındaki açık portları tespit etmek mümkündür.</p>
- ```python3 dyos.py --ip 192.168.72.129 --port 1-100 --tcpsyn```
- ![image](https://user-images.githubusercontent.com/102908626/215259561-654162fc-65a4-477a-960d-4b59634debc1.png)
<br><br>
- "--os" parametresi, kullanıcının hedef sistemin işletim sistemini tespit etmesini sağlar. Bu parametre, --tcpsyn parametresi ile birlikte kullanılması gerekir çünkü --tcpsyn parametresi hedef sistemde çalışan uygulamaları tespit etmek için kullanılırken, --os parametresi bu uygulamaların işletim sistemi ile ilişkilendirmek için kullanılır. Bu parametre, tarama işlemi sırasında hedef sistemin işletim sistemi hakkında bilgi verir ve kullanıcının sistemi daha iyi anlamasını ve açıkları tespit etmesini sağlar.
- ```python3 dyos.py --ip 192.168.72.129 --port 1-100 --tcpsyn --os```
- ![image](https://user-images.githubusercontent.com/102908626/215260378-1c6c1838-7634-4a0d-b7c5-1fad648810c1.png)
<br><br>
- <p>"--showcve" parametresi kullanıldığında internet üzerinden taranan portlarda çalışan uygulamalar hakkında bir CVE'nin bulunup bulunmadığına bakar. Bu parametre ile birlikte, araştırma derinliği adında bir parametre de alınabilir. Bu derinlik arttıkça, tarama sonucunda bulunan potansiyel CVE sayısı artabilir. Bu sayede, kullanıcının güvenlik açıkları hakkında daha detaylı bilgiye sahip olması sağlanır.</p>
- ```python3 dyos.py --ip 192.168.72.129 --port 21 --tcpsyn --showcve 1```
- ![image](https://user-images.githubusercontent.com/102908626/215260859-590ce863-aa0d-4fe2-b37a-89a3d476b5fd.png)
<br><br>
- <p>"--askdb" parametresi, DYOS tarafından toplanan ve saklanan çeşitli kaynaklardan elde edilen CVE (Common Vulnerabilities and Exposures) bilgilerini içeren veritabanından arama yapmanıza olanak tanır. Bu parametre ile, internet üzerinden arama yapmak yerine, veritabanındaki 47 bin veri arasından arama yapabilirsiniz. Bu sayede arama işlemi daha hızlı gerçekleşir ve daha doğru sonuçlar elde edersiniz. Ayrıca, --askdb boolean bir parametredir ve kullanımı oldukça basittir. Sadece "--askdb" yazmanız yeterlidir ve DYOS otomatik olarak veritabanındaki bilgileri tarar ve sonuçları size sunar.</p>
- ```python3 dyos.py --ip 192.168.72.129 --port 21 --tcpsyn --askdb```
- ![image](https://user-images.githubusercontent.com/102908626/215261323-138e399c-3ef7-4bd3-a37c-03e2097d2631.png)
<br><br>
- <p><b>Önemli not: Yukarıda yer alan tüm görseller, Metasploitable 2'ye gönderilen ilgili sorguların sonuçlarıdır.</b></p>
<br><br>
### <b>SONUÇ</b>
- DYOS (Defend Your Own System) projesi, ilk aşaması tamamlanarak, hedeflenen tüm maddelerin gerçekleştirilmeye uygun hale getirildi. Proje, geliştirilebilirlik açısından sınırsız olarak değerlendirilmektedir ve bu nedenle çalışmaların devam etmesi planlanmaktadır.

![dyos](https://user-images.githubusercontent.com/102908626/215262280-5a64398f-966f-4bf0-89e7-e9be36435f64.gif)


