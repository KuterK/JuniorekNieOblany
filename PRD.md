PRD – JuniorekNieOblany
1. Opis produktu
Nazwa robocza
JuniorekNieOblany
Cel produktu
JuniorekNieOblany to aplikacja webowa wspierająca naukę programowania poprzez analizę fragmentów kodu z wykorzystaniem modeli językowych (LLM).
Aplikacja umożliwia użytkownikowi wklejenie fragmentu kodu, który następnie zostaje przeanalizowany przez AI. W odpowiedzi użytkownik otrzymuje uporządkowane wyjaśnienie obejmujące działanie kodu, wykorzystane koncepcje programistyczne, potencjalne błędy oraz wskazówki edukacyjne. Każda analiza zostaje zapisana w prywatnej bibliotece użytkownika, dzięki czemu może on wracać do niej w dowolnym momencie.
Celem produktu jest skrócenie czasu potrzebnego na zrozumienie nowych zagadnień programistycznych oraz stworzenie osobistej bazy wiedzy opartej na rzeczywistych przykładach kodu.
________________________________________
2. Problem użytkownika
Junior Developerzy oraz studenci regularnie spotykają fragmenty kodu pochodzące z:
•	materiałów szkoleniowych,
•	zajęć akademickich,
•	code review,
•	dokumentacji,
•	GitHuba,
•	Stack Overflow.
Największym problemem nie jest znalezienie przykładu kodu, lecz jego zrozumienie.
Użytkownicy często nie wiedzą:
•	dlaczego kod działa,
•	jakie wzorce projektowe wykorzystuje,
•	jakie koncepcje języka prezentuje,
•	jakie są jego mocne i słabe strony,
•	kiedy należy stosować podobne rozwiązania.
Proces nauki wymaga przełączania się pomiędzy wieloma źródłami wiedzy, co wydłuża naukę i utrudnia organizację zdobytych informacji.
JuniorekNieOblany eliminuje ten problem poprzez dostarczenie kompletnego wyjaśnienia wygenerowanego przez AI oraz zapisanie go w osobistej bibliotece użytkownika.
________________________________________
3. Cele produktu
Cel biznesowy
Stworzenie prostego narzędzia edukacyjnego wykorzystującego AI do analizy kodu oraz budowania własnej bazy wiedzy.
Cele użytkownika
•	szybkie zrozumienie fragmentów kodu,
•	nauka nowych koncepcji programistycznych,
•	możliwość powrotu do wcześniej przeanalizowanych przykładów,
•	uporządkowanie własnych materiałów edukacyjnych.
________________________________________
4. Zakres MVP
4.1 Autoryzacja
System umożliwia:
•	rejestrację użytkownika,
•	logowanie,
•	wylogowanie.
Każdy użytkownik posiada własną bibliotekę analiz.
________________________________________
4.2 Dodawanie kodu
Użytkownik może:
•	wkleić fragment kodu (maksymalnie 100 linii),
•	uruchomić analizę AI.
Kod jest jedynym polem wprowadzanym ręcznie.
________________________________________
4.3 Automatyczna analiza AI
Po rozpoczęciu analizy AI automatycznie:
•	rozpoznaje język programowania,
•	generuje tytuł,
•	tworzy krótki opis,
•	generuje tagi,
•	analizuje kod.
Analiza posiada stałą strukturę:
1.	Krótkie podsumowanie.
2.	Opis działania kodu.
3.	Wykorzystane wzorce projektowe lub koncepcje.
4.	Potencjalne błędy i pułapki.
5.	Wyjaśnienie przeznaczone dla junior developera.
________________________________________
4.4 Zarządzanie analizami
Użytkownik może:
•	przeglądać wszystkie analizy,
•	otworzyć szczegóły analizy,
•	usunąć analizę,
•	ponownie wygenerować analizę,
•	edytować wygenerowany tytuł.
________________________________________
4.5 Ocena jakości AI
Po przeczytaniu analizy użytkownik może oznaczyć ją jako:
•	👍 pomocna,
•	👎 niepomocna.
Ocena zostaje zapisana i może zostać wykorzystana do analizy jakości odpowiedzi AI.
________________________________________
4.6 Wyszukiwanie
Użytkownik może wyszukiwać analizy po:
•	tytule,
•	języku programowania,
•	tagach.
________________________________________
5. Zakres poza MVP
Do pierwszej wersji produktu nie należą:
•	czat z AI,
•	generowanie kodu,
•	poprawianie kodu,
•	współdzielenie analiz,
•	komentarze,
•	GitHub Gists,
•	import plików,
•	RAG,
•	fine-tuning modeli,
•	historia wersji,
•	publiczne profile,
•	aplikacja mobilna,
•	obsługa wielu modeli LLM,
•	quizy,
•	kursy programowania,
•	wyszukiwanie semantyczne.
________________________________________
6. User Stories
US-01 Dodanie kodu
Jako junior developer
Chcę wkleić fragment kodu
Aby otrzymać jego wyjaśnienie.
________________________________________
US-02 Automatyczna analiza
Jako użytkownik
Chcę jednym kliknięciem wygenerować analizę AI
Aby zrozumieć działanie kodu.
________________________________________
US-03 Przegląd biblioteki
Jako użytkownik
Chcę mieć dostęp do wszystkich wcześniejszych analiz
Aby móc do nich wracać podczas nauki.
________________________________________
US-04 Ponowna analiza
Jako użytkownik
Chcę ponownie wygenerować analizę
Aby otrzymać aktualne lub lepsze wyjaśnienie.
________________________________________
US-05 Zarządzanie analizami
Jako użytkownik
Chcę usuwać oraz zmieniać tytuły analiz
Aby utrzymywać uporządkowaną bibliotekę.
________________________________________
US-06 Ocena AI
Jako użytkownik
Chcę oznaczyć analizę jako pomocną lub niepomocną
Aby ocenić jakość odpowiedzi generowanych przez AI.
________________________________________
7. Scenariusze użytkownika
Analiza nowego kodu
1.	Użytkownik loguje się.
2.	Wkleja kod.
3.	Klika Analyze.
4.	AI generuje analizę.
5.	Analiza zostaje zapisana.
6.	Użytkownik czyta wynik.
7.	Użytkownik ocenia odpowiedź.
________________________________________
Powrót do analizy
1.	Użytkownik otwiera bibliotekę.
2.	Wyszukuje analizę.
3.	Otwiera szczegóły.
4.	Korzysta z zapisanej wiedzy.
________________________________________
Ponowne wygenerowanie
1.	Użytkownik otwiera analizę.
2.	Klika Regenerate.
3.	AI tworzy nową analizę.
4.	Nowa analiza zastępuje poprzednią.
________________________________________
8. Wymagania niefunkcjonalne
•	aplikacja działa jako aplikacja webowa,
•	analiza trwa nie dłużej niż 15 sekund,
•	obsługiwane są popularne języki programowania,
•	maksymalna długość kodu wynosi 100 linii,
•	dane każdego użytkownika są od siebie odseparowane,
•	w przypadku błędu AI użytkownik otrzymuje czytelny komunikat z możliwością ponowienia próby.
________________________________________
9. Metryki sukcesu
Funkcjonalne
•	użytkownik może utworzyć konto,
•	użytkownik może dodać snippet,
•	użytkownik może wygenerować analizę AI,
•	analiza zostaje zapisana,
•	użytkownik może ją ponownie wygenerować,
•	użytkownik może ją usunąć,
•	użytkownik może ją ocenić.
Produktowe
•	minimum 90% wygenerowanych analiz zostaje zapisanych przez użytkowników,
•	minimum 80% ocen analiz stanowią pozytywne oceny (👍),
•	średni czas wygenerowania analizy nie przekracza 15 sekund,
•	użytkownik odnajduje wcześniejszą analizę w czasie krótszym niż 30 sekund,
•	co najmniej 80% użytkowników generuje więcej niż jedną analizę podczas jednej sesji.
________________________________________
10. Przyszły rozwój produktu
Po ukończeniu MVP planowana jest możliwość rozbudowy o:
•	wyszukiwanie semantyczne (RAG),
•	import z GitHub Gists,
•	historię analiz,
•	obsługę wielu modeli AI,
•	generowanie testów jednostkowych,
•	generowanie diagramów,
•	generowanie przykładów podobnego kodu,
•	udostępnianie analiz innym użytkownikom,
•	quizy sprawdzające zrozumienie analizowanego kodu.
