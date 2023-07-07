# Использование библиотек Angular, опубликованных на npm

Когда вы создаете свое приложение Angular, воспользуйтесь преимуществами сложных библиотек первой стороны, а также богатой экосистемой библиотек сторонних разработчиков. [Angular Material][angularmaterialmain] является примером сложной сторонней библиотеки.

Ссылки на самые популярные библиотеки можно найти в разделе [Angular Resources][aioresources].

## Установка библиотек

Библиотеки публикуются как [npm-пакеты][aioguidenpmpackages], обычно вместе со схемами, интегрирующими их с Angular CLI. Чтобы интегрировать многократно используемый код библиотеки в приложение, необходимо установить пакет и импортировать предоставленную функциональность в то место, где вы ее используете.

Для большинства опубликованных библиотек Angular используйте команду `ng add <lib_name>` Angular CLI.

Команда `ng add` Angular CLI использует менеджер пакетов для установки пакета библиотеки и вызывает схемы, включенные в пакет, для других подмостков в коде проекта. Примерами менеджеров пакетов являются [npm][npmjsmain] или [yarn][yarnpkgmain].

Дополнительные подмостки в коде проекта включают операторы импорта, шрифты и темы.

Опубликованная библиотека обычно содержит файл `README` или другую документацию о том, как добавить эту библиотеку в ваше приложение. В качестве примера смотрите документацию [Angular Material][angularmaterialmain].

### Типы библиотек

Как правило, пакеты библиотек включают типизации в файлы `.d.ts`; см. примеры в `node_modules/@angular/material`. Если пакет вашей библиотеки не включает типизации и ваша IDE жалуется на это, возможно, вам нужно установить пакет `@types/<lib_name>` вместе с библиотекой.

Например, предположим, у вас есть библиотека с именем `d3`:

<code-example format="shell" language="shell">

npm install d3 --save npm install &commat;types/d3 --save-dev

</code-example>

Типы, определенные в пакете `@types/` для библиотеки, установленной в рабочем пространстве, автоматически добавляются в конфигурацию TypeScript для проекта, использующего эту библиотеку. TypeScript по умолчанию ищет типы в каталоге `node_modules/@types`, поэтому вам не придется добавлять каждый пакет типов отдельно.

Если библиотека не имеет типов, доступных в каталоге `@types/`, вы можете использовать ее, добавив типы для нее вручную. Для этого:

1.  Создайте файл `typings.d.ts` в вашем каталоге `src/`.

    Этот файл автоматически включается в качестве глобального определения типа.

1.  Добавьте следующий код в `src/typings.d.ts`:

    <code-example format="typescript" language="typescript">

    объявить модуль 'host' {

    export interface Host {

    протокол?: строка;

    имя хоста?: string

    имя пути?: string;

    }

    export function parse(url: string, queryString?: string): Host;

    }

    </code-example>

1.  В компонент или файл, использующий библиотеку, добавьте следующий код:

    <code-example format="typescript" language="typescript">

    import \* as host from 'host';

    const parsedUrl = host.parse('https://angular.io');

    console.log(parsedUrl.hostname);

    </code-example>

Определите больше типов по мере необходимости.

## Обновление библиотек

Библиотека может обновляться издателем, а также имеет отдельные зависимости, которые необходимо поддерживать в актуальном состоянии. Чтобы проверить обновления установленных библиотек, используйте команду [`ng update`][aiocliupdate] Angular CLI.

Используйте команду `ng update <lib_name>` Angular CLI для обновления версий отдельных библиотек. Angular CLI проверяет последний опубликованный релиз библиотеки, и если последняя версия новее, чем установленная вами версия, загружает ее и обновляет ваш `package.json` в соответствии с последней версией.

Когда вы обновляете Angular до новой версии, вам необходимо убедиться, что все используемые вами библиотеки актуальны. Если библиотеки имеют взаимозависимость, возможно, вам придется обновлять их в определенном порядке.
См. руководство [Angular Update Guide][angularupdatemain] для справки.

## Добавление библиотеки в глобальную область видимости времени выполнения

Если унаследованная библиотека JavaScript не импортирована в приложение, вы можете добавить ее в глобальную область видимости во время выполнения и загрузить ее, как если бы она была добавлена в тег сценария. Настройте Angular CLI на выполнение этого действия во время сборки, используя опции `scripts` и `styles` цели сборки в файле конфигурации сборки рабочего пространства [`angular.json`][aioguideworkspaceconfig].

Например, чтобы использовать библиотеку [Bootstrap 4][getbootstrapdocs40gettingstartedintroduction].

1.  Установите библиотеку и связанные с ней зависимости с помощью менеджера пакетов npm:

    <code-example format="shell" language="shell">

    npm install jquery --save

    npm install popper.js --save

    npm install bootstrap --save

    </code-example>

1.  В конфигурационном файле `angular.json` добавьте связанные файлы сценариев в массив `scripts`:

    <code-example format="json" language="json">.

    "scripts": [

    "node_modules/jquery/dist/jquery.slim.js",

    "node_modules/popper.js/dist/umd/popper.js",

    "node_modules/bootstrap/dist/js/bootstrap.js"

    ],

    </code-example>

1.  Добавьте CSS-файл `bootstrap.css` в массив `styles`:

    <code-example format="css" language="css">.

    "styles": [

    "node_modules/bootstrap/dist/css/bootstrap.css",

    "src/styles.css"

    ],

    </code-example>

1.  Запустите или перезапустите команду `ng serve` Angular CLI, чтобы увидеть работу Bootstrap 4 в вашем приложении.

### Использование глобальных библиотек во время выполнения внутри вашего приложения

После импорта библиотеки с помощью массива "scripts", **не** импортируйте ее с помощью оператора import в коде TypeScript. Следующий фрагмент кода является примером оператора импорта.

<code-example format="typescript" language="typescript">

import \* as \$ from 'jquery';

</code-example>

Если вы импортируете ее с помощью оператора import, у вас будет две разные копии библиотеки: одна импортирована как глобальная библиотека, а другая - как модуль. Это особенно плохо для библиотек с плагинами, таких как JQuery, потому что каждая копия включает разные плагины.

Вместо этого выполните команду `npm install @types/jquery` Angular CLI, чтобы загрузить типы для вашей библиотеки, а затем выполните шаги по установке библиотеки. Это даст вам доступ к глобальным переменным, открываемым этой библиотекой.

### Определение типов для глобальных библиотек во время выполнения

Если глобальная библиотека, которую вам нужно использовать, не имеет глобальных типов, вы можете объявить их вручную как `any` в `src/typings.d.ts`.

Например:

<code-example format="typescript" language="typescript">

declare var libraryName: any;

</code-example>

Некоторые скрипты расширяют другие библиотеки; например, плагины JQuery:

<code-example format="typescript" language="typescript">

\$('.test').myPlugin();

</code-example>

В этом случае установленный `@types/jquery` не включает `myPlugin`, поэтому необходимо добавить интерфейс в `src/typings.d.ts`. Например:

<code-example format="typescript" language="typescript">

интерфейс JQuery { myPlugin(options?: any): any;
}

</code-example>

Если вы не добавите интерфейс для определяемого сценарием расширения, ваша IDE выдаст ошибку:

<code-example format="none" language="none">

[TS][ошибка] Свойство 'myPlugin' не существует для типа 'JQuery'

</code-example>

<!-- links -->

[aiocliupdate]: cli/update 'ng update | CLI |Angular'
[aioguidenpmpackages]: guide/npm-packages 'Workspace npm dependencies | Angular'
[aioguideworkspaceconfig]: guide/workspace-config 'Angular workspace configuration | Angular'
[aioresources]: resources 'Explore Angular Resources | Angular'

<!-- external links -->

[angularmaterialmain]: https://material.angular.io 'Angular Material | Angular'
[angularupdatemain]: https://update.angular.io 'Angular Update Guide | Angular'
[getbootstrapdocs40gettingstartedintroduction]: https://getbootstrap.com/docs/4.0/getting-started/introduction 'Introduction | Bootstrap'
[npmjsmain]: https://www.npmjs.com 'npm'
[yarnpkgmain]: https://yarnpkg.com ' Yarn'

<!-- end links -->

:date: 5.01.2022
