# Первое приложение Angular урок 3 - Создание компонента HousingLocation приложения

Этот урок демонстрирует, как добавить компонент `HousingLocation` в ваше приложение Angular.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 10 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, который вы создали в Уроке 2, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите <live-example name="first-app-lesson-02"></live-example> из Урока 1, где вы можете:

    -   Использовать _живой пример_ в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать _download пример_ и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](tutorial/first-app), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть готовый код для этого урока в <live-example></live-example> для этого урока.

## После завершения

-   В вашем приложении появился новый компонент: `HousingLocationComponent`, и оно отображает сообщение, подтверждающее, что компонент был добавлен в ваше приложение.

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 - Создание компонента `HousingLocationComponent`.

В этом шаге вы создаете новый компонент для вашего приложения.

В панели **Терминал** вашей IDE:

1. Выполните эту команду, чтобы создать новый `HousingLocationComponent`.

 <code-example format="shell" language="shell">
  ng generate component HousingLocation --standalone --inline-template --skip-tests
 </code-example>

1. Выполните эту команду, чтобы собрать и обслужить ваше приложение.

    <code-example format="shell" language="shell">

    ng serve

    </code-example>

1. Откройте браузер и перейдите по адресу `http://localhost:4200`, чтобы найти приложение.

1. Убедитесь, что приложение создается без ошибок.

    Примечание: оно должно отображаться так же, как и в предыдущем уроке, потому что, хотя вы и добавили новый компонент, вы еще не включили его ни в один из шаблонов приложения.

1. Оставьте `ng serve` запущенным, пока вы выполняете следующие шаги.

### Шаг 2 - Добавьте новый компонент в макет вашего приложения.

В этом шаге вы добавите новый компонент `HousingLocationComponent` к `HomeComponent` вашего приложения, чтобы он отображался в макете вашего приложения.

В панели **Редактирование** вашей IDE:

1.  Откройте `home.component.ts` в редакторе.

1.  В `home.component.ts` импортируйте `HousingLocationComponent`, добавив эту строку в импорт на уровне файла.

    <code-example header="Import HousingLocationComponent in src/app/home/home/home.component.ts" path="first-app-lesson-03/src/app/home/home.component.ts" region="import-housingLocation"></code-example >

1.  Далее обновите свойство `imports` метаданных `@Component`, добавив `HousingLocationComponent` в массив.

    <code-example header="Add HousingLocationComponent to imports array in src/app/home/home.component.ts" path="first-app-lesson-03/src/app/home/home.component.ts" region="add-housingLocation-to-array"></code-example>.

1.  Теперь компонент готов к использованию в шаблоне для `HomeComponent`. Обновите свойство `template` метаданных `@Component`, чтобы включить ссылку на тег `<app-housing-location>`.

    <code-example header="Add housing location to the component template in src/app/home/home/home.component.ts" path="first-app-lesson-03/src/app/home/home.component.ts" region="add-housingLocation-to-template"></code-example>.

### Шаг 3 - Добавление стилей для компонента

В этом шаге вы скопируете предварительно написанные стили для компонента `HousingLocationComponent` в ваше приложение, чтобы оно отображалось правильно.

1. Откройте файл `src/app/housing-location/housing-location.css` и вставьте в него стили, приведенные ниже:

    <code-example header="Add CSS styles to housing location to the component in src/app/housing-location/housing-location/housing-location.component.css" path="first-app-lesson-03/src/app/housing-location/housing-location.component.css"></code-example>.

1. Сохраните код, вернитесь в браузер и убедитесь, что приложение собирается без ошибок. На экране должно появиться сообщение "housing-location works!". Исправьте все ошибки, прежде чем переходить к следующему шагу.

    <section class="lightbox">

    <img alt="рамка браузера приложения homes-app, отображающая логотип, поле ввода текста фильтра, кнопку поиска и сообщение "Жилье-место работает!" src="generated/images/guide/faa/homes-app-lesson-03-step-2.png">

    </section>

## Обзор урока

В этом уроке вы создали новый компонент для своего приложения и добавили его в макет приложения.

Если у вас возникли трудности с этим уроком, вы можете просмотреть готовый код для него в <live-example></live-example>.

## Следующие шаги

-   [Первое приложение Angular урок 4 - Добавление в приложение интерфейса определения местоположения жилья](tutorial/first-app/first-app-lesson-04)
