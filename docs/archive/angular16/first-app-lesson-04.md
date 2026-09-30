---
description: Этот урок демонстрирует, как создать интерфейс и включить его в компонент вашего приложения
---

# Урок 4: Создание интерфейса

Этот урок демонстрирует, как создать интерфейс и включить его в компонент вашего приложения.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 10 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в Уроке 3, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите из Урока 3, где вы можете:

    -   Использовать [живой пример](https://angular.io/generated/live-examples/first-app-lesson-03/stackblitz.html) в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать [download пример](https://angular.io/generated/zips/first-app-lesson-03/first-app-lesson-03.zip) и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](first-app.md), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-04/stackblitz.html) для этого урока.

## После завершения

-   Ваше приложение имеет новый интерфейс, который оно может использовать в качестве типа данных.

-   В вашем приложении есть экземпляр нового интерфейса с образцом данных.

## Концептуальный обзор интерфейсов

[Интерфейсы](https://www.typescriptlang.org/docs/handbook/interfaces.html) — это пользовательские типы данных для вашего приложения.

Angular использует TypeScript, чтобы воспользоваться преимуществами работы в сильно типизированной среде программирования. Сильная проверка типов снижает вероятность того, что один элемент вашего приложения отправит другому неправильно отформатированные данные.

Такие ошибки несоответствия типов отлавливаются компилятором TypeScript, и многие такие ошибки также могут быть отловлены в вашей IDE.

В этом уроке вы создадите интерфейс для определения свойств, представляющих данные о местоположении одного жилья.

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 — Создайте новый интерфейс Angular

Этот шаг создает новый интерфейс в вашем приложении.

В панели **Терминал** вашей IDE:

1.  В каталоге проекта перейдите в каталог `first-app`.

2.  В директории `first-app` выполните эту команду для создания нового интерфейса.

    ```shell
    ng generate interface housinglocation
    ```

3.  Запустите `ng serve`, чтобы создать приложение и передать его по адресу `http://localhost:4200`.

4.  В браузере откройте `http://localhost:4200`, чтобы увидеть ваше приложение.

5.  Убедитесь, что приложение создается без ошибок.

    Исправьте все ошибки, прежде чем переходить к следующему шагу.

### Шаг 2 — Добавление свойств в новый интерфейс

Этот шаг добавляет свойства в интерфейс, которые необходимы вашему приложению для представления местоположения жилья.

1.  В панели **Терминал** вашей IDE запустите команду `ng serve`, если она еще не запущена, чтобы создать приложение и передать его по адресу `http://localhost:4200`.

2.  В панели **Edit** вашей IDE откройте файл `src/app/housinglocation.ts`.

3.  В `housinglocation.ts` замените содержимое по умолчанию на следующий код, чтобы ваш новый интерфейс соответствовал этому примеру.

    ```ts
    export interface HousingLocation {
        id: number;
        name: string;
        city: string;
        state: string;
        photo: string;
        availableUnits: number;
        wifi: boolean;
        laundry: boolean;
    }
    ```

4.  Сохраните изменения и убедитесь, что приложение не выдает никаких ошибок. Исправьте все ошибки, прежде чем переходить к следующему шагу.

На данном этапе вы определили интерфейс, который представляет данные о местоположении жилья, включая идентификатор, имя и информацию о местоположении.

### Шаг 3 — Создание тестового дома для вашего приложения

У вас есть интерфейс, но вы еще не используете его.

На этом шаге вы создаете экземпляр интерфейса и присваиваете ему некоторые образцы данных. Вы еще не увидите, как эти данные появятся в вашем приложении.

Для этого нужно пройти еще несколько уроков.

1.  В панели **Terminal** вашей IDE запустите команду `ng serve`, если она еще не запущена, чтобы создать приложение и обслужить ваше приложение по адресу `http://localhost:4200`.
2.  В панели **Edit** вашей IDE откройте `src/app/home/home.component.ts`.

3.  В `src/app/home/home/home.component.ts` добавьте этот оператор import после существующих операторов `import`, чтобы `HomeComponent` мог использовать новый интерфейс.

    ```ts
    import { HousingLocation } from '../housinglocation';
    ```

4.  В `src/app/home/home/home.component.ts` замените пустое определение `export class HomeComponent {}` на этот код, чтобы создать один экземпляр нового интерфейса в компоненте.

    ```ts
    export class HomeComponent {
        readonly baseUrl =
            'https://angular.io/assets/images/tutorials/faa';

        housingLocation: HousingLocation = {
            id: 9999,
            name: 'Test Home',
            city: 'Test city',
            state: 'ST',
            photo: `${this.baseUrl}/example-house.jpg`,
            availableUnits: 99,
            wifi: true,
            laundry: false,
        };
    }
    ```

5.  Убедитесь, что ваш файл `home.component.ts` соответствует этому примеру.

    ```ts
    import { Component } from '@angular/core';
    import { CommonModule } from '@angular/common';
    import { HousingLocationComponent } from '../housing-location/housing-location.component';
    import { HousingLocation } from '../housinglocation';

    @Component({
        selector: 'app-home',
        standalone: true,
        imports: [CommonModule, HousingLocationComponent],
        template: `
            <section>
                <form>
                    <input
                        type="text"
                        placeholder="Filter by city"
                    />
                    <button class="primary" type="button">
                        Search
                    </button>
                </form>
            </section>
            <section class="results">
                <app-housing-location></app-housing-location>
            </section>
        `,
        styleUrls: ['./home.component.css'],
    })
    export class HomeComponent {
        readonly baseUrl =
            'https://angular.io/assets/images/tutorials/faa';

        housingLocation: HousingLocation = {
            id: 9999,
            name: 'Test Home',
            city: 'Test city',
            state: 'ST',
            photo: `${this.baseUrl}/example-house.jpg`,
            availableUnits: 99,
            wifi: true,
            laundry: false,
        };
    }
    ```

    Добавив свойство `housingLocation` типа `HousingLocation` в класс `HomeComponent`, мы можем подтвердить, что данные соответствуют описанию интерфейса. Если данные не удовлетворяют описанию, IDE имеет достаточно информации, чтобы выдать нам полезные ошибки.

6.  Сохраните изменения и подтвердите, что в приложении нет ошибок. Откройте браузер и убедитесь, что ваше приложение по-прежнему отображает сообщение "housing-location works!".

    ![рамка браузера приложения homes-app, отображающая логотип, поле ввода текста фильтра, кнопку поиска и сообщение](homes-app-lesson-03-step-2.png)

7.  Исправьте все ошибки, прежде чем перейти к следующему шагу.

## Обзор урока

В этом уроке вы создали интерфейс, который создал новый тип данных для вашего приложения. Этот новый тип данных позволяет вам указать, где требуются данные `HousingLocation`.
Этот новый тип данных также позволяет вашей IDE и компилятору TypeScript гарантировать, что данные `HousingLocation` используются там, где это необходимо.

Если у вас возникли трудности с этим уроком, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-04/stackblitz.html) для него.

## Следующие шаги

-   [Урок 5 — Добавление входного параметра в компонент](first-app-lesson-05.md)

## Дополнительная информация

Для получения дополнительной информации о темах, рассмотренных в этом уроке, посетите:

-   [ng generate interface](https://angular.io/cli/generate#interface-command)
-   [ng generate](https://angular.io/cli/generate)

## Ссылки

-   [First Angular app lesson 4 — Creating an interface](https://angular.io/tutorial/first-app/first-app-lesson-04)
