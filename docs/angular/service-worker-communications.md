# Взаимодействие с сервисным работником

Импорт `ServiceWorkerModule` в ваш `AppModule` не просто регистрирует сервисный работник, он также предоставляет несколько сервисов, которые вы можете использовать для взаимодействия с сервисным работником и управления кэшированием вашего приложения.

## Предварительные условия

Базовое понимание следующего:

-   [Getting Started with Service Workers](guide/service-worker-getting-started)

## Служба `SwUpdate`.

Служба `SwUpdate` предоставляет вам доступ к событиям, которые указывают, когда работник службы обнаруживает и устанавливает доступное обновление для вашего приложения.

Служба `SwUpdate` поддерживает три отдельные операции:

-   Получить уведомление, когда обновленная версия _обнаружена_ на сервере, _установлена и готова_ к локальному использованию или когда _установка не удалась_.

-   Попросить работника службы проверить сервер на наличие новых обновлений

-   Попросите работника службы активировать последнюю версию приложения для текущей вкладки

### Обновления версий

`versionUpdates` является `Observable` свойством `SwUpdate` и испускает четыре типа событий:

| Типы событий | Подробности | | :------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | |
| `VersionDetectedEvent` | Вызывается, когда сервисный работник обнаружил новую версию приложения на сервере и собирается начать ее загрузку. |

| `NoNewVersionDetectedEvent` | Выдается, когда работник службы проверил версию приложения на сервере и не обнаружил новой версии. |

| | `VersionReadyEvent` | Вызывается, когда новая версия приложения доступна для активации клиентами. Оно может быть использовано для уведомления пользователя о доступном обновлении или для того, чтобы попросить его обновить страницу. |

| `VersionInstallationFailedEvent` | Вызывается, когда установка новой версии не удалась. Может использоваться для регистрации/мониторинга. |

<code-example header="log-update.service.ts" path="service-worker-getting-started/src/app/log-update.service.ts" region="sw-update"></code-example>.

### Проверка наличия обновлений

Можно попросить работника службы проверить, были ли развернуты обновления на сервере. Работник службы проверяет наличие обновлений во время инициализации и при каждом навигационном запросе &mdash; то есть, когда пользователь переходит с другого адреса на ваше приложение.

Однако вы можете вручную проверять наличие обновлений, если у вас сайт, который часто меняется, или если вы хотите, чтобы обновления происходили по расписанию.

Это можно сделать с помощью метода `checkForUpdate()`:

<code-example header="check-for-update.service.ts" path="service-worker-getting-started/src/app/check-for-update.service.ts"></code-example>.

Этот метод возвращает `Promise<boolean>`, который указывает, доступно ли обновление для активации. Проверка может закончиться неудачей, что приведет к отказу от `Promise`.

<div class="alert is-important">

Чтобы избежать негативного влияния на начальный рендеринг страницы, `ServiceWorkerModule` по умолчанию ждет до 30 секунд, пока приложение стабилизируется, прежде чем зарегистрировать скрипт ServiceWorker. Постоянный опрос обновлений, например, с помощью [setInterval()](https://developer.mozilla.org/docs/Web/API/WindowOrWorkerGlobalScope/setInterval) или [interval()](https://rxjs.dev/api/index/function/interval) RxJS, не позволяет приложению стабилизироваться, и скрипт ServiceWorker не регистрируется в браузере до достижения верхнего предела в 30 секунд.

<div class="alert is-helpful">

**NOTE**: <br /> This is true for any kind of polling done by your application.
Check the [isStable](api/core/ApplicationRef#isStable) documentation for more information.

</div>

Чтобы избежать этой задержки, сначала дождитесь стабилизации приложения, прежде чем начать опрашивать обновления, как показано в предыдущем примере. В качестве альтернативы вы можете определить другую [стратегию регистрации] (api/service-worker/SwRegistrationOptions#registrationStrategy) для ServiceWorker.

</div>

### Обновление до последней версии

Вы можете обновить существующую вкладку до последней версии, перезагрузив страницу, как только будет готова новая версия. Чтобы не прерывать работу пользователя, как правило, целесообразно запросить у него подтверждение, что он согласен перезагрузить страницу и обновить ее до последней версии:

<code-example header="prompt-update.service.ts" path="service-worker-getting-started/src/app/prompt-update.service.ts" region="sw-version-ready"></code-example>.

<div class="alert is-important">

Вызов {@link SwUpdate#activateUpdate SwUpdate#activateUpdate()} обновляет вкладку до последней версии без перезагрузки страницы, но это может нарушить работу приложения.

Обновление без перезагрузки может создать несоответствие версий между [оболочкой приложения](guide/glossary#app-shell) и другими ресурсами страницы, такими как [куски с ленивой загрузкой](guide/glossary#lazy-loading), имена файлов которых могут меняться между версиями.

Вы должны использовать `activateUpdate()`, только если вы уверены, что это безопасно для вашего конкретного случая использования.

</div>

### Handling an unrecoverable state

In some cases, the version of the application used by the service worker to serve a client might be in a broken state that cannot be recovered from without a full page reload.

For example, imagine the following scenario:

-   A user opens the application for the first time and the service worker caches the latest version of the application.

    Assume the application's cached assets include `index.html`, `main.<main-hash-1>.js` and `lazy-chunk.<lazy-hash-1>.js`.

-   The user closes the application and does not open it for a while.

-   After some time, a new version of the application is deployed to the server.

    This newer version includes the files `index.html`, `main.<main-hash-2>.js` and `lazy-chunk.<lazy-hash-2>.js`.

      <div class="alert is-helpful">

    **NOTE**: <br />

    The hashes are different now, because the content of the files changed.

      </div>

    The old version is no longer available on the server.

-   In the meantime, the user's browser decides to evict `lazy-chunk.<lazy-hash-1>.js` from its cache.

    Browsers might decide to evict specific \(or all\) resources from a cache in order to reclaim disk space.

-   The user opens the application again.

    Рабочий сервис обслуживает последнюю версию, известную ему на данный момент, а именно старую версию \(`index.html` и `main.<main-hash-1>.js`\).

-   Позже приложение запрашивает ленивый пакет, `lazy-chunk.<lazy-hash-1>.js`.

-   Сервисный работник не может найти актив в кэше\(помните, что браузер изгнал его\).

    Он также не может получить его с сервера\\(потому что на сервере теперь есть только `lazy-chunk.<lazy-hash-2>.js` из более новой версии\).

В предыдущем сценарии работник службы не может обслужить актив, который обычно кэшируется. Эта конкретная версия приложения сломана, и нет способа исправить состояние клиента без перезагрузки страницы.
В таких случаях работник службы уведомляет клиента, отправляя событие `UnrecoverableStateEvent`.

Подпишитесь на `SwUpdate#unrecoverable`, чтобы получать уведомления и обрабатывать эти ошибки.

<code-example header="handle-unrecoverable-state.service.ts" path="service-worker-getting-started/src/app/handle-unrecoverable-state.service.ts" region="sw-unrecoverable-state"></code-example>.

## Больше о рабочих службах Angular

Вас также может заинтересовать следующее:

-   [Service Worker Notifications](guide/service-worker-notifications)

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
