---
description: Этот обучающий урок демонстрирует, как использовать директиву ngFor в шаблонах Angular для отображения динамически повторяющихся данных в шаблоне
---

# Урок 8 - Использование `*ngFor` для вывода списка объектов в компоненте

Этот обучающий урок демонстрирует, как использовать директиву `ngFor` в шаблонах Angular для отображения динамически повторяющихся данных в шаблоне.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 10 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в уроке 7, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите код из Урока 7, где вы можете:

    -   Использовать [живой пример](https://angular.io/generated/live-examples/first-app-lesson-07/stackblitz.html) в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать [download пример](https://angular.io/generated/zips/first-app-lesson-07/first-app-lesson-07.zip) и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите [Введение в Angular tutorial](first-app.md), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

Если у вас возникнут трудности во время этого урока, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-08/stackblitz.html) для этого урока.

## После завершения

-   Вы добавите набор данных в приложение.

-   Ваше приложение будет отображать список элементов из нового набора данных с помощью `ngFor`.

## Концептуальный обзор ngFor

В Angular `ngFor` - это особый тип [директив](built-in-directives.md), используемый для динамического повторения данных в шаблоне. В обычном JavaScript вы бы использовали цикл for - ngFor обеспечивает аналогичную функциональность для шаблонов Angular. Мы используем [Angular template syntax](template-syntax.md) для указания деталей директивы.

Вы можете использовать `ngFor` для итерации по массивам и даже асинхронным значениям. В этом уроке вы добавите новый массив данных для итерации.

Для более подробного объяснения, пожалуйста, обратитесь к руководству [Built-in directives](built-in-directives.md#ngFor).

## Шаги урока

Выполните эти шаги над кодом приложения в вашей IDE.

### Шаг 1 - Добавьте данные о жилье в `HomeComponent`.

В `HomeComponent` есть только одно местоположение жилья. В этом шаге вы добавите массив записей `HousingLocation`.

1.  В `src/app/home/home/home.component.ts` удалите свойство `housingLocation` из класса `HomeComponent`.

2.  Обновите класс `HomeComponent`, чтобы он имел свойство `housingLocationList`. Обновите свой код, чтобы он соответствовал следующему коду:

    ```ts
    export class HomeComponent {
        readonly baseUrl =
            'https://angular.io/assets/images/tutorials/faa';

        housingLocationList: HousingLocation[] = [
            {
                id: 0,
                name: 'Acme Fresh Start Housing',
                city: 'Chicago',
                state: 'IL',
                photo: `${this.baseUrl}/bernard-hermant-CLKGGwIBTaY-unsplash.jpg`,
                availableUnits: 4,
                wifi: true,
                laundry: true,
            },
            {
                id: 1,
                name: 'A113 Transitional Housing',
                city: 'Santa Monica',
                state: 'CA',
                photo: `${this.baseUrl}/brandon-griggs-wR11KBaB86U-unsplash.jpg`,
                availableUnits: 0,
                wifi: false,
                laundry: true,
            },
            {
                id: 2,
                name: 'Warm Beds Housing Support',
                city: 'Juneau',
                state: 'AK',
                photo: `${this.baseUrl}/i-do-nothing-but-love-lAyXdl1-Wmc-unsplash.jpg`,
                availableUnits: 1,
                wifi: false,
                laundry: false,
            },
            {
                id: 3,
                name: 'Homesteady Housing',
                city: 'Chicago',
                state: 'IL',
                photo: `${this.baseUrl}/ian-macdonald-W8z6aiwfi1E-unsplash.jpg`,
                availableUnits: 1,
                wifi: true,
                laundry: false,
            },
            {
                id: 4,
                name: 'Happy Homes Group',
                city: 'Gary',
                state: 'IN',
                photo: `${this.baseUrl}/krzysztof-hepner-978RAXoXnH4-unsplash.jpg`,
                availableUnits: 1,
                wifi: true,
                laundry: false,
            },
            {
                id: 5,
                name: 'Hopeful Apartment Group',
                city: 'Oakland',
                state: 'CA',
                photo: `${this.baseUrl}/r-architecture-JvQ0Q5IkeMM-unsplash.jpg`,
                availableUnits: 2,
                wifi: true,
                laundry: true,
            },
            {
                id: 6,
                name: 'Seriously Safe Towns',
                city: 'Oakland',
                state: 'CA',
                photo: `${this.baseUrl}/phil-hearing-IYfp2Ixe9nM-unsplash.jpg`,
                availableUnits: 5,
                wifi: true,
                laundry: true,
            },
            {
                id: 7,
                name: 'Hopeful Housing Solutions',
                city: 'Oakland',
                state: 'CA',
                photo: `${this.baseUrl}/r-architecture-GGupkreKwxA-unsplash.jpg`,
                availableUnits: 2,
                wifi: true,
                laundry: true,
            },
            {
                id: 8,
                name: 'Seriously Safe Towns',
                city: 'Oakland',
                state: 'CA',
                photo: `${this.baseUrl}/saru-robert-9rP3mxf8qWI-unsplash.jpg`,
                availableUnits: 10,
                wifi: false,
                laundry: false,
            },
            {
                id: 9,
                name: 'Capital Safe Towns',
                city: 'Portland',
                state: 'OR',
                photo: `${this.baseUrl}/webaliser-_TPTXZd9mOo-unsplash.jpg`,
                availableUnits: 6,
                wifi: true,
                laundry: true,
            },
        ];
    }
    ```

    !!!warning ""

        Не удаляйте декоратор `@Component`, вы обновите этот код в следующем шаге.

### Шаг 2 - Обновление шаблона `HomeComponent` для использования `ngFor`

Теперь у приложения есть набор данных, который можно использовать для отображения записей в браузере с помощью директивы `ngFor`.

1.  Обновите тег `<app-house-location>` в коде шаблона следующим образом:

    ```ts
    <app-housing-location
    	*ngFor="let housingLocation of housingLocationList"
    	[housingLocation]="housingLocation">
    </app-housing-location>
    ```

    Обратите внимание, в коде `[housingLocation] = "housingLocation"` значение `housingLocation` теперь относится к переменной, используемой в директиве `ngFor`. До этого изменения оно ссылалось на свойство класса `HomeComponent`.

2.  Сохраните все изменения.

3.  Обновите браузер и убедитесь, что приложение теперь отображает сетку расположения жилья.

    ![рамка браузера приложения homes-app, отображающая логотип, поле ввода текста фильтра, кнопку поиска и сетку карточек расположения жилья](homes-app-lesson-08-step-2.png)

## Обзор урока

В этом уроке вы использовали директиву `ngFor` для динамического повторения данных в шаблонах Angular. Вы также добавили новый массив данных для использования в приложении Angular. Теперь приложение динамически отображает список мест расположения жилья в браузере.

Приложение обретает форму, отличная работа.

Если у вас возникли трудности с этим уроком, вы можете просмотреть [готовый код](https://angular.io/generated/live-examples/first-app-lesson-08/stackblitz.html) для него.

## Следующие шаги

-   [Урок 9 - Добавление сервиса в приложение](first-app-lesson-09.md)

## Для получения дополнительной информации о темах, рассмотренных в этом уроке, посетите:

-   [Structural Directives](structural-directives.md)
-   [ngFor guide](built-in-directives.md#ngFor)
-   [ngFor](https://angular.io/api/common/NgFor)

## Ссылки

-   [Lesson 8: Use `*ngFor` to list objects in component](https://angular.io/tutorial/first-app/first-app-lesson-08)
