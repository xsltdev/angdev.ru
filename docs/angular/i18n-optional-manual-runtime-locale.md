# Установите локаль времени выполнения вручную

<!--todo: The Angular CLI sets the locale ID token as part of the translation. -->

<!--todo: To override the provider for the locale ID token. -->

Начальная установка Angular уже содержит данные локали для английского языка в Соединенных Штатах \(`en-US`\). Angular CLI][aioclimain] автоматически включает данные локали и устанавливает значение `LOCALE_ID`, когда вы используете опцию `--localize` в команде [`ng build`][aioclibuild].

Чтобы вручную установить локаль времени выполнения приложения, отличную от автоматического значения, выполните следующие действия.

1.  Найдите идентификатор локали Unicode в комбинации "язык-локаль" в каталоге [`@angular/common/locales/`][unpkgbrowseangularcommonlocales].

1.  Установите маркер [`LOCALE_ID`][aioapicorelocaleid].

В следующем примере значение `LOCALE_ID` установлено на `fr` для французского языка.

<code-example header="src/app/app.module.ts" path="i18n/doc-files/app.module.ts" region="locale-id"></code-example>

<!-- links -->

[aioapicorelocaleid]: api/core/LOCALE_ID 'LOCALE_ID | Core - API | Angular'
[aioclimain]: cli 'CLI Overview and Command Reference | Angular'
[aioclibuild]: cli/build 'ng build | CLI | Angular'

<!-- external links -->

[unpkgbrowseangularcommonlocales]: https://unpkg.com/browse/@angular/common/locales/ '@angular/common/locales/ | Unpkg'

<!-- end links -->

:date: 28.02.2022
