# Closed test — operator and tester guide (draft)

Version is shown in the parents area from the same `project.godot` values used
by both Android presets. Operator must first fill {{TEST_LINK}},
{{FEEDBACK_KANAL}}, {{HERAUSGEBER}} and {{SUPPORT_EMAIL}}, and approve the
privacy notice/rights. No invitation, Play upload or test-duration requirement
has been completed by this document. Verify current account-specific Play rules.
Use the **neutral** upload-signed AAB for Play. Family debug APKs stay private.

## Deutsch

Mit dem vorgesehenen Testkonto {{TEST_LINK}} öffnen, dem Test zustimmen und über
Google Play installieren. Den angebotenen Versionsstand im Elternbereich prüfen.
Die Einladung und Zugriffsrechte richtet der Betreiber ein. Für Tests etwa zehn
bis fünfzehn Minuten einplanen; Hilfe Erwachsener und Pausen sind freiwillig.

1. Offline starten: kein Login und keine Berechtigungsabfrage.
2. Sprache wählen; Beschriftungen und Aufgaben passen zu DE/EN/RU.
3. Figur, Kleidung und eine Kulisse pro Fach wählen.
4. Mathe-, Sprach- und Sachrätsel lösen; Hilfe und falsche Antwort ausprobieren.
5. Beide freiwilligen Boni öffnen oder ohne Strafe überspringen.
6. Gesamtpunkte verdienen; App vollständig schließen/neustarten: Punkte bleiben.
7. Hoch-/Querformat, große Schrift und kleines Display: nichts verdeckt Antworten.
8. Stimme bis zum Ende hören; Musik und Lautstärke ändern; keine abgeschnittenen Wörter.
9. Während Sprache Home/Appwechsel/Sperren, dann zurück: kein unerwünschter Hintergrundton.
10. **Eigenes Figurenbild:** nur Erwachsene wählen über das System ein synthetisches JPEG/PNG/WebP, drehen/zoomen/verschieben und bestätigen. Keine neue Berechtigung zulassen; bei Abfrage abbrechen und melden. Abbrechen erhält das vorige Bild und Punkte.
11. Figur im Spiel ansehen; im Elternbereich entfernen und Zurücksetzen mit Rückfrage prüfen. Nur synthetische Bilder nutzen. Die App-Kopie verschwindet; das Geräteoriginal bleibt.
12. Update über denselben Play-Testkanal: Punkte/Einstellungen bleiben. Nicht deinstallieren, um einen Updatefehler zu umgehen.

Fehler an {{FEEDBACK_KANAL}}: Version/Code, Sprache, Androidversion und grobe
Geräteklasse, kurze Schritte, erwartetes/tatsächliches Ergebnis. Keine Namen von
Kindern, Konten, Seriennummern, Spielstände oder Fotos schicken. **Keine Screenshots
mit Kinderfotos** oder anderen echten Personen. Bekannte Grenzen: siehe unten.

## English

Open {{TEST_LINK}} with the invited test account, opt in and install through
Google Play. Check the version in the parents area. The operator configures
invitations/access. Allow about ten to fifteen minutes; adult help and breaks
are voluntary.

1. Start offline: no login or permission prompt.
2. Choose language; UI and language-learning tasks match DE/EN/RU.
3. Select character, clothes and scenery per subject.
4. Try maths, language and science, including Help and a wrong answer.
5. Open both optional bonuses or skip without penalty.
6. Earn points; fully close/restart: the total remains.
7. Rotate, enlarge text and use a small display: answers stay reachable.
8. Listen to complete speech; adjust music/volume; report cut-off words.
9. Switch apps/lock during speech, then return: no unwanted background sound.
10. **Own image:** adults select a synthetic JPEG/PNG/WebP with the system picker, adjust orientation/pan/zoom and confirm. Never grant a new permission: cancel/report a prompt. Cancelling preserves the old picture/points.
11. View it in play; remove in parents and test confirmed reset using synthetic data. The app copy disappears; the device original remains.
12. Update within the same Play test channel: points/settings remain. Do not uninstall to work around an update failure.

Report to {{FEEDBACK_KANAL}}: version/code, language, Android version, broad device
class, short reproduction, expected/actual result. No children's names, accounts,
serials, saves or photos. **Never send screenshots containing child photos** or
other real people. Known boundaries are listed below.

## Русский

Откройте {{TEST_LINK}} с приглашённой тестовой учётной записью, подтвердите участие
и установите приложение через магазин. Проверьте версию в разделе для взрослых.
Приглашения и доступ настраивает оператор. Достаточно десяти–пятнадцати минут;
помощь взрослых и перерывы добровольны.

1. Запустите без сети: нет входа в учётную запись или запроса разрешений.
2. Выберите язык: интерфейс и языковые задания соответствуют выбору.
3. Выберите персонажа, одежду и декорации для каждого предмета.
4. Решите задачи по математике, языку и окружающему миру; попробуйте помощь и неверный ответ.
5. Откройте оба бонуса или пропустите их без наказания.
6. Заработайте очки и полностью перезапустите приложение: сумма сохраняется.
7. Поверните экран, увеличьте шрифт; ответы доступны на небольшом экране.
8. Дослушайте речь, измените музыку и громкость; сообщите об обрезанных словах.
9. Во время речи переключите приложение или заблокируйте экран: нет лишнего звука в фоне.
10. **Свой персонаж:** взрослый выбирает синтетическое изображение через системное окно, меняет положение и масштаб, подтверждает. Не выдавайте новых разрешений: отмените запрос и сообщите. Отмена сохраняет старое изображение и очки.
11. Посмотрите персонажа в игре; удалите его в разделе для взрослых и проверьте сброс с подтверждением. Используйте только синтетические данные. Копия исчезает, оригинал на устройстве не меняется.
12. Обновите через тот же тестовый канал: очки и настройки остаются. Не удаляйте приложение для обхода ошибки обновления.

Сообщайте через {{FEEDBACK_KANAL}}: версию и код сборки, язык, версию Андроид,
общий класс устройства, шаги, ожидаемый и фактический результат. Не отправляйте
имена детей, учётные записи, серийные номера, сохранения или фотографии.
**Нельзя присылать снимки экрана с фотографиями детей** и других реальных людей.

## Shared acceptance boundaries

[Known issues](known-issues.md) distinguishes issue-tracker bugs from unexecuted
checks. Full [acceptance](../ACCEPTANCE.md) additionally requires Android 13+ and
10–12 system selection/update/backup checks, native-language listening and an
independent content review. Desktop tests do not replace them. Points/engagement
are not empirical learning outcomes. No telemetry, feedback upload or reporting
button is added; voluntary reports go to the operator's chosen external channel.
