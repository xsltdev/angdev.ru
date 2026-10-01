# Установите локаль времени выполнения вручную

:date: 28.02.2022

Начальная установка Angular уже содержит данные локали для английского языка в Соединенных Штатах (`en-US`). [Angular CLI][aioclimain] автоматически включает данные локали и устанавливает значение `LOCALE_ID`, когда вы используете опцию `--localize` в команде [`ng build`][aioclibuild].

Чтобы вручную установить локаль времени выполнения приложения, отличную от автоматического значения, выполните следующие действия.

1.  Найдите идентификатор локали Unicode в комбинации "язык-локаль" в каталоге [`@angular/common/locales/`][unpkgbrowseangularcommonlocales].

2.  Установите маркер [`LOCALE_ID`][aioapicorelocaleid].

В следующем примере значение `LOCALE_ID` установлено на `fr` для французского языка.

```ts
import { LOCALE_ID, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from '../src/app/app.component';

@NgModule({
    imports: [BrowserModule],
    declarations: [AppComponent],
    providers: [{ provide: LOCALE_ID, useValue: 'fr' }],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

<!-- links -->

[aioapicorelocaleid]: https://angular.io/api/core/LOCALE_ID
[aioclimain]: https://angular.io/cli
[aioclibuild]: https://angular.io/cli/build

<!-- external links -->

[unpkgbrowseangularcommonlocales]: https://unpkg.com/browse/@angular/common/locales/

<!-- end links -->
