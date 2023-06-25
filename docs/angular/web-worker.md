# Фоновая обработка с помощью web worker

[Web workers](https://developer.mozilla.org/docs/Web/API/Web_Workers_API) позволяет выполнять ресурсоемкие вычисления в фоновом потоке, освобождая основной поток для обновления пользовательского интерфейса. Приложения, выполняющие большое количество вычислений, например, генерирующие чертежи для автоматизированного проектирования \(CAD\) или выполняющие тяжелые геометрические вычисления, могут использовать веб-рабочие для повышения производительности.

<div class="alert is-helpful">

Angular CLI не поддерживает самостоятельный запуск в web worker.

</div>

## Добавление веб-работника

Чтобы добавить веб-работника в существующий проект, используйте команду Angular CLI `ng generate`.

<code-example format="shell" language="shell">

ng generate web-worker &lt;location&gt;

</code-example>

Вы можете добавить веб-работника в любое место вашего приложения. Например, чтобы добавить веб-работника в корневой компонент `src/app/app.component.ts`, выполните следующую команду.

<code-example format="shell" language="shell">

ng generate web-worker app

</code-example>

Команда выполняет следующие действия.

1.  Настраивает ваш проект на использование веб-рабочих, если это еще не так.

1.  Добавляет следующий код scaffold в `src/app/app.worker.ts` для получения сообщений.

    <code-example language="typescript" header="src/app/app.worker.ts">

    addEventListener('message', ({ data }) =&gt; {

    const response = `ответ работника на &dollar;{data}`;

    postMessage(response);

    });

    </code-example>

1.  Добавляет следующий код scaffold в `src/app/app.component.ts` для использования рабочего.

    <code-example language="typescript" header="src/app/app.component.ts">

    if (typeof Worker !== 'undefined') {

    // Создаем новый

    const worker = new Worker(new URL('./app.worker', import.meta.url));

    worker.onmessage = ({ data }) =&gt; {

    console.log(`страница получила сообщение: &dollar;{data}`);

    };

    worker.postMessage('hello');

    } else {

    // Web workers не поддерживаются в этой среде.

    // Вы должны добавить fallback, чтобы ваша программа все еще выполнялась правильно.

    }

    </code-example>

После того как вы создадите этот начальный пример, вы должны рефакторизовать свой код для использования веб-работника, отправляя сообщения на него и с него.

<div class="alert is-important">

Некоторые среды или платформы, такие как `@angular/platform-server`, используемые в [Server-side Rendering](guide/universal), не поддерживают веб-рабочих. Чтобы обеспечить работу вашего приложения в таких средах, вы должны предоставить резервный механизм для выполнения вычислений, которые в противном случае выполнил бы рабочий.

</div>

<!-- links -->

<!-- external links -->

<!-- end links -->

:date: 28.02.2022
