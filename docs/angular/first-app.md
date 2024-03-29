---
description: Этот учебник состоит из уроков, в которых представлены концепции Angular, которые необходимо знать, чтобы начать кодировать в Angular
---

# Введение в Angular: первое приложение Angular

Этот учебник состоит из уроков, в которых представлены концепции Angular, которые необходимо знать, чтобы начать кодировать в Angular.

Если вы только начинаете изучать Angular, то последовательное прохождение уроков обеспечит наилучший опыт обучения, поскольку каждый урок основывается на предыдущих. После того как вы освоите Angular, вы сможете вернуться к любому уроку для повторного изучения.

Если вы более опытны, уроки этого руководства можно проходить по отдельности. Вы можете сделать столько или столько, сколько захотите, и выполнять их в любом порядке.

## Прежде чем начать

Для получения наилучшего опыта работы с этим учебником ознакомьтесь с этими требованиями, чтобы убедиться, что у вас есть все необходимое для успешной работы.

### Ваш опыт

Уроки в этом учебнике предполагают, что вы сделали следующее:

1.  **Создали веб-страницу HTML, отредактировав непосредственно HTML.**.

    В этом учебнике упоминаются элементы HTML и объектная модель документа (DOM). Если эти термины вам не знакомы, изучите программирование HTML до начала работы над этим учебником.

1.  **Программирование содержимого веб-сайта на JavaScript.**

    В этом учебнике много примеров программирования на TypeScript, который основан на JavaScript. Объясняются специфические особенности TypeScript, но для понимания уроков этого учебника необходимо знакомство с программированием на JavaScript.

1.  **Прочитайте содержание Каскадной таблицы стилей (CSS) и поймите, как используются селекторы**.

    Этот учебник не требует кодирования CSS, но если эти термины вам незнакомы, ознакомьтесь с CSS и селекторами до начала работы над этим учебником.

1.  **Используйте инструкции командной строки для выполнения задач на компьютере.**.

    Для выполнения многих задач в Angular используется командная строка Angular CLI. В этом руководстве приведены команды, которые необходимо использовать, и предполагается, что вы знаете, как открыть инструмент командной строки или интерфейс терминала, в котором их использовать. Если вы не знаете, как использовать инструмент командной строки или терминальный интерфейс, ознакомьтесь с ними перед началом этого урока.

### Ваше оборудование

Эти уроки можно выполнить, используя локальную установку инструментов Angular или используя StackBlitz в веб-браузере. Локальная разработка Angular может быть выполнена на системах на базе Windows, MacOS или Linux.

Преимущество работы на собственном компьютере заключается в том, что вы можете сохранять свою работу локально для дальнейшего использования. Работа в StackBlitz позволяет проходить уроки, не загружая никаких программ на свой компьютер.

## Концептуальный предварительный просмотр вашего первого приложения Angular

В уроках этого руководства создается простое приложение Angular, в котором перечисляются дома, сдаваемые в аренду, и показываются детали отдельных домов. В этом приложении используются функции, характерные для многих приложений Angular.

![Output of heroes dashboard](homes-app-landing-page.png)

## Среда разработки

Если вы планируете выполнить этот учебник на своем локальном компьютере, вам необходимо установить необходимое программное обеспечение. Если вы уже установили некоторые из необходимых программ, необходимо проверить, что они имеют правильную версию.

Выполните эти шаги в инструменте командной строки на компьютере, который вы хотите использовать для этого учебника.

!!!note ""

    Если вы планируете использовать StackBlitz для выполнения уроков, вы можете перейти к первому уроку. Вам не нужно устанавливать никакое программное обеспечение.

### Шаг 1 — Определите версию `node.js`, которую требует Angular

!!!note ""

    Этот шаг необходим только в том случае, если у вас установлена версия node, в противном случае перейдите к шагу 2 ниже.

Для Angular требуется активная LTS или поддерживаемая LTS версия Node. Давайте подтвердим вашу версию `node.js`. Информацию о требованиях к конкретной версии смотрите в свойстве engines в файле [package.json](https://unpkg.com/browse/@angular/core@15.1.5/package.json).

Из окна **Terminal**:

1.  Выполните следующую команду: `node --version`.
2.  Убедитесь, что отображаемый номер версии соответствует требованиям.

### Шаг 2 — Установите правильную версию `node.js` для Angular

Если у вас не установлена версия `node.js`, следуйте [указаниям по установке на nodejs.org](https://nodejs.org/ru/download/)

### Шаг 3 — Установите последнюю версию Angular

Когда `node.js` и `npm` установлены, следующим шагом будет установка [Angular CLI](https://angular.io/cli), который предоставляет инструменты для эффективной разработки Angular.

Из окна **Terminal**:

1.  Выполните следующую команду: `npm install -g @angular/cli`.

2.  После завершения установки в окне терминала появится информация о версии Angular CLI, установленной на вашем локальном компьютере.

### Шаг 4 — Установка интегрированной среды разработки (IDE)

Вы можете использовать любой инструмент для создания приложений с Angular. Мы рекомендуем следующее:

1.  [Visual Studio Code](https://code.visualstudio.com/)

2.  В качестве необязательного, но рекомендуемого шага вы можете дополнительно улучшить свой опыт разработчика, установив [Angular Language Service](https://marketplace.visualstudio.com/items?itemName=Angular.ng-template)

## Обзор урока

В этом уроке вы узнали о приложении, которое вы создадите в этом учебнике, и подготовили свой локальный компьютер к разработке приложений Angular.

## Следующие шаги

-   [Первое приложение Angular урок 1 — Hello world](first-app-lesson-01.md)

## Дополнительная информация

Для получения дополнительной информации по темам, рассмотренным в этом уроке, посетите:

-   [Что такое Angular](what-is-angular.md)
-   [Angular CLI Reference](https://angular.io/cli)

## Ссылки

-   [Build your first Angular app](https://angular.io/tutorial/first-app)
