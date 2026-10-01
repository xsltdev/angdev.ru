# Взаимодействие с Service Worker

:date: 28.02.2022

Импорт `ServiceWorkerModule` в ваш `AppModule` не просто регистрирует Service Worker, он также предоставляет несколько сервисов, которые вы можете использовать для взаимодействия с сервисным работником и управления кэшированием вашего приложения.

## Предварительные условия

Базовое понимание следующего:

-   [Начало работы с Service Workers](service-worker-getting-started.md)

## Служба `SwUpdate`

Служба `SwUpdate` предоставляет вам доступ к событиям, которые указывают, когда работник службы обнаруживает и устанавливает доступное обновление для вашего приложения.

Служба `SwUpdate` поддерживает три отдельные операции:

-   Получить уведомление, когда обновленная версия _обнаружена_ на сервере, _установлена и готова_ к локальному использованию или когда _установка не удалась_.
-   Попросить работника службы проверить сервер на наличие новых обновлений
-   Попросите работника службы активировать последнюю версию приложения для текущей вкладки

### Обновления версий

`versionUpdates` является `Observable` свойством `SwUpdate` и испускает четыре типа событий:

| Типы событий                     | Подробности                                                                                                                                                                                                      |
| :------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `VersionDetectedEvent`           | Вызывается, когда Service Worker обнаружил новую версию приложения на сервере и собирается начать ее загрузку.                                                                                                   |
| `NoNewVersionDetectedEvent`      | Выдается, когда работник службы проверил версию приложения на сервере и не обнаружил новой версии.                                                                                                               |
| `VersionReadyEvent`              | Вызывается, когда новая версия приложения доступна для активации клиентами. Оно может быть использовано для уведомления пользователя о доступном обновлении или для того, чтобы попросить его обновить страницу. |
| `VersionInstallationFailedEvent` | Вызывается, когда установка новой версии не удалась. Может использоваться для регистрации/мониторинга.                                                                                                           |

```ts
@Injectable()
export class LogUpdateService {
    constructor(updates: SwUpdate) {
        updates.versionUpdates.subscribe((evt) => {
            switch (evt.type) {
                case 'VERSION_DETECTED':
                    console.log(
                        `Downloading new app version: ${evt.version.hash}`
                    );
                    break;
                case 'VERSION_READY':
                    console.log(
                        `Current app version: ${evt.currentVersion.hash}`
                    );
                    console.log(
                        `New app version ready for use: ${evt.latestVersion.hash}`
                    );
                    break;
                case 'VERSION_INSTALLATION_FAILED':
                    console.log(
                        `Failed to install app version '${evt.version.hash}': ${evt.error}`
                    );
                    break;
            }
        });
    }
}
```

### Проверка наличия обновлений

Можно попросить работника службы проверить, были ли развернуты обновления на сервере. Работник службы проверяет наличие обновлений во время инициализации и при каждом навигационном запросе &mdash; то есть, когда пользователь переходит с другого адреса на ваше приложение.

Однако вы можете вручную проверять наличие обновлений, если у вас сайт, который часто меняется, или если вы хотите, чтобы обновления происходили по расписанию.

Это можно сделать с помощью метода `checkForUpdate()`:

```ts
import { ApplicationRef, Injectable } from '@angular/core';
import { SwUpdate } from '@angular/service-worker';
import { concat, interval } from 'rxjs';
import { first } from 'rxjs/operators';

@Injectable()
export class CheckForUpdateService {
    constructor(appRef: ApplicationRef, updates: SwUpdate) {
        // Allow the app to stabilize first, before starting
        // polling for updates with `interval()`.
        const appIsStable$ = appRef.isStable.pipe(
            first((isStable) => isStable === true)
        );
        const everySixHours$ = interval(6 * 60 * 60 * 1000);
        const everySixHoursOnceAppIsStable$ = concat(
            appIsStable$,
            everySixHours$
        );

        everySixHoursOnceAppIsStable$.subscribe(
            async () => {
                try {
                    const updateFound = await updates.checkForUpdate();
                    console.log(
                        updateFound
                            ? 'A new version is available.'
                            : 'Already on the latest version.'
                    );
                } catch (err) {
                    console.error(
                        'Failed to check for updates:',
                        err
                    );
                }
            }
        );
    }
}
```

Этот метод возвращает `Promise<boolean>`, который указывает, доступно ли обновление для активации. Проверка может закончиться неудачей, что приведет к отказу от `Promise`.

!!!warning ""

    Чтобы избежать негативного влияния на начальный рендеринг страницы, `ServiceWorkerModule` по умолчанию ждет до 30 секунд, пока приложение стабилизируется, прежде чем зарегистрировать скрипт ServiceWorker. Постоянный опрос обновлений, например, с помощью [setInterval()](https://developer.mozilla.org/docs/Web/API/WindowOrWorkerGlobalScope/setInterval) или [interval()](https://rxjs.dev/api/index/function/interval) RxJS, не позволяет приложению стабилизироваться, и скрипт ServiceWorker не регистрируется в браузере до достижения верхнего предела в 30 секунд.

    Это справедливо для любого вида опроса, выполняемого вашим приложением.
    Для получения дополнительной информации ознакомьтесь с документацией [isStable](https://angular.io/api/core/ApplicationRef#isStable).

    Чтобы избежать этой задержки, сначала дождитесь стабилизации приложения, прежде чем начать опрашивать обновления, как показано в предыдущем примере. В качестве альтернативы вы можете определить другую [стратегию регистрации](https://angular.io/api/service-worker/SwRegistrationOptions#registrationStrategy) для ServiceWorker.

### Обновление до последней версии

Вы можете обновить существующую вкладку до последней версии, перезагрузив страницу, как только будет готова новая версия. Чтобы не прерывать работу пользователя, как правило, целесообразно запросить у него подтверждение, что он согласен перезагрузить страницу и обновить ее до последней версии:

```ts
@Injectable()
export class PromptUpdateService {
    constructor(swUpdate: SwUpdate) {
        swUpdate.versionUpdates
            .pipe(
                filter(
                    (evt): evt is VersionReadyEvent =>
                        evt.type === 'VERSION_READY'
                )
            )
            .subscribe((evt) => {
                if (promptUser(evt)) {
                    // Reload the page to update to the latest version.
                    document.location.reload();
                }
            });
    }
}
```

!!!warning ""

    Вызов [SwUpdate#activateUpdate](https://angular.io/api/service-worker/SwUpdate#activateUpdate) обновляет вкладку до последней версии без перезагрузки страницы, но это может нарушить работу приложения.

    Обновление без перезагрузки может создать несоответствие версий между [оболочкой приложения](glossary.md#app-shell) и другими ресурсами страницы, такими как [куски с ленивой загрузкой](glossary.md#lazy-loading), имена файлов которых могут меняться между версиями.

    Вы должны использовать `activateUpdate()`, только если вы уверены, что это безопасно для вашего конкретного случая использования.

### Обработка невосстановимого состояния

В некоторых случаях версия приложения, используемая сервисным работником для обслуживания клиента, может находиться в поврежденном состоянии, которое невозможно восстановить без полной перезагрузки страницы.

Например, представьте следующий сценарий:

-   Пользователь открывает приложение в первый раз, и работник службы кэширует последнюю версию приложения.

    Предположим, что кэшированные активы приложения включают `index.html`, `main.<main-hash-1>.js` и `lazy-chunk.<lazy-hash-1>.js`.

-   Пользователь закрывает приложение и не открывает его некоторое время.

-   Через некоторое время новая версия приложения развертывается на сервере.

    Эта новая версия включает файлы `index.html`, `main.<main-hash-2>.js` и `lazy-chunk.<lazy-hash-2>.js`.

    !!!note ""

        Хеши теперь другие, потому что содержимое файлов изменилось.

    Старая версия больше не доступна на сервере.

-   Тем временем, браузер пользователя решил удалить `lazy-chunk.<lazy-hash-1>.js` из своего кэша.

    Браузеры могут решить удалить определенные (или все) ресурсы из кэша, чтобы освободить место на диске.

-   Пользователь снова открывает приложение.

    Рабочий сервис обслуживает последнюю версию, известную ему на данный момент, а именно старую версию (`index.html` и `main.<main-hash-1>.js`).

-   Позже приложение запрашивает ленивый пакет, `lazy-chunk.<lazy-hash-1>.js`.

-   Service Worker не может найти актив в кэше (помните, что браузер изгнал его).

    Он также не может получить его с сервера (потому что на сервере теперь есть только `lazy-chunk.<lazy-hash-2>.js` из более новой версии).

В предыдущем сценарии работник службы не может обслужить актив, который обычно кэшируется. Эта конкретная версия приложения сломана, и нет способа исправить состояние клиента без перезагрузки страницы.
В таких случаях работник службы уведомляет клиента, отправляя событие `UnrecoverableStateEvent`.

Подпишитесь на `SwUpdate#unrecoverable`, чтобы получать уведомления и обрабатывать эти ошибки.

```ts
@Injectable()
export class HandleUnrecoverableStateService {
    constructor(updates: SwUpdate) {
        updates.unrecoverable.subscribe((event) => {
            notifyUser(
                'An error occurred that we cannot recover from:\n' +
                    event.reason +
                    '\n\nPlease reload the page.'
            );
        });
    }
}
```

## Больше о рабочих службах Angular

Вас также может заинтересовать следующее:

-   [Service Worker уведомления](service-worker-notifications.md)

<!-- links -->

<!-- external links -->

<!-- end links -->
