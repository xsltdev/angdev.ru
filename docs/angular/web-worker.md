# Фоновая обработка с помощью web worker

:date: 28.02.2022

[Web workers](https://developer.mozilla.org/docs/Web/API/Web_Workers_API) позволяет выполнять ресурсоемкие вычисления в фоновом потоке, освобождая основной поток для обновления пользовательского интерфейса. Приложения, выполняющие большое количество вычислений, например, генерирующие чертежи для автоматизированного проектирования (CAD) или выполняющие тяжелые геометрические вычисления, могут использовать веб-рабочие для повышения производительности.

!!!note ""

    Angular CLI не поддерживает самостоятельный запуск в web worker.

## Добавление веб-работника

Чтобы добавить веб-работника в существующий проект, используйте команду Angular CLI `ng generate`.

```
ng generate web-worker <location>
```

Вы можете добавить веб-работника в любое место вашего приложения. Например, чтобы добавить веб-работника в корневой компонент `src/app/app.component.ts`, выполните следующую команду.

```
ng generate web-worker app
```

Команда выполняет следующие действия.

1.  Настраивает ваш проект на использование веб-рабочих, если это еще не так.

2.  Добавляет следующий код scaffold в `src/app/app.worker.ts` для получения сообщений.

    ```ts
    addEventListener('message', ({ data }) => {
        const response = `worker response to ${data}`;
        postMessage(response);
    });
    ```

3.  Добавляет следующий код scaffold в `src/app/app.component.ts` для использования рабочего.

    ```ts
    if (typeof Worker !== 'undefined') {
        // Create a new
        const worker = new Worker(
            new URL('./app.worker', import.meta.url)
        );
        worker.onmessage = ({ data }) => {
            console.log(`page got message: ${data}`);
        };
        worker.postMessage('hello');
    } else {
        // Web workers are not supported in this environment.
        // You should add a fallback so that your program still executes correctly.
    }
    ```

После того как вы создадите этот начальный пример, вы должны рефакторизовать свой код для использования веб-работника, отправляя сообщения на него и с него.

!!!warning ""

    Некоторые среды или платформы, такие как `@angular/platform-server`, используемые в [Server-side Rendering](universal.md), не поддерживают веб-рабочих. Чтобы обеспечить работу вашего приложения в таких средах, вы должны предоставить резервный механизм для выполнения вычислений, которые в противном случае выполнил бы рабочий.

<!-- links -->

<!-- external links -->

<!-- end links -->
