# HTTP: настройка для взаимодействия с сервером

:date: 03.11.2022

Прежде чем использовать `HttpClient`, необходимо импортировать модуль Angular `HttpClientModule`. Большинство приложений делают это в корневом `AppModule`.

```ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
    imports: [
        BrowserModule,
        // import HttpClientModule after BrowserModule.
        HttpClientModule,
    ],
    declarations: [AppComponent],
    bootstrap: [AppComponent],
})
export class AppModule {}
```

Затем вы можете внедрить сервис `HttpClient` в качестве зависимости класса приложения, как показано в следующем примере `ConfigService`.

```ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class ConfigService {
    constructor(private http: HttpClient) {}
}
```

Сервис `HttpClient` использует [observables](glossary.md#observable 'Observable definition') для всех транзакций. Вы должны импортировать RxJS observable и символы операторов, которые появляются в фрагментах примера.

Эти импорты `ConfigService` являются типичными.

```ts
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
```

!!!note ""

    Вы можете запустить [пример](https://angular.io/generated/live-examples/http-setup-server-communication/stackblitz.html), который сопровождает данное руководство.

    Пример приложения не требует сервера данных. Он полагается на [Angular _in-memory-web-api_](https://github.com/angular/angular/tree/main/packages/misc/angular-in-memory-web-api), который заменяет `HttpBackend` модуля _HttpClient_.

    Заменяющий сервис имитирует поведение REST-подобного бэкенда.

    Посмотрите на `AppModule` _imports_, чтобы увидеть, как он настроен.
