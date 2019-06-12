Architektura Aplikacji Chmurowych - Projekt Końcowy - Dokumentacja
========================

Funkcjonalność aplikacji
========================

-   Strona internetowa klasyfikująca obrazki wgrywane przez
    użytkowników.

-   Po wgraniu obrazku, użytkownik dostaje informację do 10 najbardziej
    prawdopodobnych etykiet opisujących obrazek.

-   Wyświetlane jest 20 ostatnio klasyfikowanych obrazków.

-   Wyświetlany jest ranking 10 najczęściej przewidywanych klas.

Informacja o predykcjach przechowywana jest w DynamoDB (z linkami do
obrazków w S3 i datą wrzucenia obrazka) w celu ewentualnej późniejszej
analizy *trendów*.

Korzystanie z aplikacji
=======================

Strona dostępna jest pod adresem:
<http://chmury.website.pl.s3-website-us-east-1.amazonaws.com/>. Reszta
jest samowyjaśniająca się :)

Architektura
============

![Architektura
aplikacji.](final_architecture.png)

Strona statyczna internetowa
----------------------------

Aplikacja jest dostępna przez przeglądarkę. Strona została napisana z wykorzystaniem
*vue.js* i hostowaną na *S3*. Jej wysoka dostępność jest zapewniana
przez usługę *CloudFront*.

Po wejściu użytkownika na stronę generowana jest jej zawartość. Linki
obrazków do galerii otrzymywane są poprzez wykonanie zapytania RESTowego,
przez *API Gateway*, które wywołuję funkcję *AWS Lambda*
pageDataFunction. Funkcja zwraca linki do maksymalnie 20 ostatnio
wgranych obrazków oraz informację o najczęściej klasyfikowanych
obiektach.

Po wybraniu obrazka i kliknięciu przycisku classify wykonywane jest
zapytanie RESTowe, przez *API Gateway* i wywoływana jest funkcja *Lambda*
classifyImage. Funkcja zwraca do 10 etykiet opisujących co jest na obrazku
wraz z pewnością ich znalezienia.

*Lambda* pageDataFunction
-------------------------

Funkcja ta:

-   Zwraca 10 najczęściej przewidywanych etykiet.

-   Zwraca linki do S3 do 20 ostatnio dodanych obrazków.

*Lambda* classifyImage
----------------------

Funkcja ta przyjmuje obrazek, w formacie base64, który na którym mają
zostać rozpoznane obiekty. a następnie:

-   Dodaje obrazek do bucketa *S3*

-   Dokonuje predykcji obiektów na obrazku wykorzystując funkcję
    getLabels z *Amazon Rekognition*

-   Dodaje wyniki predykcji oraz linki do obrazków do bazy danych
    *DynamoDB*.

-   Zwraca etykiety obiektów z pewnościami w formacie JSON.

*Lambda* dailyReport
--------------------

Funkcja ta generuje raport z klasyfikacji z poprzedniego dnia,
wywoływana jest przez Event *WatchCloud*. Dzięki temu mechanizmowi, gdy
użytkownik wchodzi na stronę, nie trzeba zliczać wszystkich elementów w
bazie w celu wyznaczenia statystyk, a jedynie z ostatniego dnia. 
Funkcja aktualizuje tabelę *StatisticsData* w *DynamoDB*.
Następnie wysyła raport do administratora poprzez e-mail i SMS, dzięki usłudze
*SNS*.

Niestety ze względu na ograniczenia konta, brak możliwości zrobienia
eventu *WatchCloudowego*, ta funkcjonalność nie została w pełni
zrealizowana.

Baza *DynamoDB*
---------------

Aplikacja wykorzystuje do działania dwie tabele. Jedna z nich
przechowuje informacje o obrazkach, a druga dane statystyczne.

### ClassifiedImages

Przechowuje:

-   date (String) -- Primary partition key;

-   time (String) -- Primary sort key;

-   bucketName (String);

-   createdOn (String);

-   imgLocation (String)

-   labels (List(Map)).

### StatisticsData

Przechowuje:

-   set\_name (String) -- Primary partition key;

-   labels (List(Map));

-   last\_sync (String).

Usprawnienia
============

Continuous delivery
-------------------

Mimo braku uprawnień do realizacji continuous delivery, udało się
zrealizować tą funkcjonalność przy pomocy aws-cli. Skrypty `publish.bat`
(generyczny skrypt przyjmujący nazwę funkcji lambda oraz nazwę
hendlara), `publish_all.bat` (skrypt aktualizujący wszystkie funkcje
lambda) oraz trzy skrypty opakowujące skrypt `publish.bat` pod kątem
aktualizacji konkretnej funkcji po edycji na dysku. Pozwalają one
również na wykorzystanie mechanizmów kontroli wersji do kontroli kodu.

Kontrola wersji
---------------

W celu łatwiejszego zarządzania kodem strony oraz funkcji *Lambda*,
zostały one umieszczone na GitHubie
[AWS\_FinalProject](https://github.com/bi3niol/AWS_FinalProject).

Wykorzystane usługi Amazon AWS
==============================

1.  S3

2.  Cloudfront

3.  Lambda

4.  API Gateway

5.  Rekognition

6.  DynamoDB

7.  aws-cli

8.  SNS

9.  ~~WatchCloud~~ - niestety nie mamy uprawnień do zrobienia Eventu

Autorzy
==================
[Piotr Pasza Storożenko](https://github.com/pstorozenko/) & [Mateusz Bieńkowski](https://github.com/bi3niol/)
