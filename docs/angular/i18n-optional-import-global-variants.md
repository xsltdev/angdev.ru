# Импорт глобальных вариантов данных локали

[Angular CLI][aioclimain] автоматически включает данные о локали, если вы выполняете команду [`ng build`][aioclibuild] с опцией `--localize`.

<!--todo: replace with code-example -->

<code-example format="shell" language="shell">

ng build --localize

</code-example>

Пакет `@angular/common` на npm содержит файлы данных локали. Глобальные варианты данных локали доступны в [`@angular/common/locales/global`][unpkgbrowseangularcommonlocalesglobal].

## Пример `импорта` для французского языка

Следующий пример импортирует глобальные варианты для французского языка \(`fr`\).

<code-example header="src/app/app.module.ts" path="i18n/doc-files/app.module.ts" region="global-locale"></code-example>

<!-- links -->

[aioclimain]: cli 'CLI Overview and Command Reference | Angular'
[aioclibuild]: cli/build 'ng build | CLI | Angular'

<!-- external links -->

[unpkgbrowseangularcommonlocalesglobal]: https://unpkg.com/browse/@angular/common/locales/global '@angular/common/locales/global | Unpkg'

<!-- end links -->

:date: 28.02.2022
