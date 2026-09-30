---
description: "Режим без ZoneJS ускоряет приложение, упрощает отладку и убирает лишнюю сложность совместимости с браузером."
---

# Angular без ZoneJS (zoneless) {: #angular-without-zonejs-zoneless}

:date: 30.09.2026

## Зачем режим без ZoneJS? {: #why-use-zoneless}

Главные причины убрать зависимость ZoneJS:

-   **Выше скорость.** ZoneJS считает события DOM и асинхронные задачи признаком того, что состояние приложения _могло_ измениться, и после этого запускает синхронизацию: обнаружение изменений по представлениям приложения. ZoneJS не знает, изменилось ли состояние на самом деле, поэтому синхронизация срабатывает чаще, чем нужно.
-   **Лучше Core Web Vitals.** У ZoneJS заметные накладные расходы и на размер поставки, и на время запуска.
-   **Проще отладка.** С ZoneJS код отлаживать труднее. Трассировки стека читаются хуже. Труднее и разобрать поломку, которая произошла из-за кода вне зоны Angular.
-   **Лучше совместимость с экосистемой.** ZoneJS работает, подменяя API браузера, но патчи есть не для каждого нового API. Некоторые API, например `async`/`await`, нормально не патчатся, и синтаксис приходится опускать до более старого, чтобы он работал с ZoneJS. Библиотеки экосистемы тоже иногда несовместимы с тем, как ZoneJS патчит нативные API. Без зависимости ZoneJS совместимость на длинной дистанции лучше: уходит источник сложности, подмены нативных API и постоянной поддержки.

## Включение режима без ZoneJS {: #enabling-zoneless-in-an-application}

В Angular v21 и новее режим без ZoneJS включён по умолчанию, отдельно его включать не нужно. Проверьте, что `provideZoneChangeDetection` нигде не переопределяет конфигурацию по умолчанию.

В Angular v20 обнаружение изменений без ZoneJS включают функцией `provideZonelessChangeDetection()` при запуске приложения:

```ts
bootstrapApplication(MyApp, {providers: [provideZonelessChangeDetection()]});
```

```ts
platformBrowser().bootstrapModule(AppModule);

@NgModule({
  providers: [provideZonelessChangeDetection()],
})
export class AppModule {}
```

## Удаление ZoneJS {: #removing-zonejs}

Приложению без ZoneJS стоит полностью убрать ZoneJS из сборки, чтобы уменьшить размер бандла. Обычно ZoneJS подключают параметром `polyfills` в `angular.json`, и в цели `build`, и в цели `test`. Уберите оттуда `zone.js` и `zone.js/testing`, чтобы пакет не попал в сборку. Если в проекте есть явный файл `polyfills.ts`, удалите из него `import 'zone.js';` и `import 'zone.js/testing';`.

После удаления ZoneJS из сборки зависимость `zone.js` тоже не нужна, и пакет можно убрать полностью:

```shell
npm uninstall zone.js
```

## Требования совместимости с режимом без ZoneJS {: #requirements-for-zoneless-compatibility}

Angular решает, когда запускать обнаружение изменений и в каких представлениях, по уведомлениям от основных API.

Среди таких уведомлений:

-   `ChangeDetectorRef.markForCheck` (его автоматически вызывает `AsyncPipe`)
-   `ComponentRef.setInput`
-   обновление сигнала, который читается в шаблоне
-   обратные вызовы привязанных слушателей на хосте или в шаблоне
-   подключение представления, которое один из способов выше пометил как грязное

### Компоненты, совместимые с `OnPush` {: #onpush-compatible-components}

Убедиться, что компонент пользуется перечисленными уведомлениями, можно стратегией [ChangeDetectionStrategy.OnPush](https://angular.dev/best-practices/skipping-subtrees#using-onpush).

Стратегия обнаружения изменений `OnPush` не обязательна, но для компонентов приложения это рекомендуемый шаг к совместимости с режимом без ZoneJS. Компонентам библиотеки не всегда можно поставить `ChangeDetectionStrategy.OnPush`. Если библиотечный компонент служит хостом пользовательских компонентов, которые могут использовать `ChangeDetectionStrategy.Eager` или `Default`, ему нельзя брать `OnPush`: иначе дочерний компонент не обновится, когда он сам с `OnPush` не совместим и рассчитывает, что обнаружение изменений запустит ZoneJS. Компонент может оставаться на стратегии `Default`, если сообщает Angular, когда нужно обнаружение изменений: вызывает `markForCheck`, использует сигналы, `AsyncPipe` и так далее. Быть хостом пользовательского компонента — значит вызывать API вроде `ViewContainerRef.createComponent`, а не просто размещать часть шаблона этого компонента (проекцию содержимого или вход со ссылкой на шаблон).

### Удаление `NgZone.onMicrotaskEmpty`, `NgZone.onUnstable`, `NgZone.isStable` и `NgZone.onStable` {: #remove-ngzoneonmicrotaskempty-ngzoneonunstable-ngzoneisstable-or-ngzoneonstable}

Приложениям и библиотекам нужно убрать обращения к `NgZone.onMicrotaskEmpty`, `NgZone.onUnstable` и `NgZone.onStable`. Когда в приложении включено обнаружение изменений без ZoneJS, эти наблюдаемые объекты не эмитят ни разу. `NgZone.isStable` при этом всегда равен `true`, и по нему нельзя решать, выполнять ли код.

Наблюдаемые `NgZone.onMicrotaskEmpty` и `NgZone.onStable` чаще всего ждут, пока Angular закончит обнаружение изменений, и только потом выполняют задачу. Их заменяют на `afterNextRender`, если нужно дождаться одного прохода обнаружения изменений, и на `afterEveryRender`, если условие может занять несколько проходов. В остальных случаях их брали потому, что они были под рукой и срабатывали примерно тогда, когда нужно. Часто прямее взять API DOM, например `MutationObserver`, если коду нужно определённое состояние DOM, а не косвенное ожидание через хуки отрисовки Angular.

!!! info "NgZone.run и NgZone.runOutsideAngular совместимы с режимом без ZoneJS"

    `NgZone.run` и `NgZone.runOutsideAngular` можно не удалять: код и так совместим с приложениями без ZoneJS. Если убрать эти вызовы, библиотеки, которые ещё работают в приложениях с ZoneJS, могут стать медленнее.

### `PendingTasks` для серверного рендеринга {: #pendingtasks-for-server-side-rendering-ssr}

При серверном рендеринге Angular опирается на ZoneJS, чтобы понять, когда приложение «стабильно» и его можно сериализовать. Если асинхронная задача должна задержать сериализацию, приложение без ZoneJS сообщает о ней Angular через сервис [PendingTasks](https://angular.dev/api/core/PendingTasks). Сериализация дождётся первого момента, когда все незавершённые задачи сняты.

Два самых прямых применения незавершённых задач — метод `run`:

```ts
const taskService = inject(PendingTasks);
taskService.run(async () => {
  const someResult = await doSomeWorkThatNeedsToBeRendered();
  this.someState.set(someResult);
});
```

Для более сложных случаев задачу добавляют и снимают вручную:

```ts
const taskService = inject(PendingTasks);
const taskCleanup = taskService.add();
try {
  await doSomeWorkThatNeedsToBeRendered();
} catch {
  // handle error
} finally {
  taskCleanup();
}
```

Кроме того, вспомогательная функция [pendingUntilEvent](https://angular.dev/api/core/rxjs-interop/pendingUntilEvent) из `rxjs-interop` удерживает приложение в нестабильном состоянии, пока наблюдаемый объект не эмитнет значение, не завершится, не сообщит об ошибке или пока от него не отпишутся.

```ts
readonly myObservableState = someObservable.pipe(pendingUntilEvent());
```

Фреймворк сам пользуется этим сервисом и не сериализует приложение, пока асинхронные задачи не закончены. Среди таких задач, в частности, идущая навигация маршрутизатора и незаконченный запрос `HttpClient`.

### Реактивные формы в приложениях без ZoneJS {: #reactive-forms-in-zoneless-applications}

Обновление модели реактивных форм (`setValue`, `patchValue`, `FormArray.push` и похожие API) меняет состояние формы и шлёт значения в наблюдаемые объекты формы, но само не планирует обнаружение изменений компонента.

Если шаблон зависит от состояния реактивной формы, свяжите наблюдаемые формы с уведомлением для обнаружения изменений (например, `ChangeDetectorRef.markForCheck()`) или отдайте данные сигналами, которые читает шаблон.

## Тестирование и отладка {: #testing-and-debugging}

### Режим без ZoneJS в `TestBed` {: #using-zoneless-in-testbed}

По умолчанию `TestBed` обнаруживает изменения через Zone, если `zone.js` загружен в `polyfills`.

Если `zone.js` нет, `TestBed` по умолчанию работает без ZoneJS. Чтобы включить этот режим принудительно, пока `zone.js` загружен, добавьте `provideZonelessChangeDetection()`:

```ts
TestBed.configureTestingModule({
  // Optional: include the provider to force the testing environment
  // uses the same zoneless behavior as a zoneless application.
  providers: [provideZonelessChangeDetection()],
});

const fixture = TestBed.createComponent(MyComponent);
await fixture.whenStable();
```

Чтобы тесты вели себя как продакшен-код, по возможности не вызывайте `fixture.detectChanges()`. Вызов заставляет обнаружение изменений идти даже тогда, когда Angular его не планировал. Тест должен проверить, что уведомления действительно есть, и оставить Angular решать, когда синхронизировать состояние, а не форсировать это в тесте.

В уже написанных тестах `fixture.detectChanges()` встречается часто, и переписывать их на `await fixture.whenStable()` обычно не окупается. `TestBed` всё равно потребует, чтобы компонент фикстуры был совместим с `OnPush`, и выбросит `ExpressionChangedAfterItHasBeenCheckedError`, если значения шаблона изменились без уведомления (то есть `fixture.componentInstance.someValue = 'newValue';`). Если компонент работает в продакшене, исправьте его: храните состояние в сигналах или вызывайте `ChangeDetectorRef.markForCheck()`. Если компонент лишь обёртка для теста и в приложении не используется, достаточно `fixture.changeDetectorRef.markForCheck()`.

### Проверка в режиме отладки, что обновления замечены {: #debug-mode-check-to-ensure-updates-are-detected}

Ещё один инструмент Angular проверяет, что приложение меняет состояние способом, совместимым с режимом без ZoneJS. Вызов `provideCheckNoChangesConfig({exhaustive: true, interval: <milliseconds>})` периодически проверяет, что ни одна привязка не обновилась без уведомления. Если привязка изменилась так, что обнаружение изменений без ZoneJS её бы не обновило, Angular выбрасывает `ExpressionChangedAfterItHasBeenCheckedError`.


---

Источник: [https://angular.dev/guide/zoneless](https://angular.dev/guide/zoneless)
