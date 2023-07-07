# Импорт глобальных вариантов данных локали

:date: 28.02.2022

[Angular CLI][aioclimain] автоматически включает данные о локали, если вы выполняете команду [`ng build`][aioclibuild] с опцией `--localize`.

<!--todo: replace with code-example -->

```shell
ng build --localize
```

Пакет `@angular/common` на npm содержит файлы данных локали. Глобальные варианты данных локали доступны в [`@angular/common/locales/global`][unpkgbrowseangularcommonlocalesglobal].

## Пример `импорта` для французского языка

Следующий пример импортирует глобальные варианты для французского языка (`fr`).

```ts
import '@angular/common/locales/global/fr';
```

<!-- links -->

[aioclimain]: https://angular.io/cli
[aioclibuild]: https://angular.io/cli/build

<!-- external links -->

[unpkgbrowseangularcommonlocalesglobal]: https://unpkg.com/browse/@angular/common/locales/global

<!-- end links -->
