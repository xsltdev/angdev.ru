# Обзор компонентов Angular

Компоненты - это основной строительный блок для приложений Angular. Каждый компонент состоит из:

-   HTML-шаблона, который определяет, что отображается на странице.

-   класса TypeScript, определяющего поведение

-   CSS-селектор, определяющий, как компонент используется в шаблоне.

-   Опционально, стили CSS, применяемые к шаблону.

В этой теме описывается, как создать и настроить компонент Angular.

<div class="alert is-helpful">

Для просмотра или загрузки кода примера, использованного в этой теме, см. <live-example></live-example>.

</div>

## Предварительные условия

Чтобы создать компонент, убедитесь, что вы выполнили следующие предварительные условия:

1.  [Установите Angular CLI.](guide/setup-local#install-the-angular-cli)

1.  [Создайте рабочее пространство Angular](guide/setup-local#create-a-workspace-and-initial-application) с начальным приложением.

    Если у вас нет проекта, создайте его с помощью команды `ng new <project-name>`, где `<project-name>` - имя вашего приложения Angular.

## Создание компонента

Лучший способ создания компонента - это использование Angular CLI. Вы также можете создать компонент вручную.

### Создание компонента с помощью Angular CLI

Чтобы создать компонент с помощью Angular CLI, выполните следующие действия:

1.  В окне терминала перейдите в каталог, содержащий ваше приложение.

1.  Выполните команду `ng generate component <component-name>`, где `<component-name>` - это имя вашего нового компонента.

По умолчанию эта команда создает следующее:

-   каталог с именем компонента

-   Файл компонента, `<component-name>.component.ts'

-   Файл шаблона, `<component-name>.component.html`

-   CSS-файл, `<component-name>.component.css`

-   Файл спецификации тестирования, `<component-name>.component.spec.ts`.

Где `<component-name>` - имя вашего компонента.

<div class="alert is-helpful">

Вы можете изменить, как `ng generate component` создает новые компоненты. Для получения дополнительной информации смотрите [ng generate component](cli/generate#component-command) в документации Angular CLI.

</div>

### Создание компонента вручную

Хотя Angular CLI является лучшим способом создания компонента Angular, вы также можете создать компонент вручную. В этом разделе описано, как создать файл основного компонента в существующем проекте Angular.

Чтобы создать новый компонент вручную:

1.  Перейдите в каталог проекта Angular.
1.  Создайте новый файл `<component-name>.component.ts`.

1.  В верхней части файла добавьте следующий оператор импорта.

    <code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="import"></code-example>.

1.  После оператора `import` добавьте декоратор `@Component`.

    <code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="decorator-skeleton"></code-example>

1.  Выберите CSS-селектор для компонента.

    <code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="selector"></code-example>.

    Для получения дополнительной информации о выборе селектора смотрите [Указание селектора компонента](#specifying-a-components-css-selector).

1.  Определите HTML-шаблон, который компонент использует для отображения информации.

    В большинстве случаев этот шаблон представляет собой отдельный HTML-файл.

    <code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="templateUrl"></code-example>.

    Для получения дополнительной информации об определении шаблона компонента смотрите [Определение шаблона компонента] (#defining-a-components-template).

1.  Выберите стили для шаблона компонента.

    В большинстве случаев стили для шаблона компонента задаются в отдельном файле.

    <code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="decorator"></code-example>.

1.  Добавьте оператор `class`, включающий код компонента.

    <code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="class"></code-example>.

## Указание CSS-селектора компонента

Каждый компонент требует наличия CSS _селектора_. Селектор предписывает Angular инстанцировать этот компонент везде, где он найдет соответствующий тег в HTML шаблона. Например, рассмотрим компонент `hello-world.component.ts`, который определяет свой селектор как `app-hello-world`.
Этот селектор предписывает Angular инстанцировать этот компонент каждый раз, когда в шаблоне появляется тег `<app-hello-world>`.

Укажите селектор компонента, добавив оператор `selector` в декоратор `@Component`.

<code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="selector"></code-example>.

## Определение шаблона компонента

Шаблон - это блок HTML, который указывает Angular, как отобразить компонент в вашем приложении. Определите шаблон для вашего компонента одним из двух способов: ссылкой на внешний файл или непосредственно в компоненте.

Чтобы определить шаблон как внешний файл, добавьте свойство `templateUrl` к декоратору `@Component`.

<code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="templateUrl"></code-example>.

Чтобы определить шаблон внутри компонента, добавьте свойство `template` к декоратору `@Component`, содержащее HTML, который вы хотите использовать.

<code-example path="component-overview/src/app/component-overview/component-overview.component.1.ts" region="template"></code-example>

If you want your template to span multiple lines, use backticks \(<code>&grave;</code>\). For example:

<code-example path="component-overview/src/app/component-overview/component-overview.component.2.ts" region="templatebacktick"></code-example>

<div class="alert is-helpful">

Компонент Angular требует шаблона, определенного с помощью `template` или `templateUrl`. Вы не можете иметь оба утверждения в компоненте.

</div>

## Объявление стилей компонента

Объявите стили компонента, используемые для его шаблона, одним из двух способов: Ссылаясь на внешний файл, или непосредственно в компоненте.

Чтобы объявить стили для компонента в отдельном файле, добавьте свойство `styleUrls` к декоратору `@Component`.

<code-example path="component-overview/src/app/component-overview/component-overview.component.ts" region="decorator"></code-example>.

Чтобы объявить стили внутри компонента, добавьте свойство `styles` к декоратору `@Component`, содержащему стили, которые вы хотите использовать.

<code-example path="component-overview/src/app/component-overview/component-overview.component.3.ts" region="styles"></code-example>.

Свойство `styles` принимает массив строк, содержащих объявления правил CSS.

## Следующие шаги

-   Для архитектурного обзора компонентов смотрите [Введение в компоненты и шаблоны](guide/architecture-components)

-   Дополнительные параметры, которые можно использовать при создании компонента, см. в разделе [Component](api/core/Component) в API Reference.

-   Для получения дополнительной информации о стилях компонентов смотрите [Стили компонентов](guide/component-styles)

-   Для получения дополнительной информации о шаблонах смотрите [Синтаксис шаблонов](guide/template-syntax)

<!-- links -->

<!-- external links -->

<!-- end links -->

@ просмотрено 2022-02-28
