Program nasil calisir?

Program hicbir parametre almadan run edilebilir.
server.py disinda baska dosya bulunmamaktadir.

En dista if elif bloklari ile gelen request'in type'i anlasilir (or. POST, GET) Bu if'lerin sonunda bir else bulunur, 404 doner.
Bu if else'lerin ic kisminda birden fazla endpoint varsa bir request type icin, (or. GET) bunlar ayiklanir.
Cogu ozellik odev metninde istendigi gibi calismaktadir, birkac corner case mevcut olabilir.
Bazi requestlerde istenen gorev yapilmasina karsin 404 mesaji body'ye gonderilmektedir, nedenini anlayamadim. Fakat Postman uzerinden
kontrol edildigi takdirde, Status: 200 OK seklinde istenen response dogru sekilde donulmektedir.
Kodun uzunlugu response donerken JSON formatinda donmek icin dictionary olusturup donmemden kaynaklidir. Bir metot olusturup oradan cagiramadim, kusura bakmayin, zamanim dardi.
Odev metninden anlayamadigim ve varsaydigim tek nokta, upload ve download yaparken, parametre olarak fileName=safa.txt verildigidir. Eger bu requestlerde parametre vermezseniz 
download ve upload yapmamaktadir. Bu parametrenin dogru olup olmadiginin kontrolu ise bu iki endpoint icin eksiktir. Ancak parametre gosterdigim gibi verildigi takdirde dogru calismaktadir. Arada postman uzerinden gonderilen request'lere cevap gelmezse, server'i yeniden baslatmaniz yeterlidir.

Kodumla ilgili ufak hatalar ve varsayimlarim bu kadardir, umarim begenirsiniz.