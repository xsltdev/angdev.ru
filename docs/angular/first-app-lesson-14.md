# Урок 14 - Добавьте HTTP-коммуникацию в ваше приложение

Этот урок демонстрирует, как интегрировать HTTP и API в ваше приложение.

До этого момента ваше приложение считывало данные из статического массива в сервисе Angular. Следующим шагом будет использование сервера JSON, с которым ваше приложение будет взаимодействовать по HTTP. HTTP-запрос будет имитировать работу с данными с сервера.

**Затраты времени:** ожидайте, что на выполнение этого урока вы потратите около 20 минут.

## Перед началом

Этот урок начинается с кода из предыдущего урока, поэтому вы можете:

-   Использовать код, созданный в Уроке 13, в своей интегрированной среде разработки (IDE).

-   Начните с примера кода из предыдущего урока. Выберите <live-example name="first-app-lesson-13"></live-example> из Урока 13, где вы можете:

    -   Использовать _живой пример_ в StackBlitz, где интерфейс StackBlitz является вашей IDE.

    -   Использовать _download пример_ и открыть его в вашей IDE.

Если вы не просмотрели введение, посетите учебник [Введение в Angular](first-app.md), чтобы убедиться, что у вас есть все необходимое для завершения этого урока.

## После завершения

-   Ваше приложение будет использовать данные с сервера JSON.

## Шаги урока

Выполните эти шаги в терминале на вашем локальном компьютере.

### Шаг 1 - Настройка сервера JSON

JSON Server - это инструмент с открытым исходным кодом, используемый для создания имитационных REST API. Вы будете использовать его для обслуживания данных о местоположении жилья, которые в настоящее время хранятся в службе жилья.

1.  Install `json-server` from npm by using the following command.
    <code-example language="bash" format="bash">
    npm install -g json-server
    </code-example>

1.  In the root directory of your project, create a file called `db.json`. This is where you will store the data for the `json-server`.

1.  Open `db.json` and copy the following code into the file
    <code-example language="json" format="json">
    {
    "locations": [
    {
    "id": 0,
    "name": "Acme Fresh Start Housing",
    "city": "Chicago",
    "state": "IL",
    "photo": "/assets/bernard-hermant-CLKGGwIBTaY-unsplash.jpg",
    "availableUnits": 4,
    "wifi": true,
    "laundry": true
    },
    {
    "id": 1,
    "name": "A113 Transitional Housing",
    "city": "Santa Monica",
    "state": "CA",
    "photo": "/assets/brandon-griggs-wR11KBaB86U-unsplash.jpg",
    "availableUnits": 0,
    "wifi": false,
    "laundry": true
    },
    {
    "id": 2,
    "name": "Warm Beds Housing Support",
    "city": "Juneau",
    "state": "AK",
    "photo": "/assets/i-do-nothing-but-love-lAyXdl1-Wmc-unsplash.jpg",
    "availableUnits": 1,
    "wifi": false,
    "laundry": false
    },
    {
    "id": 3,
    "name": "Homesteady Housing",
    "city": "Chicago",
    "state": "IL",
    "photo": "/assets/ian-macdonald-W8z6aiwfi1E-unsplash.jpg",
    "availableUnits": 1,
    "wifi": true,
    "laundry": false
    },
    {
    "id": 4,
    "name": "Happy Homes Group",
    "city": "Gary",
    "state": "IN",
    "photo": "/assets/krzysztof-hepner-978RAXoXnH4-unsplash.jpg",
    "availableUnits": 1,
    "wifi": true,
    "laundry": false
    },
    {
    "id": 5,
    "name": "Hopeful Apartment Group",
    "city": "Oakland",
    "state": "CA",
    "photo": "/assets/r-architecture-JvQ0Q5IkeMM-unsplash.jpg",
    "availableUnits": 2,
    "wifi": true,
    "laundry": true
    },
    {
    "id": 6,
    "name": "Seriously Safe Towns",
    "city": "Oakland",
    "state": "CA",
    "photo": "/assets/phil-hearing-IYfp2Ixe9nM-unsplash.jpg",
    "availableUnits": 5,
    "wifi": true,
    "laundry": true
    },
    {
    "id": 7,
    "name": "Hopeful Housing Solutions",
    "city": "Oakland",
    "state": "CA",
    "photo": "/assets/r-architecture-GGupkreKwxA-unsplash.jpg",
    "availableUnits": 2,
    "wifi": true,
    "laundry": true
    },
    {
    "id": 8,
    "name": "Seriously Safe Towns",
    "city": "Oakland",
    "state": "CA",
    "photo": "/assets/saru-robert-9rP3mxf8qWI-unsplash.jpg",
    "availableUnits": 10,
    "wifi": false,
    "laundry": false
    },
    {
    "id": 9,
    "name": "Capital Safe Towns",
    "city": "Portland",
    "state": "OR",
    "photo": "/assets/webaliser-_TPTXZd9mOo-unsplash.jpg",
    "availableUnits": 6,
    "wifi": true,
    "laundry": true
    }
    ]
    }
    </code-example>

1.  Save this file.

1.  Time to test your configuration. From the command line, at the root of your project run the following commands.

    <code-example language="bash" format="bash">
        json-server --watch db.json
    </code-example>

1.  In your web browser, navigate to the `http://localhost:3000/locations` and confirm that the response includes the data stored in `db.json`.

Если у вас возникли проблемы с конфигурацией, вы можете найти более подробную информацию в [официальной документации](https://www.npmjs.com/package/json-server).

### Шаг 2 - Обновление сервиса для использования веб-сервера вместо локального массива

Источник данных настроен, следующим шагом будет обновление веб-приложения для подключения к нему и использования данных.

1.  В `src/app/housing.service.ts` внесите следующие изменения:

    1.  Обновите код, чтобы удалить свойство `housingLocationList` и массив, содержащий данные.

    1.  Добавьте строковое свойство с именем и установите значение `'http://localhost:3000/locations'`.

        <code-example anguage="javascript" format="javascript">

        url = 'http://localhost:3000/locations';

        </code-example>

        Этот код приведет к ошибкам в остальной части файла, поскольку он зависит от свойства `housingLocationList`. Далее мы обновим методы сервиса.

    1.  Обновите функцию `getAllHousingLocations`, чтобы она выполняла вызов веб-сервера, который вы настроили.

        <code-example header="" path="first-app-lesson-14/src/app/housing.service.ts" region="update-getAllHousingLocations"></code-example>.

        Теперь код использует асинхронный код для выполнения `get` запроса через `HTTP`. Обратите внимание, что для этого примера в коде используется fetch. Для более продвинутых случаев использования рассмотрим использование `HttpClient`, предоставляемого Angular.

    1.  Обновите функцию `getHousingLocationsById`, чтобы сделать вызов к веб-серверу, который вы настроили.

        <code-example header="" path="first-app-lesson-14/src/app/housing.service.ts" region="update-getHousingLocationById"></code-example>.

    1.  Когда все обновления будут завершены, ваш обновленный сервис будет соответствовать следующему коду.

        <code-example header="Final version of housing.service.ts" path="first-app-lesson-14/src/app/housing.service.ts"></code-example>.

### Шаг 3 - Обновление компонентов для использования асинхронных вызовов службы жилья

Сервер теперь читает данные из запроса `HTTP`, но компоненты, которые полагаются на службу, теперь имеют ошибки, потому что они были запрограммированы на использование синхронной версии службы.

1.  В `src/app/home/home.component.ts` обновите конструктор, чтобы использовать новую асинхронную версию метода `getAllHousingLocations`.

    <code-example header="" path="first-app-lesson-14/src/app/home/home.component.ts" region="update-home-component-constructor"></code-example>

1.  В `src/app/details/details.component.ts` обновите конструктор, чтобы использовать новую асинхронную версию метода `getHousingLocationById`.

    <code-example header="" path="first-app-lesson-14/src/app/details/details.component.ts" region="update-details-component-constructor"></code-example>.

1.  Сохраните свой код.

1.  Откройте приложение в браузере и убедитесь, что оно работает без ошибок.

## Обзор урока

В этом уроке вы обновили свое приложение, чтобы:

-   использовать локальный веб-сервер (`json-server`)

-   использовать асинхронные методы сервиса для получения данных.

Поздравляем! Вы успешно завершили этот урок и готовы продолжить свое путешествие по созданию еще более сложных приложений Angular Apps. Если вы хотите узнать больше, пожалуйста, рассмотрите другие [учебники](./first-app.md) и [руководства](developer-guide-overview.md) по Angular для разработчиков.
